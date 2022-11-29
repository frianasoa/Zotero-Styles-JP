from scripts.aerj import Aerj
from scripts.jids import Jids
Aerj(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Africa Educational Research Journal", 
    suffix = {"id": "aerj-ja", "title":"AERJ　（日本語）"}
).create()

Jids(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal of International Development Studies", 
    suffix = {"id": "jids-ja", "title":"JIDS　（日本語）"}
).create()