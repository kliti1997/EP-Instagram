from collections import defaultdict
from instagram.src.instagram import Instagram
import logging

logger = logging.getLogger('testing')

monitoring_map = defaultdict(list)
url1 = {"id": "ulferdowoff",
        "href": "https://www.instagram.com/ulferdowoff/",
        "type": "posts", "mode": "1", "monitoring_folder": "ulferdowoff/posts/",
        "change": "", "notify": "", "err": ""}      
url2 = {"id": "ulferdowoff",
        "href": "https://www.instagram.com/ulferdowoff/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "ulferdowoff/igtv/",
        "change": "", "notify": "", "err": ""}        
url3 = {"id": "ulferdowoff",
        "href": "https://www.instagram.com/ulferdowoff/tagged/",
        "type": "tagged", "mode": "2", "monitoring_folder": "ulferdowoff/tagged/",
        "change": "", "notify": "", "err": ""}
        
monitoring_map["instagram"].append(url1)
monitoring_map["instagram"].append(url2)
monitoring_map["instagram"].append(url3)

logger.info("\t\t{{{BASIC TEST}}}")

Instagram(monitoring_map)

logger.info("\t\t{{{RESULT}}}")
for url in monitoring_map["instagram"]:
    logger.info("ID:\t" + url["id"])
    logger.info("Type:\t" + url["type"])
    logger.info("Mode:\t" + url["mode"])
    logger.info("Change:\t" + str(url["change"]))
    logger.info("Notify:\t" + str(url["notify"]))
    logger.info("Error:\t" + str(url["err"]) + "\n")