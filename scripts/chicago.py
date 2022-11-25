import os, copy
from lxml import etree as ET
from lxml.etree import SubElement, QName

class Chicago:
    def __init__(self, input, journal, suffix):
        self.ns = {"z": "http://purl.org/net/xbiblio/csl"}
        self.input = input
        self.journal = journal
        self.suffix = suffix
        parser = ET.XMLParser(remove_blank_text=True)
        self.tree = ET.parse(self.input, parser)
        self.root = self.tree.getroot()
        self.info = self.tree.findall('z:info', self.ns)[0]
        self.macros = self.getmacros()
        self.locales = self.getlocales()
        self.citation = self.tree.findall('z:citation', self.ns)[0]
        self.bibliography = self.tree.findall('z:bibliography', self.ns)[0]
      
    def create(self):
        self.language()
        self.doctitle()
        self.id()
        self.contributor()
        self.summary()
        self.locale()
        self.setbiblio()
        self.setcitation()
        
        # macros
        self.setissue()
        self.setdate()
        self.setcontainertitle()
        self.locatorsarticle()
        self.locatorschapter()
        self.locators()
        self.containercontributors()
        self.contributors()
        self.contributorsshort()
        self.title()
        
        #save
        self.save()
    
    
    def setcitation(self):
        self.setattr(self.citation, ".", {
            "et-al-min":"3",
            "disambiguate-add-year-suffix":"false",
            "disambiguate-add-names":"false",
            "disambiguate-add-givenname":"false",
        })
        
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":", "})
    
    def setbiblio(self):
        self.move(self.bibliography, "z:layout/z:text[@macro='issue']", "z:layout/z:text[@macro='edition']")
        self.move(self.bibliography, "z:layout/z:text[@macro='container-title']", "z:layout/z:text[@macro='container-contributors']")
        self.setattr(self.bibliography, "z:layout/z:text[@macro='container-title']", {"prefix":""})
        self.setattr(self.bibliography, "z:layout/z:group", {"delimiter":""})
        
        self.delattr(self.bibliography, ".", "subsequent-author-substitute")
        
        parent = self.bibliography.xpath("z:sort", namespaces=self.ns)[0]
        after = self.bibliography.xpath("z:sort/z:key[@macro='contributors']", namespaces=self.ns)[0]
        self.render({"tag":"key", "attrib":{"variable": "yomi"}}, parent, after=after)
    
    def summary(self):
        for summary in self.tree.findall('z:info/z:summary', self.ns):
            summary.text = summary.text+" - Edited for "+self.suffix["title"]
            
    def doctitle(self):
        for title in self.tree.findall('z:info/z:title', self.ns):
            title.text = title.text+" - "+self.suffix["title"]
    
    def id(self):
        for id in self.tree.findall('z:info/z:id', self.ns):
            id.text = id.text+"-"+self.suffix["id"]
            
    def contributor(self):
        last_contributor = self.info.findall("z:contributor", self.ns)[-1]
        moi = {
            "tag": "contributor", "children": [
                {"tag": "name", "text": "Fanantenana Rianasoa Andriariniaina"},
                {"tag": "uri", "text": "https://orcid.org/0000-0002-8665-0922"},
            ]
        }
        self.render(moi, self.info, last_contributor)
    
    def q(self, v):
        return QName("http://www.w3.org/XML/1998/namespace", v)
    
    def locale(self):
        en = self.locales["en"]
        self.delelement(en, "z:terms/z:term[@name='editor' and @form='verb-short']")
        
        locale = {
            "tag":"locale", 
            "attrib": {self.q("lang"): "ja"}, 
            "children": [
                {
                    "tag": "terms", 
                    "children": 
                    [
                        {"tag": "term", "attrib": {"name": "and others"}, "text": "et al."},
                        {"tag": "term", "attrib": {"name": "editor", "form":"short"}, "children": [
                            {"tag": "single", "text": "ed."},
                            {"tag": "multiple", "text": "eds."},
                        ]}
                    ]}
            ]}
        self.render(locale, self.root, self.info)
    
    def language(self):
        self.root.attrib["default-locale"] = "ja-JA"
    
    def setissue(self):
        issue = self.macros.get("issue", None)
        c = self.addcondition(issue, "z:choose/z:else/z:group")
        self.setattr(c["if"], "z:group", {"prefix": "", "delimiter": ""}) 
        self.setattr(c["else"], "z:group", {"prefix": ". ", "delimiter": ", "})
        
    def setdate(self):
        date = self.macros.get("date", None)
        c = self.addcondition(date, "z:choose/z:if[@variable='issued']/z:group")
        
        # if Japanese
        self.setattr(c["if"], "z:group", {"delimiter": ""}) 
        self.setattr(c["if"], "z:group/z:date[@variable='original-date']", {"prefix": "（", "suffix": "）"}) 
        self.setattr(c["if"], "z:group/z:date[@variable='issued']", {"prefix": "（", "suffix": "）"})
        
        # if not Japanese
        self.setattr(c["else"], "z:group", {"delimiter": ""})
        self.setattr(c["else"], "z:group/z:date[@variable='original-date']", {"prefix": " (", "suffix": ")."})
        self.setattr(c["else"], "z:group/z:date[@variable='issued']", {"prefix": " (", "suffix": "). "})
      
    
    def title(self):
        t = self.macros.get("title", None)
        c1 = self.child(t, "z:choose/z:else-if[@type='bill book graphic legislation motion_picture song']")
        
        text = self.addcondition(c1, "z:text")
        group = self.addcondition(c1, "z:group")
        
        self.setattr(text["if"], "z:text", {"text-case": None, "prefix": "『", "suffix": "』"})
        
        self.setattr(group["if"], "z:group", {
            "prefix": "（", "suffix": "）"
        })
        
        c2 = self.child(t, "z:choose/z:else")
        text2 = self.addcondition(c2, "z:text")
        self.setattr(text2["if"], "z:text", {"quotes":"false", "prefix": "「", "suffix": "」"})
        
        self.setattr(text2["else"], "z:text", {"quotes":"false"})
        
    def contributorsshort(self):
        cs = self.macros.get("contributors-short", None)
        c = self.addcondition(cs, "z:names")
        self.setattr(c["if"], "z:names/z:name", {"form":"short", "delimiter":"・", "and": None, "initialize-with": None})
        
        self.setattr(c["else"], "z:names/z:name", {"and":"symbol"})
        
        name = c["else"].xpath("z:names/z:name", namespaces=self.ns)[0]
        
        
        self.render({"tag": "et-al", "attrib":{"term": "and others"}}, name.getparent(), name)
        
    def contributors(self):
        c = self.macros.get("contributors", None)
        v = self.addcondition(c, "z:group/z:names[@variable='author']")
        
        self.setattr(v["if"], "z:names/z:name", {
            "name-as-sort-order":"all", "delimiter":"・", "delimiter-precedes-last":"never", "and": None, "sort-separator":None
        })
        
        editor = v["if"].xpath("z:names/z:substitute/z:names[@variable='editor']", namespaces=self.ns)[0]
        self.setattr(editor, ".", {"suffix":"編"})
        self.render({"tag": "name", "attrib": { "name-as-sort-order":"all", "delimiter":"・", "delimiter-precedes-last":"never"}}, editor, where=0)
        
        self.setattr(v["else"], "z:names/z:name", {"and": "symbol", "name-as-sort-order": "all", "delimiter-precedes-last": "never", "initialize-with": ". "})
        
        self.delelement(v["if"], "z:names/z:label")
        
        c = v["if"].getparent().getparent().getparent()
        self.move(c, "z:group/z:text", "z:group/choose")

    def containercontributors(self):
        cc = self.macros.get("container-contributors", None)
        c = self.addcondition(cc, "z:choose/z:if[@type='chapter entry-dictionary entry-encyclopedia paper-conference']/z:group")
        
        self.setattr(c["if"], "z:group", {"prefix":"", "delimiter":""})
        self.setattr(c["if"], "z:group/z:names[@variable='container-author']", {"delimiter":"・"})
        self.setattr(c["if"], "z:group/z:names[@variable='container-author']/z:name", {"and":None, "delimiter":"・"})
        
        self.setattr(c["if"], "z:group/z:names[@variable='editor translator']", {"delimiter":"・", "suffix": "編"})
        self.setattr(c["if"], "z:group/z:names[@variable='editor translator']/z:name", {"and":None, "delimiter": "・", "sort-separator":", ", "delimiter-precedes-last":"never"})
        self.delelement(c["if"], "z:group/z:names[@variable='editor translator']/z:label")
        
        self.setattr(c["else"], "z:group", {"prefix":" "})
        self.move(c["else"], "z:group/z:names[@variable='editor translator']/z:label", "z:group/z:names[@variable='editor translator']/z:name")
        
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:name", {
        "and":"symbol", "delimiter":", ", "sort-separator":", ", "delimiter-precedes-last": "never", "initialize-with":". "})
        
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:label", {
        "form": "short", "prefix": None, "suffix": None})
        
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:label", {
        "form": "short", "prefix": " (", "suffix":"). "})
        
        self.render({"tag": "text", "attrib":{"value": "In", "suffix":" ", "prefix": ". "}}, c["else"], where=0)
    
    def getchild(self, parent, xpath):
        return parent.xpath(xpath, namespaces=self.ns)[0]
    
    def locators(self):
        l = self.macros.get("locators", None)
        aj = self.addcondition(l, "z:choose/z:if[@type='article-journal']/z:choose")
        
        self.setattr(aj["if"], "z:choose/z:if[@variable='volume']/z:text", {"prefix": None, "suffix": "巻"})
        
        self.delelement(aj["if"], "z:choose/z:if[@variable='volume']/z:group")
        
        issue = self.child(aj["if"], "z:choose/z:else-if[@variable='issue']")
        
        self.setattr(issue, "z:group/z:text[@variable='issue']", {"suffix":"号"})
        
        self.move(issue, "z:group/z:text[@variable='issue']", "z:group")
        
        self.delelement(issue, "z:group")
        
        other = self.child(aj["if"], "z:choose/z:else")
        self.setattr(other, "z:date", {"prefix":None})
        
        self.setattr(aj["else"], "z:choose/z:if[@variable='volume']/z:group", {"prefix": "(", "suffix":")"})
        
        # bill book graphic legal_case legislation motion_picture report song
        c = self.addcondition(l, "z:choose/z:else-if[@type='bill book graphic legal_case legislation motion_picture report song']/z:group")
        self.setattr(c["if"], "z:group", {"prefix":"", "delimiter":""})
        
        self.delelement(c["if"], "z:group/z:group/z:text[@term='volume']")
        self.setattr(c["if"], "z:group/z:group/z:number", {"prefix":"（", "suffix":"）"})
        
        group = self.child(c["if"], "z:group/z:group/z:number[@variable='number-of-volumes']").getparent()
        self.render({"tag": "text", "attrib": {"term": "volume", "form": "short", "prefix": " ", "plural": "true"}}, group)
        
        
        
    
    def locatorschapter(self):
        lc = self.macros.get("locators-chapter", None)
        c = self.addcondition(lc, "z:choose/z:if/z:choose/z:if/z:group")
        self.setattr(c["if"], "z:group", {"prefix": "、", "suffix": "頁"})
        self.setattr(c["else"], "z:group", {"prefix": ", pp. "})
    
    def locatorsarticle(self):
        la = self.macros.get("locators-article", None)
        c = self.addcondition(la, "z:choose/z:else-if[@type='article-journal']/z:choose/z:if/z:text")
        self.setattr(c["if"], "z:text", {"prefix": "、", "suffix": "頁"})
        self.setattr(c["else"], "z:text", {"prefix": "", "suffix": "頁"})
        
        c = self.addcondition(la, "z:choose/z:else-if[@type='article-journal']/z:choose/z:else/z:text")

    def setcontainertitle(self):
        # Remove container-prefix "in"
        ct = self.macros.get("container-title", None)
        self.delelement(ct, "z:choose/z:if[@type='chapter entry-dictionary entry-encyclopedia paper-conference' and @match='any']", delparent=True)
        
        # Add condition
        c = self.addcondition(ct, "z:choose/z:else-if[@type='legal_case' and @match='none']/z:group")
        
        # for japanese
        jaja = c["if"].xpath("z:group/z:text", namespaces=self.ns)[0]
        self.setattr(jaja, ".", {"font-style": None, "prefix":"『", "suffix": "』"})
        
        group = jaja.getparent()
        choose = self.render({"tag": "choose"}, group)
        ifel = self.render({"tag": "if", "attrib":{"type":"article-journal"}}, choose)
        elseel = self.render({"tag": "else"}, choose)
        ifel.insert(0, jaja)
        elseel.insert(0, copy.deepcopy(jaja))
        
        # other than japanese
        jaelse = c["else"].xpath("z:group/z:text", namespaces=self.ns)[0]
        self.setattr(jaelse, ".", {"prefix":". ", "suffix": ", "})
        
        group = jaelse.getparent()
        choose = self.render({"tag": "choose"}, group)
        ifel = self.render({"tag": "if", "attrib":{"type":"article-journal"}}, choose)
        elseel = self.render({"tag": "else"}, choose)
        ifel.insert(0, jaelse)
        
        # other than journal journal
        jaelseelse = copy.deepcopy(jaelse)
        self.setattr(jaelseelse, ".", {"prefix":None, "suffix": None})
        elseel.insert(0, jaelseelse)        
    
    def getmacros(self):
        m = self.tree.findall('z:macro', self.ns)
        m = {x.attrib["name"]:x for x in m}
        return m
    
    def getlocales(self):
        m = self.tree.findall('z:locale', self.ns)
        m = {x.attrib[self.q("lang")]:x for x in m}
        return m
    
    def addcondition(self, target, xpath):
        element = target.xpath(xpath, namespaces=self.ns)[0]
        elementcopy = copy.deepcopy(element)
        parent = element.getparent()
        
        choose = self.render({"tag": "choose"}, parent)
        ifel = self.render({"tag": "if", "attrib":{"variable": "language"}}, choose)
        elseel = self.render({"tag": "else"}, choose)
        ifel.insert(0, elementcopy)
        elseel.insert(0, element)
        return {
            "if": ifel,
            "else": elseel
        }
    
    def render(self, d, parent, previous=None, after=None, where=None):
        tag = d.get("tag", None)
        attrib = d.get("attrib", {})
        text = d.get("text", None)
        children = d.get("children", [])
        element = None
        
        if where is not None:
            index = where
        elif after is not None:
            index = parent.getchildren().index(after)
        elif previous is not None:
            index = previous.getparent().getchildren().index(previous)+1
        else:
            try:
                previous = parent.getchildren()[len(parent.getchildren())-1]
                index = parent.getchildren().index(previous)+1
            except:
                index = 0
        
        if tag is not None:
            element = SubElement(parent, tag)
            parent.insert(index, element)
            
            if text is not None:
                setattr(element, "text", text)
                
            for key in attrib:
                value = attrib[key]
                element.attrib[key] = value
            
            for child in children:
                self.render(child, element)
        return element
        
    def move(self, parent, elementxpath, previousxpath):
        element = parent.xpath(elementxpath, namespaces=self.ns)
        previous = parent.xpath(previousxpath, namespaces=self.ns)
        
        if len(element)==0:
            print("Element does not exist: "+elementxpath+" in ")
            print(parent)
            print(parent.getchildren())
            print([x.getchildren() for x in parent.getchildren()])
            
        elif len(previous)==0:      
            print("Element does not exist: "+previousxpath+"  in ")
            print(parent)
            print(parent.getchildren())
            print([x.getchildren() for x in parent.getchildren()])
            
        else:
            element = element[0]
            previous = previous[0]
            index = previous.getparent().getchildren().index(previous)+1
            previous.getparent().insert(index, element)
        
        
    def setattr(self, parent, element, attr):
        elt = parent.xpath(element, namespaces=self.ns)[0]
        for key in attr:
            value = attr[key]
            if value is None:
                self.delattr(parent, element, key)
            else:
                elt.attrib[key] = value
    
    def delelement(self, parent, xpath, delparent=False):
        elements = parent.xpath(xpath, namespaces=self.ns)
        p = elements[0].getparent()
        [x.getparent().remove(x) for x in elements]
        if delparent:
            p.getparent().remove(p)
            
    def child(self, parent, path):
        c = parent.xpath(path, namespaces=self.ns)
        if len(c)>0:
            return c[0]
        else:
            return None
    
    def delattr(self, parent, element, attr):
        element = parent.xpath(element, namespaces=self.ns)[0]
        if type(attr)==type([]):
            for a in attr:
                if a in element.attrib:
                    element.attrib.pop(a)
        else:
            if attr in element.attrib:
                element.attrib.pop(attr)
 
    def save(self):
        os.makedirs(self.journal, exist_ok=True)
        outfile = self.journal+"/"+os.path.splitext(os.path.basename(self.input))[0]+"-"+self.suffix["id"]+".csl"
        self.tree.write(outfile, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    