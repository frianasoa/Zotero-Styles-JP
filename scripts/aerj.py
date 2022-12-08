from .chicago import Chicago

class Aerj(Chicago):
    def __init__(self, input, journal, suffix):
        super().__init__(input, journal, suffix)
    
    def custom(self):        
        suffix = {"if": {"tag":"text", "attrib": {"value":"頁"}}, "else": {}}
        prefix = {"if": {}, "else": {"tag":"label", "attrib": {"variable": "locator", "form": "short", "suffix":" "}}}
        self.shortpagelabel(prefix=prefix, suffix=suffix)