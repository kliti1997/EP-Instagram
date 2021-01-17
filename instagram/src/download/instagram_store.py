"""
The module is responsible for the downloading phase. 
It saves the dom content of the instagram-subdirectory to be visited in an instagram class object, 
by calling further functions which are located in the instagram_monitor module.
"""
from instagram.src.helper import *
from instagram.src.download.download_methods import login, random_sleep, pre_download, save_html, add_html_tags, delete_new_html
from instagram.src.helper import set_err
from instagram.src.instagram_object import InstagramObject
from instagram.src.download.profile_data import ProfileData
import datetime

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
            init_return_values(url)
            actual_phase = 0
            
            for i in range(MAX_RUNS):
                try:
                    #Download-Phase 1
                    actual_phase = 1
                    random_sleep(6)
                    content = save_html(url)
                    ig = InstagramObject(url, "new", content)
                    validate_obj(ig, url)
                    
                    #Download-Phase 2
                    actual_phase = 2
                    pre_download(url)
                    ig.write(url)

                    #Download-Phase 3
                    actual_phase = 3
                    initial = driver.execute_script("return window._sharedData;")
                    profile = ProfileData(initial_data=initial, requests=driver.requests)
                    
                    add_html_tags(url, ig, profile)
                    del driver.requests
                    break
                except Exception as e:
                    logger.info("Download-Try: " + str(i + 1) + " of " + str(MAX_RUNS) + " failed in Phase " + str(actual_phase) + ".")
                    delete_new_html(url)
                    if i >= MAX_RUNS - 1:
                        eType = e.__class__.__name__
                        logger.error("Error while downloading the html files.\nException message: " + eType + ": " + str(e))
                        set_err(url)
                        actual = config_folder + '/error_screenshots/' + str(datetime.datetime.now()) + '.png'      #only for debug in headless mode        #TODO REMOVE_MARKER
                        driver.save_screenshot(actual)                                                                                                      #TODO REMOVE_MARKER

        driver.close()