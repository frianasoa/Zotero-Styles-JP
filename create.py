from scripts.aerj import Aerj
from scripts.jids import Jids
from scripts.kyosei import Kyosei
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

Kyosei(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal of Kyosei Studies", 
    suffix = {"id": "kyosei-ja", "title":"KYOSEI　（日本語）"}
).create()