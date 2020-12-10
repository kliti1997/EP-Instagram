from collections import defaultdict
from instagram.src.download.instagram_store import InstagramStore
from instagram.src.modify.instagram_monitor import InstagramMonitor
from instagram.src.modify.modify_methods import compare_hover_items as cmp


monitoring_map = defaultdict(list)
#monitoring_folder = "/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/testing/hover"
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        #"type": "posts", "mode": "1", "monitoring_folder": "./polizei.hannover/posts/",
        "type": "posts", "mode": "1", "monitoring_folder": "/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/testing/hover/posts/",
        "change": "", "notify": "", "err": ""}
        
url2 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/testing/hover/igtv",
        "change": "", "notify": "", "err": ""}
        
url3 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/tagged/",
        "type": "tagged", "mode": "1", "monitoring_folder": "/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/testing/hover/tagged",
        "change": "", "notify": "", "err": ""}
cmp(url1)