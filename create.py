from scripts.aerj import Aerj
c = Aerj(
        input  = 'scripts/source/chicago-author-date.csl', 
        journal = "Africa Educational Research Journal", 
        suffix = {"id": "aerj-ja", "title":"AERJ　（日本語）"}
    )
c.create()