from scripts.aerj import Aerj
from scripts.jids import Jids
from scripts.jidsen import JidsEn
from scripts.kyosei import Kyosei
from scripts.kyoseien import Kyoseien
from scripts.kyoso import Kyoso
from scripts.iczemi import ICZemi

Aerj(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Africa Educational Research Journal", 
    suffix = {"id": "aerj-ja", "title":"AERJ　（日本語）", "language": "Japanese"},
    doclinks = [
        "https://www.japan-society-for-africa-educational-research.org/app/download/8289809356/AERJ12.pdf"
    ]
).create()

Jids(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal of International Development Studies", 
    suffix = {"id": "jids-ja", "title":"JIDS　（日本語）", "language": "Japanese"},
    doclinks = [
        "https://drive.google.com/file/d/1VAu6cAs5beGPgYpwNwfOXISZgXEaOKnL/view",
        "https://drive.google.com/file/d/1M0SKuOO7Bi_vsBWZ98cW99kGKXXwst-Y/view",
    ]
).create()

JidsEn(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal of International Development Studies", 
    suffix = {"id": "jids-en", "title":"JIDS (English)", "language": "English"},
    doclinks = [
        "https://drive.google.com/file/d/1VAu6cAs5beGPgYpwNwfOXISZgXEaOKnL/view",
        "https://drive.google.com/file/d/1M0SKuOO7Bi_vsBWZ98cW99kGKXXwst-Y/view",
    ]
).create()

Kyosei(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal of Kyosei Studies", 
    suffix = {"id": "kyosei-ja", "title":"OU Kyosei Studies　（日本語）", "language": "Japanese"},
    doclinks = [
        "http://kyosei.hus.osaka-u.ac.jp/wp-content/uploads/2021/07/3505fd795307005aa71cd3a930f2557a.pdf"
    ]
).create()

Kyoseien(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal of Kyosei Studies", 
    suffix = {"id": "kyosei-en", "title":"OU Kyosei Studies (English)", "language": "English"},
    doclinks = [
        "http://kyosei.hus.osaka-u.ac.jp/wp-content/uploads/2021/07/3505fd795307005aa71cd3a930f2557a.pdf"
    ]
).create()

Kyoso(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Journal - Mirai Kyoso", 
    suffix = {"id": "kyoso-ja", "title":"KYOSO　（日本語）", "language": "Japanese"},
    doclinks = [
        "http://www.hus.osaka-u.ac.jp/mirai-kyoso/ja/journal/mirai-kyoso-journaltoko_11.pdf"
    ]
).create()

ICZemi(
    input  = 'scripts/source/chicago-author-date.csl', 
    journal = "Osaka University - International Collaboration and Development Studies", 
    suffix = {"id": "iczemi-ja", "title":"IC Zemi　（日本語）", "language": "Japanese"},
    doclinks = [
        "https://drive.google.com/file/d/1ZsYZXG98x1zHz4VdmBgeqyGlYDkyU8nD"
    ]
).create()