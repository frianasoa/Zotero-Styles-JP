from .chicago import Chicago

class Kyosei(Chicago):
    def __init__(self, input, journal, suffix):
        super().__init__(input, journal, suffix)
    
    def custom(self):
        # remove comma after name (setcitation)
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":""})
                
        # Issue number
        self.originallocators()

        # Japanese dot at the end [ja & en]
        #remove general suffix
        self.setattr(self.bibliography, "z:layout", {"suffix": None})
        text = self.render({"tag": "text"}, self.bibliography, path="z:layout")
        c = self.addcondition(text, ".")
        self.setattr(c["if"], "text", {"value": "。"})
        self.setattr(c["else"], "text", {"value": "."})
        
        # remove dot prefix in access
        self.setattr(self.bibliography, "z:layout/z:text[@macro='access']", {"prefix": None})
        
        # add space in front of URL
        

        # Volume
        
        # Title
        t = self.conds["title"] 
        self.setattr(t["else"], "z:text", {"quotes":"false", "prefix": "“", "suffix":"”"})
        
        # Journal name
        t = self.conds["container-title"]
        self.setattr(t["if"], "z:group/choose/if/z:text", {"prefix":None, "suffix":None})
        self.setattr(t["else"], "z:group/choose/if/z:text", {"prefix":" ", "suffix":". "})
        
        # webpage container title [ja]
        ctw = self.conds["container-title-webpage"]
        self.setattr(ctw["if"], "z:text", {"prefix":"、", "suffix":"。"})

        # Journal name (Add comma in front) [ja]
        t = self.conds["container-title"]
        self.setattr(t["if"], "z:group/choose/if/z:text", {"prefix":"『", "suffix":"』"})
        
        # Date no parentheses
        c = self.conds["date"]
        self.setattr(c["else"], "z:group/z:date[@variable='original-date']", {"prefix": " ", "suffix": ". "})
        self.setattr(c["else"], "z:group/z:date[@variable='issued']", {"prefix": " ", "suffix": ". "})
        
        # Date with comma [ja]
        self.setattr(c["if"], "z:group/z:date[@variable='original-date']", {"prefix": " ", "suffix": ""})
        self.setattr(c["if"], "z:group/z:date[@variable='issued']", {"prefix": " ", "suffix": ""})
        
        # Bibliography author
        c = self.conds["contributors"]
        self.setattr(c["if"], "z:names/z:name", {"name-as-sort-order": None})
        self.render({"tag": "name-part", "attrib": {"name": "family"}}, c["if"], path="z:names/z:name")
        self.render({"tag": "name-part", "attrib": {"name": "given", "prefix": " "}}, c["if"], path="z:names/z:name")
        
        self.setattr(c["else"], "z:names", {"suffix": ". "})
        self.setattr(c["else"], "z:names/z:name", {"initialize": "false", "and": "text"})
        self.setattr(c["else"], "z:names/z:label", {"form": None})
        
        # remove dot before "In"
        c = self.conds["container-contributors"]
        self.setattr(c["else"], "text", {"prefix": " "})
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:name", {"and": "text", "initialize": "false", "name-as-sort-order": "all"})
        
        # add 、 in front of contributors [ja]
        # self.setattr(c["if"], "z:group", {"prefix": "、", "suffix": "、"})
        
        # remov 、 in front of publisher [ja]
        c = self.conds["publisher"]
        self.setattr(c["if"], "z:group", {"prefix": None})
        
        c = self.conds["secondary-contributors"]
        self.setattr(c["if"], "z:group", {"suffix": "、"})
        
        #move issue towards the end
        self.move(self.bibliography, "z:layout/z:text[@macro='issue']", "z:layout/z:text[@macro='locators-article']")
    
    def locatorschapter(self):
        lc = self.macros.get("locators-chapter", None)
        self.setattr(lc, "z:choose/z:if/z:choose/z:if/z:group", {"prefix": " pp. ", "suffix": "、"})

    def locatorsarticle(self):
        la = self.macros.get("locators-article", None)
        self.setattr(la, "z:choose/z:else-if/z:choose/z:if/z:text", {"prefix": ":"})
        
        # c = self.addcondition(la, "z:choose/z:else-if[@type='article-journal']/z:choose/z:if/z:text")
        # self.setattr(c["if"], "z:text", {"prefix": "、", "suffix": "頁"})
        # self.setattr(c["else"], "z:text", {"prefix": ", ", "suffix": ""})
        # d = self.addcondition(la, "z:choose/z:else-if[@type='article-journal']/z:choose/z:else/z:text")
        # self.conds["locators-article"] = c
        
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
                "tag": "date", "attrib": {"variable": "accessed", "prefix":"（", "suffix":" アクセス）", "delimiter": "/"},
                "children": [
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"year"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"month"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"day"}}
                ]
            },
            c["if"], path="z:choose/z:if/z:choose/z:else")
        
        self.delelement(c["else"], "z:choose/z:if/z:choose/z:else/date")
        self.render(
            {
                "tag": "date", "attrib": {"variable": "accessed", "prefix":"（", "suffix":" アクセス）", "delimiter": "/"},
                "children": [
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"year"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"month"}},
                    {"tag": "date-part", "attrib": {"form":"numeric", "name":"day"}}
                ]
            },
            c["else"], path="z:choose/z:if/z:choose/z:else")
        
        #remove date
        self.delelement(a, "z:group/z:choose[2]")
        self.conds["access"] = c