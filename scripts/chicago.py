import os, copy, datetime, pytz
from lxml import etree as ET
from lxml.etree import SubElement, QName

class Chicago:
    def __init__(self, input, journal, suffix, doclinks, config={}):
        self.conds = {}
        self.config = config
        self.ns = {"z": "http://purl.org/net/xbiblio/csl"}
        self.input = input
        self.journal = journal
        self.suffix = suffix
        self.doclinks = doclinks
        parser = ET.XMLParser(remove_blank_text=True)
        self.tree = ET.parse(self.input, parser)
        self.root = self.tree.getroot()
        self.info = self.tree.findall('z:info', self.ns)[0]
        self.macros = self.getmacros()
        self.locales = self.getlocales()
        self.citation = self.tree.findall('z:citation', self.ns)[0]
        self.bibliography = self.tree.findall('z:bibliography', self.ns)[0]
        self.setdoclinks()
    
    def custom(self):
        pass
    
    def setdoclinks(self):
        for l in self.doclinks:
            self.render({"tag": "link", "attrib": {"href":l, "rel": "documentation"}}, self.info, previous=self.child(self.info, "z:link[2]"))
    
    def create(self):
        self.create_()
        self.custom()
        self.save()
        
    def create_(self):
        self.setroot()
        self.doctitle()
        self.id()
        self.contributor()
        self.summary()
        self.locale()
        self.setbiblio()
        self.setcitation()
        self.updated()
        
        # macros
        self.setissue()
        self.setdate()
        self.access()
        self.setcontainertitle()
        self.locatorsarticle()
        self.locatorschapter()
        self.locators()
        self.containercontributors()
        self.contributors()
        self.contributorsshort()
        self.publisher()
        self.title()
        self.secondarycontributors()
        self.translator()
        self.edition()
        self.shortpageprefix()
        self.dateintext()
        
    def updated(self):  
        up = self.child(self.info, "z:updated")
        up.text = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    
    def setcitation(self):
        self.setattr(self.citation, ".", {
            "et-al-min":"3",
            "disambiguate-add-year-suffix":"false",
            "disambiguate-add-names":"false",
            "disambiguate-add-givenname":"false",
        })
        
        """
        Add comma after name
        """
        
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":self.config.get("short-author-suffix", ", ")})
        self.setattr(self.citation, "z:layout", {"prefix": "（", "suffix": "）"})
        
        """
        Add condition
        """
        c = self.addcondition(self.citation, "z:layout/z:group/z:choose/z:if/z:group")
        self.setattr(c["if"], "z:group", {"delimiter": ""}) 
        self.setattr(c["else"], "z:group", {"delimiter": " "})
        
        
        
    def setbiblio(self):
        self.move(self.bibliography, "z:layout/z:text[@macro='issue']", "z:layout/z:text[@macro='edition']")
        self.move(self.bibliography, "z:layout/z:text[@macro='container-title']", "z:layout/z:text[@macro='container-contributors']")
        self.setattr(self.bibliography, "z:layout/z:text[@macro='container-title']", {"prefix":""})
        self.setattr(self.bibliography, "z:layout/z:group", {"delimiter":""})
        
        self.delattr(self.bibliography, ".", "subsequent-author-substitute")
        
        parent = self.bibliography.xpath("z:sort", namespaces=self.ns)[0]
        after = self.bibliography.xpath("z:sort/z:key[@macro='contributors']", namespaces=self.ns)[0]
        self.render({"tag":"key", "attrib":{"variable": "name-kana"}}, parent, after=after)
    
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
        self.delelement(en, ".")
        
        locale = {
            "tag":"locale", 
            "attrib": {self.q("lang"): "en"}, 
            "children": [
                {
                    "tag": "terms", 
                    "children": 
                    [
                        {"tag": "term", "attrib": {"name": "editortranslator", "form":"verb"}, "text": "編訳"},
                        {"tag": "term", "attrib": {"name": "editortranslator", "form":"verb-short"}, "text": "Edited and translated by"},
                        {"tag": "term", "attrib": {"name": "translator", "form":"verb"}, "text": "訳"},
                        {"tag": "term", "attrib": {"name": "translator", "form":"verb-short"}, "text": "Translated by"},
                        {"tag": "term", "attrib": {"name": "and others"}, "text": "ほか"},
                        {"tag": "term", "attrib": {"name": "editor", "form":"short"}, "children": [
                            {"tag": "single", "text": "ed."},
                            {"tag": "multiple", "text": "eds."},
                        ]}
                    ]}
            ]}
        self.render(locale, self.root, self.info)
    
    def dateintext(self):
        dit = self.macros.get("date-in-text", None)
        self.setattr(dit, "z:choose/z:if/z:group", {"delimiter": None}) 
        self.setattr(dit, "z:choose/z:if/z:group/z:date[@variable='original-date']", {"prefix": None, "suffix": "="}) 
    
    def setroot(self):
        self.root.attrib["default-locale"] = "en-US"
        self.root.attrib["page-range-format"] = "expanded"
    
    def setissue(self):
        issue = self.macros.get("issue", None)
        c = self.addcondition(issue, "z:choose/z:else/z:group")
        self.setattr(c["if"], "z:group", {"prefix": "", "delimiter": ""}) 
        self.setattr(c["else"], "z:group", {"prefix": ". ", "delimiter": ", "})
        
    def setdate(self):
        date = self.macros.get("date", None)
        c = self.addcondition(date, "z:choose/z:if[@variable='issued']/z:group")
        self.conds["date"] = c
        
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
        self.conds["title-1"] = text
        
        group = self.addcondition(c1, "z:group")
        self.conds["title-2"] = group
        
        self.setattr(text["if"], "z:text", {"text-case": None, "prefix": "『", "suffix": "』"})
        
        self.setattr(group["if"], "z:group", {
            "prefix": "（", "suffix": "）"
        })
        
        c2 = self.child(t, "z:choose/z:else")
        t = self.addcondition(c2, "z:text")
        self.conds["title-3"] = t
        
        self.setattr(t["if"], "z:text", {"quotes":"false", "prefix": "「", "suffix": "」"})
        self.setattr(t["else"], "z:text", {"quotes":"false"})
        self.conds["title"] = t
        
    def edition(self):
        e = self.macros.get("edition", None)
        c = self.addcondition(e, "z:choose/z:else-if/z:choose/z:else/z:text")
        self.setattr(c["if"], "z:text", {"prefix": "（", "suffix": "）"}   )
        self.setattr(c["else"], "z:text", {"prefix": " (", "suffix": ") "} )
        self.conds["edition"] = c
    
    def translator(self):
        return
        t = self.macros.get("translator", None)
        c = self.addcondition(t, "z:names")
        self.render({"tag": "text", "attrib": {"term": "translated by "}}, c["else"])
        
    
    def secondarycontributors(self):
        p = self.macros.get("secondary-contributors", None)
        c = self.addcondition(p, "z:choose/z:if/z:group")
        self.setattr(c["if"], "z:group", {"delimiter": "・", "suffix": None})
        self.setattr(c["if"], "z:group/z:names[@variable='editor translator']", {"delimiter": None, "suffix": "、"})
        self.setattr(c["if"], "z:group/z:names[@variable='director']", {"delimiter": None, "suffix": None})
        self.move(c["if"], "z:group/z:names[@variable='editor translator']/z:label", "z:group/z:names[@variable='editor translator']/z:name" )
        
        # else
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']", {"delimiter": ", ", "prefix":". "})
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:label", {"form": "verb-short"})
        
        self.conds["secondary-contributors"] = c
        
        self.setattr(self.bibliography, "z:layout/z:text[@macro='secondary-contributors']", {"prefix": None})
        
    def publisher(self):
        p = self.macros.get("publisher", None)
        c = self.addcondition(p, "z:group")
        self.conds["publisher"] = c
        
    def contributorsshort(self):
        cs = self.macros.get("contributors-short", None)
        c = self.addcondition(cs, "z:names")
        self.conds["contributors-short"] = c
        
        self.setattr(c["if"], "z:names/z:name", {"form":"short", "delimiter":"・", "and": None, "initialize-with": None})
        
        self.setattr(c["else"], "z:names/z:name", {"and":"symbol"})
        
        names = c["if"].xpath("z:names/z:name", namespaces=self.ns)
        if len(names)<=0:
            return
        else:
            name = names[0]
        
        self.render({"tag": "et-al", "attrib":{"term": "and others"}}, name.getparent(), name)
        
    def contributors(self):
        c = self.macros.get("contributors", None)
        v = self.addcondition(c, "z:group/z:names[@variable='author']")
        
        self.setattr(v["if"], "z:names/z:name", {
            "name-as-sort-order":"all", "delimiter":"・", "delimiter-precedes-last":"never", "and": None, "sort-separator":None
        })
        
        editors = v["if"].xpath("z:names/z:substitute/z:names[@variable='editor']", namespaces=self.ns)
        if len(editors)>0:
            editor = editors[0]
            self.setattr(editor, ".", {"suffix":"編"})
            self.render({"tag": "name", "attrib": { "name-as-sort-order":"all", "delimiter":"・", "delimiter-precedes-last":"never"}}, editor, where=0)
        
        self.setattr(v["else"], "z:names/z:name", {"and": "symbol", "name-as-sort-order": "all", "delimiter-precedes-last": "never", "initialize-with": ". "})
        
        self.delelement(v["if"], "z:names/z:label")
        
        c = v["if"].getparent().getparent().getparent()
        self.move(c, "z:group/z:text", "z:group/choose")
        
        self.conds["contributors"] = v

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
        self.conds["container-contributors"] = c
    
    def getchild(self, parent, xpath):
        return parent.xpath(xpath, namespaces=self.ns)[0]
    
    def locators(self):
        l = self.macros.get("locators", None)
        group = self.render({"tag":"group"}, l, path="z:choose/z:if[@type='article-journal']")
        group.insert(0, self.child(l, "z:choose/z:if[@type='article-journal']/z:choose"))
        
        aj = self.addcondition(l, "z:choose/z:if[@type='article-journal']/group")
        self.conds["locators"] = aj
        
        self.setattr(aj["if"], "group/z:choose/z:if[@variable='volume']/z:text", {"prefix": None, "suffix": "巻"})
        
        self.delelement(aj["if"], "group/z:choose/z:if[@variable='volume']/z:group")
        
        # change issue tag from else-if to if
        self.child(aj["if"], "group/z:choose/z:else-if[@variable='issue']").tag = "if"
        
        issue = self.child(aj["if"], "group/z:choose/if[@variable='issue']")
        issued = self.child(aj["if"], "group/z:choose/z:else")
        
        self.setattr(issue, "z:group/z:text[@variable='issue']", {"suffix":"号"})
        
        self.move(issue, "z:group/z:text[@variable='issue']", "z:group")
        
        self.delelement(issue, "z:group")
        
        # add new choose
        newchoose = self.render({"tag": "choose"}, aj["if"])
        newchoose.insert(0, issue)
        newchoose.insert(1, issued)
        
        # add to group
        self.child(newchoose.getparent(), "group").insert(1, newchoose)
        
        other = self.child(aj["if"], "z:choose/z:else")
        self.setattr(other, "z:date", {"prefix":None})
        
        self.setattr(aj["else"], "z:choose/z:if[@variable='volume']/z:group", {"prefix": "(", "suffix":")"})
        
        # bill book graphic legal_case legislation motion_picture report song
        c = self.addcondition(l, "z:choose/z:else-if[@type='bill book graphic legal_case legislation motion_picture report song']/z:group")
        self.setattr(c["if"], "z:group", {"prefix":"", "delimiter":""})
        
        self.delelement(c["if"], "z:group/z:group/z:text[@term='volume']")
        self.setattr(c["if"], "z:group/z:group/z:number", {"prefix":"（", "suffix":"）"})
        
        number = self.child(c["if"], "z:group/z:group/z:number[@variable='number-of-volumes']")
        self.conds["locator-bill-etc"] = c
        if number is None:
            return
        group = number.getparent()
        
        
        self.render({"tag": "text", "attrib": {"term": "volume", "form": "short", "prefix": " ", "plural": "true"}}, group)
        
    def locatorschapter(self):
        lc = self.macros.get("locators-chapter", None)
        c = self.addcondition(lc, "z:choose/z:if/z:choose/z:if/z:group")
        self.setattr(c["if"], "z:group", {"prefix": "、", "suffix": "頁"})
        self.setattr(c["else"], "z:group", {"prefix": ", pp. "})
        self.conds["locators-chapter"] = c
    
    def locatorsarticle(self):
        la = self.macros.get("locators-article", None)
        c = self.addcondition(la, "z:choose/z:else-if[@type='article-journal']/z:choose/z:if/z:text")
        self.setattr(c["if"], "z:text", {"prefix": "、", "suffix": "頁"})
        self.setattr(c["else"], "z:text", {"prefix": ", ", "suffix": ""})
        d = self.addcondition(la, "z:choose/z:else-if[@type='article-journal']/z:choose/z:else/z:text")
        self.conds["locators-article"] = c
    
    def access(self):
        a = self.macros.get("access", None)
        self.setattr(a, "z:group", {"delimiter": " "})
        c = self.addcondition(a, "z:group/z:choose[4]")
        self.setattr(c["else"], "z:choose/z:if/z:choose/z:else/z:text", {"suffix": " "})
        self.render({"tag": "date", "attrib": {"variable": "accessed", "prefix": " (", "suffix": ")", "form":"text"}}, c["else"], path="z:choose/z:if/z:choose/z:else")
        
        # Japanese
        self.setattr(c["if"], "z:choose/z:if/z:choose/z:else/z:text", {"suffix": " "})
        self.render(
            {
                "tag": "date", "attrib": {"variable": "accessed", "prefix": "（", "suffix": "）"},
                "children": [
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"year", "suffix": "年"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"month", "suffix": "月"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"day", "suffix": "日"}}
                ]
            },
            c["if"], path="z:choose/z:if/z:choose/z:else")
        #remove date
        self.delelement(a, "z:group/z:choose[2]")
        self.conds["access"] = c
        
    def setcontainertitle(self):
        # Remove container-prefix "in"
        ct = self.macros.get("container-title", None)
        self.delelement(ct, "z:choose/z:if[@type='chapter entry-dictionary entry-encyclopedia paper-conference' and @match='any']", delparent=True)
        
        # Add condition
        c = self.addcondition(ct, "z:choose/z:else-if[@type='legal_case' and @match='none']/z:group")
        
        # for japanese
        jaja = c["if"].xpath("z:group/z:text", namespaces=self.ns)
        if len(jaja)<=0:
            return
        else:
            jaja = jaja[0]
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
        self.conds["container-title"] = c

        # Suffix
        self.setattr(c["else"], "z:group/z:choose[position()=2]/z:if/z:text", {"suffix": "*"})
        
        # for webpage
        cwp = self.addcondition(ct, "z:choose/z:if[@type='webpage']/z:text")
        self.setattr(cwp["if"], "z:text", {"suffix": "、", "prefix": "、"})
        self.setattr(cwp["else"], "z:text", {"prefix": " "})
        self.conds["container-title-webpage"] = cwp
    
    def originallocators(self):
        aj = self.conds["locators"]
        t = aj["if"].getparent().getparent()
        self.delelement(t, "choose")
        self.render({"tag": "group", "children":[{"tag": "choose", "children": [
            {"tag": "if", "attrib":{"variable": "volume issue", "match": "all"}, "children": [{"tag":"text", "attrib":{"variable": "volume"}}, {"tag":"text", "attrib":{"variable": "issue", "prefix": "(", "suffix": ")"}}]},
            {"tag": "else-if", "attrib":{"variable": "volume"}, "children": [{"tag":"text", "attrib":{"variable": "volume"}}]},
            {"tag": "else-if", "attrib":{"variable": "issue"}, "children": [{"tag":"text", "attrib":{"variable": "issue"}}]},
            {"tag": "else", "children": [{"tag":"date", "attrib":{"variable": "issued", "prefix": "(", "suffix": ")"}, "children":[{"tag": "date-part", "attrib":{"name": "month"}}]}]},
            
        ]}]}, t)
    
    def getmacros(self):
        m = self.tree.findall('z:macro', self.ns)
        m = {x.attrib["name"]:x for x in m}
        return m
    
    def getlocales(self):
        m = self.tree.findall('z:locale', self.ns)
        m = {x.attrib[self.q("lang")]:x for x in m}
        return m
    
    def addcondition(self, target, xpath, elifs={}):
        """
        If the entry contains a field name-kana
        """
        
        element = target.xpath(xpath, namespaces=self.ns)
        
        if len(element)<=0:
            print("Not found")
            print(target)
            print(xpath)
            return {
                "if": SubElement(self.root, "condition-error"),
                "else": SubElement(self.root, "condition-error")
            }
        else:
            element = element[0]
        
        elementcopy = copy.deepcopy(element)
        parent = element.getparent()
        choose = self.render({"tag": "choose"}, parent)
        r = {}
        
        x = 0
        for t in elifs:
            c = elifs[t]
            if x==0:
                elifel = self.render({"tag": "if", "attrib":{"variable": c}}, choose)
            else:
                elifel = self.render({"tag": "else-if", "attrib":{"variable": c}}, choose)
            elifel.insert(0, copy.deepcopy(element))
            r[t]= elifel
            x+=1
        
        # else if but kept as "if" for consistency
        if len(elifs)==0:
            ifel = self.render({"tag": "if", "attrib":{"variable": "name-kana"}}, choose)
        else:
            ifel = self.render({"tag": "else-if", "attrib":{"variable": "name-kana"}}, choose)
        ifel.insert(0, elementcopy)
        r["if"] = ifel
        
        elseel = self.render({"tag": "else"}, choose)        
        elseel.insert(0, element)
        r["else"] =  elseel
        return r
    
    def splitlocales(self, target, xpath, locales):
        element = target.xpath(xpath, namespaces=self.ns)
        
        if len(element)<=0:
            print("Not found")
            print(target)
            print(xpath)
            return {
                "if": SubElement(self.root, "condition-error"),
                "else": SubElement(self.root, "condition-error")
            }
        else:
            element = element[0]
        
        r = {"default": element}
        
        for l in locales:
            elementcopy = copy.deepcopy(element)
            self.setattr(elementcopy, ".", {"locale": l})
            parent = element.getparent()
            parent.insert(0, elementcopy)
            r[l] = elementcopy
        return r
    
    def render(self, d, parent, previous=None, after=None, where=None, path=None):
        if path is not None:
            parent = self.child(parent, path)
            
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
    
    def unwrap(self, element, clean=True):
        parent = element.getparent()
        children = element.getchildren()
        index =  element.getparent().getchildren().index(element)
        for c in children:
            parent.insert(index, c)
            index+=1
        if clean:
            parent.remove(element)
    
    def wrap(self, element, w="group", attrib={}):
        children = element.getchildren()
        # group = self.render({"tag": w}, element)
        group = SubElement(self.root, w)
        for c in children:
            group.insert(-1, c)
        element.insert(0, group)
        for a in attrib:
            group.attrib[a] = attrib[a]
        
    def shortpagelabel(self, prefix=None, suffix=None):
        pl = self.macros.get("point-locators", None)
        c = self.addcondition(pl, "z:choose/z:if/z:text")
        
        if prefix is not None:
            pref = self.render(prefix["if"], c["if"], where=-2)
            pref = self.render(prefix["else"], c["else"], where=-2)
        if suffix is not None:
            pref = self.render(suffix["if"], c["if"], where=-1)
            pref = self.render(suffix["else"], c["else"], where=-1)
    
    def shortpageprefix(self, prefix=", ", label=""):
        self.setattr(self.citation, "z:layout/z:group", {"delimiter": prefix})
    
    def changetag(self, parent, elementxpath, newtag):
        elements = parent.xpath(elementxpath, namespaces=self.ns)
        if len(elements)>0:
            elements[0].tag = newtag
        else:
            print("No element for "+elementxpath)
            
    def move(self, parent, elementxpath, previousxpath):
        if parent is None:
            return
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
        
    
    def setattrs(self, parent, values):
        for key in values:
            v = values[key]
            parent.attrib[key] = v
        return parent
    
    def setattr(self, parent, element, attr):
        if parent is None:
            return
        
        elt = parent.xpath(element, namespaces=self.ns)
        if len(elt)<=0:
            return
        else:
            elt = elt[0]
        for key in attr:
            value = attr[key]
            if value is None:
                self.delattr(parent, element, key)
            else:
                elt.attrib[key] = value
    
    def delelement(self, parent, xpath, delparent=False):
        if parent is None:
            return
        elements = parent.xpath(xpath, namespaces=self.ns)
        if len(elements)>0:
            p = elements[0].getparent()
            [x.getparent().remove(x) for x in elements]
            if delparent:
                p.getparent().remove(p)
        else:
            print("Not found!")
            print(parent)
            print(xpath)
            
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
        buildoutfile = "build"+"/"+os.path.splitext(os.path.basename(self.input))[0]+"-"+self.suffix["id"]+".csl"
        self.tree.write(outfile, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        self.tree.write(buildoutfile, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    