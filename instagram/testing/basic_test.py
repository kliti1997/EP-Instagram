from collections import defaultdict
from instagram.src.download.instagram_store import InstagramStore

monitoring_map = defaultdict(list)
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        #"type": "posts", "mode": "1", "monitoring_folder": "./polizei.hannover/posts/",
        "type": "posts", "mode": "1", "monitoring_folder": "polizei.hannover/posts/",
        "change": "", "notify": "", "err": ""}
        
url2 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "polizei.hannover/igtv/",
        "change": "", "notify": "", "err": ""}

monitoring_map["instagram"].append(url1)
monitoring_map["instagram"].append(url2)

InstagramStore(monitoring_map)