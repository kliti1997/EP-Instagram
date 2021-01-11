from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.download.download_methods import login, random_sleep, pre_download, save_html, add_html_tags
from instagram.src.helper import set_err
from instagram.src.instagram_object import InstagramObject
from instagram.src.download.profile_data import ProfileData

MAX_RUNS = 10

class InstagramStore:
    def __init__(self, monitoring_map):
        logger = logging.getLogger('instagram')
        logger.info("\n\n")
        logger.info("\t************STORING PHASE************\n")
        driver.get(base_url)
        random_sleep(5)
        login(ig_credentials["user"], ig_credentials["pass"])

        for url in monitoring_map["instagram"]:
            ig = None
            logger.info("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            logger.info("OR in " + url["monitoring_folder"] + "new.html")
            logger.info("--------------------------------------------\n")

            for i in range(MAX_RUNS):
                try:
                    init_return_values(url)
                    random_sleep(5)
                    content = save_html(url)
                    ig = InstagramObject(url, "new", content)
                    break
                except Exception as e:
                    eType = e.__class__.__name__
                    logger.error("downloading the html files.\nException message: " + eType + ": " + str(e))
                    set_err(url)
                    if i == MAX_RUNS - 1:
                        driver.quit()
                        url["err"] = True
                        exit(1)
                    continue

            pre_download(url)
            ig.write(url)

            initial = driver.execute_script("return window._sharedData;")
            profile = ProfileData(initial_data=initial, requests=driver.requests)
            add_html_tags(url, ig, profile)

        driver.quit()
