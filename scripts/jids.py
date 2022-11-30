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
        self.setattr(aj["else"], "z:choose/z:if[@variable='volume']/z:group/z:choose/z:if[@variable='issue']/z:text", {"prefix": ", No. ", "suffix": None})
        self.setattr(aj["else"], "z:choose/z:if[@variable='volume']/z:group/z:choose/z:else/z:date", {"prefix": ", (", "suffix": ")"})
        
        # Volume
        self.setattr(aj["else"], "z:choose/z:if[@variable='volume']/z:text[@variable='volume']", {"prefix": " Vol. ", "suffix": None})
        self.setattr(aj["else"], "z:choose/z:if[@variable='volume']/z:group", {"prefix": None, "suffix": None})
        
        # Title
        t = self.conds["title"] 
        self.setattr(t["else"], "z:text", {"quotes":"false", "prefix": "“", "suffix":"”"})
        
        # Journal name
        t = self.conds["container-title"]
        self.setattr(t["else"], "z:group/choose/if/z:text", {"prefix":" ", "suffix":". "})
        
        # Date no parentheses
        c = self.conds["date"]
        self.setattr(c["else"], "z:group/z:date[@variable='original-date']", {"prefix": " ", "suffix": ". "})
        self.setattr(c["else"], "z:group/z:date[@variable='issued']", {"prefix": " ", "suffix": ". "})
        
        # Bibliography author
        c = self.conds["contributors"]
        self.setattr(c["else"], "z:names", {"suffix": ". "})
        self.setattr(c["else"], "z:names/z:name", {"initialize": "false", "and": "text"})
        self.setattr(c["else"], "z:names/z:label", {"form": None})
        
        # remove dot before "In"
        c = self.conds["container-contributors"]
        self.setattr(c["else"], "text", {"prefix": " "})
        self.setattr(c["else"], "z:group/z:names[@variable='editor translator']/z:name", {"and": "text", "initialize": "false", "name-as-sort-order": "all"})
    