"""
The module is responsible for the downloading phase. 
It saves the dom content of the instagram-subdirectory to be visited in an instagram class object, 
by calling further functions which are located in the instagram_monitor module.
"""
from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.download.download_methods import login, random_sleep, pre_download, save_html, add_html_tags
from instagram.src.helper import set_err
from instagram.src.instagram_object import InstagramObject
from instagram.src.download.profile_data import ProfileData
import datetime

MAX_RUNS = 10               #how often the programm should retry to download a profile, if an error occurs
"""
Determines how often the website should be revisited in case of connection issues.
"""

class InstagramStore:
    def __init__(self, monitoring_map):
        logger = logging.getLogger('instagram')
        logger.info("\n\n")
        logger.info("\t************STORING PHASE************\n")
        try:
            driver.get(base_url)
            random_sleep(6)
            login(ig_credentials["user"], ig_credentials["pass"])
        except:
            logger.error("Please check your internet connection.")

        for url in monitoring_map["instagram"]:
            ig = None
            logger.info("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            logger.info("OR in " + url["monitoring_folder"] + "new.html")
            logger.info("--------------------------------------------\n")
            
            try:
                init_return_values(url)
                for i in range(MAX_RUNS):
                    random_sleep(6)
                    content = save_html(url)
                    ig = InstagramObject(url, "new", content)
                    break

                pre_download(url)
                ig.write(url)

                initial = driver.execute_script("return window._sharedData;")
                profile = ProfileData(initial_data=initial, requests=driver.requests)
                add_html_tags(url, ig, profile)
                del driver.requests

            except Exception as e:
                eType = e.__class__.__name__
                logger.error("Error while downloading the html files.\nException message: " + eType + ": " + str(e))
                actual = config_folder + '/error_screenshots/' + str(datetime.datetime.now()) + '.png'      #only for debug in headless mode        #TODO REMOVE_MARKER
                driver.save_screenshot(actual)                                                                                                      #TODO REMOVE_MARKER
                set_err(url)
                continue

        driver.quit()
