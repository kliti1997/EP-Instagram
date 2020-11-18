from collections import defaultdict
from instagram.src.download.instagram_store import InstagramStore

monitoring_map = defaultdict(list)
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        "type": "posts", "mode": "1", "monitoring_folder": "./polizei.hannover/posts/",
        "change": "", "notify": "", "err": ""}
monitoring_map["instagram"].append(url1)

InstagramStore(monitoring_map)