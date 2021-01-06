from collections import defaultdict
from shutil import copyfile
import re
from instagram.src.modify.instagram_monitor import InstagramMonitor
from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.instagram_object import InstagramObject
from instagram.src.download.download_methods import login, random_sleep, pre_download, save_html, add_html_tags
from lxml import etree

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
        
url3 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/tagged/",
        "type": "tagged", "mode": "1", "monitoring_folder": "polizei.hannover/tagged/",
        "change": "", "notify": "", "err": ""}
monitoring_map["instagram"].append(url1)
monitoring_map["instagram"].append(url2)
monitoring_map["instagram"].append(url3)

ig = InstagramObject(url3, "new")
InstagramMonitor(monitoring_map)
