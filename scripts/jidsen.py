from .jids import Jids

class JidsEn(Jids):
    def __init__(self, input, journal, suffix, doclinks):
        super().__init__(input, journal, suffix, doclinks)
    
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
        self.setattr(self.citation, "z:layout/z:group/z:choose/z:if/z:group/z:text[@macro='contributors-short']", {"suffix":", "})
        self.setattr(self.citation, "z:layout", {"prefix": "(", "suffix": ")"})
    
    def custom(self):
        super().custom()
        
        # Clean bibliography layout
        self.delelement(self.bibliography, "z:layout/choose")
        self.render({"tag": "text", "attrib": {"value": "."}}, self.bibliography.xpath("z:layout", namespaces=self.ns)[0])
        
        # Remove all conditions to leave only English
        self.revertconditions(keeptag="else")