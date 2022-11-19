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
        self.title()
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
            
    def title(self):
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
    
    def render(self, d, parent, previous=None, after=None):
        tag = d.get("tag", None)
        attrib = d.get("attrib", {})
        text = d.get("text", None)
        children = d.get("children", [])
        element = None
        
        if after is not None:
            index = parent.getchildren().index(after)
        elif previous is not None:
            index = parent.getchildren().index(previous)+1
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
        
    def move(self, parent, element, previous):
        element = parent.xpath(element, namespaces=self.ns)[0]
        previous = parent.xpath(previous, namespaces=self.ns)[0]
        index = previous.getparent().getchildren().index(previous)+1
        previous.getparent().insert(index, element)
    
    def setattr(self, parent, element, attr):
        elt = parent.xpath(element, namespaces=self.ns)[0]
        for key in attr:
            value = attr[key]
            if value is None:
                self.delattr(elt, element, key)
            else:
                elt.attrib[key] = value
    
    def delelement(self, parent, xpath, delparent=False):
        elements = parent.xpath(xpath, namespaces=self.ns)
        p = elements[0].getparent()
        [x.getparent().remove(x) for x in elements]
        if delparent:
            p.getparent().remove(p)
            
            
    
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
    