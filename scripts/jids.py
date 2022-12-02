from .chicago import Chicago

class Jids(Chicago):
    def __init__(self, input, journal, suffix):
        super().__init__(input, journal, suffix)
    
    def custom(self):
        # remove comma after name (setcitation)
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":""})
        
        # Add pp to page
        c = self.conds["locators-article"]
        self.setattr(c["else"], "z:text", {"prefix": ", pp. ", "suffix": ""})
        
        # Issue number
        aj = self.conds["locators"]
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group/z:choose/z:if[@variable='issue']/z:text", {"prefix": ", No. ", "suffix": None})
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group/z:choose/z:else/z:date", {"prefix": ", (", "suffix": ")"})
        
        # Issue number [ja]
        self.setattr(aj["if"], "group/z:choose/z:if[@variable='volume']/z:text", {"prefix": "第", "suffix": "巻"})
        self.setattr(aj["if"], "group/choose/if/z:text", {"prefix": "第", "suffix": "号"})
        self.setattr(aj["if"], "group", {"delimiter": "、"})
        
        
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
        c = self.conds["access"]
        self.setattr(c["else"], "z:choose/z:if/z:choose/z:if/z:text", {"prefix":". "})
        self.setattr(c["else"], "z:choose/z:if/z:choose/z:else/z:text", {"prefix":". "})

        # Volume
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:text[@variable='volume']", {"prefix": " Vol. ", "suffix": None})
        self.setattr(aj["else"], "group/z:choose/z:if[@variable='volume']/z:group", {"prefix": None, "suffix": None})
        
        # Title
        t = self.conds["title"] 
        self.setattr(t["else"], "z:text", {"quotes":"false", "prefix": "“", "suffix":"”"})
        
        # Journal name
        t = self.conds["container-title"]
        self.setattr(t["else"], "z:group/choose/if/z:text", {"prefix":" ", "suffix":". "})
        
        # webpage container title [ja]
        ctw = self.conds["container-title-webpage"]
        self.setattr(ctw["if"], "z:text", {"prefix":"、", "suffix":"。"})
        
        
        # Journal name (Add comma in front) [ja]
        t = self.conds["container-title"]
        self.setattr(t["if"], "z:group/choose/if/z:text", {"prefix":"、『"})
        
        # Date no parentheses
        c = self.conds["date"]
        self.setattr(c["else"], "z:group/z:date[@variable='original-date']", {"prefix": " ", "suffix": ". "})
        self.setattr(c["else"], "z:group/z:date[@variable='issued']", {"prefix": " ", "suffix": ". "})
        
        # Date with comma [ja]
        self.setattr(c["if"], "z:group/z:date[@variable='original-date']", {"prefix": "、", "suffix": "、"})
        self.setattr(c["if"], "z:group/z:date[@variable='issued']", {"prefix": "、", "suffix": "、"})
        
        # Bibliography author
        c = self.conds["contributors"]
        self.setattr(c["else"], "z:names", {"suffix": ". "})
        self.setattr(c["else"], "z:names/z:name", {"initialize": "false", "and": "text"})
        self.setattr(c["else"], "z:names/z:label", {"form": None})
        
        # remove dot before "In"
        c = self.conds["container-contributors"]
        self.setattr(c["else"], "text", {"prefix": " "})
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:name", {"and": "text", "initialize": "false", "name-as-sort-order": "all"})
        
        # add 、 in front of contributors [ja]
        self.setattr(c["if"], "z:group", {"prefix": "、", "suffix": "、"})
        
        # add 、 in front of publisher [ja]
        c = self.conds["publisher"]
        self.setattr(c["if"], "z:group", {"prefix": "、"})