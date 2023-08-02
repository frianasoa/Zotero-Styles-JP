from .chicago import Chicago

class ICZemi(Chicago):
    def __init__(self, input, journal, suffix, doclinks):
        super().__init__(input, journal, suffix, doclinks)
    
    def setcitation(self):
        self.setattr(self.citation, ".", {
            "et-al-min":"3",
            "disambiguate-add-year-suffix":"false",
            "disambiguate-add-names":"false",
            "disambiguate-add-givenname":"false",
            "after-collapse-delimiter":"; ", #ICZemi
        })
        
        """
        Add comma after name
        """
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":""})
        
        #ICZemi delimiter ":" for page number
        # in self.shortpageprefix
        
        #ICZemi
        self.setattr(self.citation, "z:layout", {"prefix": "（", "suffix": "）", "delimiter": ", "})
        
        c = self.addcondition(self.citation, "z:layout/z:group/z:choose/z:if/z:group")
        self.setattr(c["if"], "z:group", {"delimiter": ""}) 
        self.setattr(c["else"], "z:group", {"delimiter": " "})
    
    def contributors(self):
        c = self.macros.get("contributors", None)
        v = self.addcondition(c, "z:group/z:names[@variable='author']", {"elif": "name-katakana"})
        
        #Katakana authors /waiting for csl to support this in asian script/
        self.setattr(v["elif"], "z:names/z:name", {
            "name-delimiter": "、", "sort-separator":"、","name-as-sort-order":"first", "delimiter":"、",  "and": None, "delimiter-precedes-last": "never", "initialize":"false"
        })
        
        editors = v["elif"].xpath("z:names/z:substitute/z:names[@variable='editor']", namespaces=self.ns)
        if len(editors)>0:
            editor = editors[0]
            self.setattr(editor, ".", {"suffix":"編"})
            self.render({"tag": "name", "attrib": { "name-as-sort-order":"all", "delimiter":"、", "delimiter-precedes-last":"never"}}, editor, where=0)
        
        #Regular japanese
        self.setattr(v["if"], "z:names/z:name", {
            "name-as-sort-order":"all", "delimiter":"、", "delimiter-precedes-last":"never", "and": None, "sort-separator":None
        })
        
        editors = v["if"].xpath("z:names/z:substitute/z:names[@variable='editor']", namespaces=self.ns)
        if len(editors)>0:
            editor = editors[0]
            self.setattr(editor, ".", {"suffix":"編"})
            self.render({"tag": "name", "attrib": { "name-as-sort-order":"all", "delimiter":"・", "delimiter-precedes-last":"never"}}, editor, where=0)
        
        #ICZemi "name-as-sort-order": "first"
        self.setattr(v["else"], "z:names/z:name", {"and": "symbol", "name-as-sort-order": "first", "delimiter-precedes-last": "never", "initialize-with": ". "})
        
        self.delelement(v["if"], "z:names/z:label")
        
        c = v["if"].getparent().getparent().getparent()
        self.move(c, "z:group/z:text", "z:group/choose")
        
        self.conds["contributors"] = v
    
    
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
                "tag": "date", "attrib": {"variable": "accessed", "prefix": "（", "suffix": "閲覧）"},
                "children": [
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"year", "suffix": "年"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"month", "suffix": "月"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"day", "suffix": "日"}}
                ]
            },
            c["if"], path="z:choose/z:if/z:choose/z:else")
        
        # English
        #remove date
        self.delelement(a, "z:group/z:choose[2]")
        
        
        self.render(
            {
                "tag": "date", "attrib": {"variable": "accessed", "prefix": "（", "suffix": "閲覧）"},
                "children": [
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"year", "suffix": "年"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"month", "suffix": "月"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"day", "suffix": "日"}}
                ]
            },
            c["else"], path="z:choose/z:if/z:choose/z:else")
        self.setattr(c["else"], "z:choose/z:if/z:choose/z:if/z:text", {"prefix": ", https://doi.org/", "suffix": None})
        self.conds["access"] = c
    
    def custom(self):
        # remove comma after name (setcitation)
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":""})
        
        # prefix = {"if": {"tag":"label", "attrib": {"variable": "locator", "form": "short", "suffix":" ", "prefix":"："}}, "else": {"tag":"label", "attrib": {"variable": "locator", "form": "short", "suffix":" ", "prefix":"："}}}
        
        # self.shortpagelabel(prefix=prefix)
        
        # No pp to page
        c = self.conds["locators-article"]
        self.setattr(c["else"], "z:text", {"prefix": ":", "suffix": ""})
        self.setattr(c["if"], "z:text", {"prefix": ":", "suffix": ""})
        
        # ----//--- book chapter
        c = self.conds["locators-chapter"]
        self.setattr(c["if"], "z:group", {"prefix": "、pp. ", "suffix": ""})
        
        # Issue number
        aj = self.conds["locators"]
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group/z:choose/z:if[@variable='issue']/z:text", {"prefix": ", No. ", "suffix": None})
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group/z:choose/z:else/z:date", {"prefix": ", (", "suffix": ")"})
        
        # Issue number [ja]
        self.setattr(aj["if"], "group/z:choose/z:if[@variable='volume']/z:text", {"prefix": None, "suffix": None})
        self.setattr(aj["if"], "group/choose/if/z:text", {"prefix": "(", "suffix": ")"})
        self.setattr(aj["if"], "group", {"delimiter": None})
        
        
        # Japanese dot at the end [ja & en]　 in bibliography
        #remove general suffix
        self.setattr(self.bibliography, "z:layout", {"suffix": None})
        text = self.render({"tag": "text"}, self.bibliography, path="z:layout")
        c = self.addcondition(text, ".")
        self.setattr(c["if"], "text", {"value": "."})
        self.setattr(c["else"], "text", {"value": "."})
        
        # remove dot prefix in access
        self.setattr(self.bibliography, "z:layout/z:text[@macro='access']", {"prefix": None})
        
        # add space in front of URL
        # c = self.conds["access"]
        # self.setattr(c["else"], "z:choose/z:if/z:choose/z:if/z:text", {"prefix":". "})
        # self.setattr(c["else"], "z:choose/z:if/z:choose/z:else/z:text", {"prefix":". "})

        # Volume
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:text[@variable='volume']", {"prefix": None, "suffix": None})
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group", {"prefix": None, "suffix": None})
        
        # Issue
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group/z:choose/z:if/z:text", {"prefix": "(", "suffix": ")"})
        
        # Title
        t = self.conds["title"] 
        self.setattr(t["else"], "z:text", {"quotes":"false", "prefix": "“", "suffix":".”"})
        
        # Journal name
        t = self.conds["container-title"]
        self.setattr(t["else"], "z:group/choose/if/z:text", {"prefix":" ", "suffix":", "})
        
        # webpage container title [ja]
        ctw = self.conds["container-title-webpage"]
        self.setattr(ctw["if"], "z:text", {"prefix":"、", "suffix":"。"})

        # Journal name (no comma in front) [ja]
        # t = self.conds["container-title"]
        # self.setattr(t["if"], "z:group/choose/if/z:text", {"prefix":"『"})
        
        # Date with parentheses
        c = self.conds["date"]
        self.setattr(c["else"], "z:group", {"prefix": " (", "suffix": ") "})
        self.setattr(c["else"], "z:group/z:date[@variable='original-date']", {"prefix": "", "suffix": "="})
        self.setattr(c["else"], "z:group/z:date[@variable='issued']", {"prefix": "", "suffix": ""})
        
        # Date with comma [ja] added original-date
        self.setattr(c["if"], "z:group", {"prefix": "（", "suffix": "）"})
        self.setattr(c["if"], "z:group/z:date[@variable='original-date']", {"prefix": "", "suffix": "="})
        self.setattr(c["if"], "z:group/z:date[@variable='issued']", {"prefix": "", "suffix": ""})
        
        # Bibliography author
        c = self.conds["contributors"]
        self.setattr(c["else"], "z:names", {"suffix": " "})
        self.setattr(c["else"], "z:names/z:name", {"initialize": "false", "and": "symbol"})
        self.setattr(c["else"], "z:names/z:label", {"form": None})
        
        # remove dot before "In"
        c = self.conds["container-contributors"]
        self.setattr(c["else"], "text", {"prefix": " "})
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:name", {"and": "text", "initialize": "false", "name-as-sort-order": "none"})
        
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:label", {"suffix": "), "})
        
        # add "In" etc
        
        
        # add 、 in front of contributors [ja]
        self.setattr(c["if"], "z:group", {"prefix": "、", "suffix": ""})
        
        # no 、 in front of publisher [ja]
        c = self.conds["publisher"]
        self.setattr(c["if"], "z:group", {"prefix": None})
        
        #ICZemi change page prefix
        self.shortpageprefix(prefix=":")