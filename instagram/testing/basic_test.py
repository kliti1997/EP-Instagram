from collections import defaultdict
from instagram.src.download.instagram_store import InstagramStore
from instagram.src.modify.instagram_monitor import InstagramMonitor
import logging

logger = logging.getLogger('basic_test')

monitoring_map = defaultdict(list)
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        "type": "posts", "mode": "2", "monitoring_folder": "polizei.hannover/posts/",
        "change": "", "notify": "", "err": ""}      
url2 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "polizei.hannover/igtv/",
        "change": "", "notify": "", "err": ""}        
url3 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/tagged/",
        "type": "tagged", "mode": "1", "monitoring_folder": "polizei.hannover/tagged/",
        "change": "", "notify": "", "err": ""}
url4 = {"id": "frieda_rudi_make_oink",
        "href": "https://www.instagram.com/frieda_rudi_make_oink/",
        "type": "posts", "mode": "1", "monitoring_folder": "frieda_rudi_make_oink/posts/",
        "change": "", "notify": "", "err": ""}
        
monitoring_map["instagram"].append(url1)
monitoring_map["instagram"].append(url2)
monitoring_map["instagram"].append(url3)
monitoring_map["instagram"].append(url4)

logger.info("\t\t{{{BASIC TEST}}}")

InstagramStore(monitoring_map)
InstagramMonitor(monitoring_map)

logger.info("\t\t{{{RESULT}}}")
for url in monitoring_map["instagram"]:
    logger.info("ID:\t" + url["id"])
    logger.info("Type:\t" + url["type"])
    logger.info("Mode:\t" + url["mode"])
    logger.info("Change:\t" + str(url["change"]))
    logger.info("Notify:\t" + str(url["notify"]))
    logger.info("Error:\t" + str(url["err"]) + "\n")