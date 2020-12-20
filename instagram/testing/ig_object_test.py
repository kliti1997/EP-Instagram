from collections import defaultdict
from shutil import copyfile
import re
from instagram.src.download.instagram_store import InstagramStore
from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.instagram_object import InstagramObject
from instagram.src.download.download_methods import login, random_sleep, pre_download, save_html, add_html_tags
from lxml import etree

monitoring_map = defaultdict(list)
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        #"type": "posts", "mode": "1", "monitoring_folder": "./polizei.hannover/posts/",
        "type": "posts", "mode": "1", "monitoring_folder": "testfiles/polizei.hannover/posts/",
        "change": "", "notify": "", "err": ""}
        
url2 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "testfiles/polizei.hannover/igtv/",
        "change": "", "notify": "", "err": ""}
        
url3 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/tagged/",
        "type": "tagged", "mode": "1", "monitoring_folder": "testfiles/polizei.hannover/tagged/",
        "change": "", "notify": "", "err": ""}

ig = InstagramObject(url3, "new")
print(ig.__tostr__("tags"))
add_html_tags(url3["type"], ig)

ig.write(url3)
