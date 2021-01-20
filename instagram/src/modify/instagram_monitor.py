"""
The module is responsible for the monitoring phase of the instagram monitor.
In case of changes, the module highlights these changes by calling functions in the modify_methods module.
"""
from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.modify.modify_methods import pre_modify, compare_posts, compare_followers_following, compare_igtv,compare_tagged, compare_hover_items, compare_stories
from instagram.src.instagram_object import InstagramObject

class InstagramMonitor:
    def __init__(self, monitoring_map):
        logger = logging.getLogger('instagram')
        logger.info("\n\n")
        logger.info("\t********MONITORING PHASE********")

        for url in monitoring_map["instagram"]:

            if not get_err(url):

                html_type = get_type(url)
                old_html_path = get_old_html_path(url)
                new_html_path = get_new_html_path(url)

                logger.info("compare ("+old_html_path+") with ("+new_html_path+")") 
                
                if not pre_modify(url):
                    logger.info("Error while modifying the html files.\n"+old_html_path+" or "+new_html_path+" is missing")
                    logger.info("You can ignore this, if this profile was loaded for the first time. Otherwise check missing html.")
                    set_change(url)
                    logger.debug(url)
                    continue
                try:
                    ig = (InstagramObject(url, "new"), InstagramObject(url, "old"))

                    compare_followers_following(url, ig)
                    compare_stories(url, ig)

                    if html_type == "posts":
                        compare_posts(url, ig)
                    elif html_type == "igtv":
                        compare_igtv(url, ig)
                    elif html_type == "tagged":
                        compare_tagged(url, ig)
                    compare_hover_items(url, ig)
                    logger.debug(url)
                except Exception as e:
                    eType = e.__class__.__name__
                    logger.error("Error while modifying the html files.\nException message: " + eType + ": " + str(e))
                    set_err(url)
                    continue
            
            else:
                logger.error("Skip modifying the html files of href: " + get_href(url) + ". [Download Error]")
                continue