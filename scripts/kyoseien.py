from .kyosei import Kyosei
import copy

class Kyoseien(Kyosei):
    def __init__(self, input, journal, suffix, doclinks):
        super().__init__(input, journal, suffix, doclinks)
    
    def custom(self):
        super().custom()
        
        # Removing all full-width parentheses
        locators = self.conds["locator-bill-etc"]
        self.setattr(locators["if"], "z:group/z:group/z:number", {"prefix" : " (", "suffix": ") "})
        
        # Citation
        self.setattr(self.citation, "z:layout", {"prefix" : " (", "suffix": ") "})
        
        # access
        access = self.conds["access"]
        self.setattr(access["else"], "z:choose/z:if/z:choose/z:else/date", {"prefix" : " (Last accessed ", "suffix": ") "})
        self.setattr(access["if"], "z:choose/z:if/z:choose/z:else/date", {"prefix" : " (Last accessed ", "suffix": ") "})
        
        #title
        title = self.conds["title-2"]
        self.setattr(title["if"], "z:group", {"prefix" : " (", "suffix": ") "})
        
        #Edition
        edition = self.conds["edition"]
        self.setattr(edition["if"], "z:text", {"prefix" : " (", "suffix": ") "})
        
        