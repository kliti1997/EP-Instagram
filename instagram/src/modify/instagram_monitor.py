from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.modify.modify_methods import pre_modify, compare_posts, compare_followers_following, compare_igtv,compare_tagged, compare_hover_items, compare_stories
from instagram.src.instagram_object import InstagramObject

class InstagramMonitor:
    def __init__(self, monitoring_map):
        logger = logging.getLogger('instagram')
        logger.info("\n\n")
        logger.info("\t********MONITORING PHASE********")
        # We check only the subdirectories for every request. For example we check only the posts version
        # with each other when also the type Posts is. Otherwise there would be more compares
        # because for every url ('type=posts', 'type=igtv', 'type=tagged') every time everything would be compared.
        # 3 * 3 = 9 times

        for url in monitoring_map["instagram"]:

            html_type = get_type(url)
            old_html_path = get_old_html_path(url)
            new_html_path = get_new_html_path(url)

            logger.info("compare ("+old_html_path+") with ("+new_html_path+")") 
            
            if not pre_modify(url):
                logger.info("error while compare: "+old_html_path+" or "+new_html_path+" is missing")
                set_change(url)
                logger.debug(url)
                continue

            ig = (InstagramObject(url, "new"), InstagramObject(url, "old"))

            compare_followers_following(url, ig)
            compare_stories(url, ig)
            # TODO throws lsit index out of bounds exception compare_stories(url, ig)

            if html_type == "posts":
                compare_posts(url, ig)
            elif html_type == "igtv":
                compare_igtv(url, ig)
            elif html_type == "tagged":
                compare_tagged(url, ig)
            compare_hover_items(url, ig)
            logger.debug(url)

""" Circular import
if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
"""
