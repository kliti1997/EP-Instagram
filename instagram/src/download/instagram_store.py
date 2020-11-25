"""
The module containts the class InstagramStore, which performs the download of different instagram
subpages. 
The "posts", "tagged" and the "IGTV" subpages will be downloaded and saved to a html file for further 
investigation.
"""
from instagram.data.config import *
from instagram.src.download.instagram_methods import login, random_sleep, pre_download, save_html

class InstagramStore:
    def __init__(self, monitoring_map):
        print("\n\n\t************STORING PHASE************")

        try:
            login(ig_credentials["user"], ig_credentials["pass"])
        except Exception as e:
            logger.error("performing the login process.\nException message: " + str(e))

        for url in monitoring_map["instagram"]:
            print("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            print("OR in " + url["monitoring_folder"] + "new.html")
            print("--------------------------------------------\n")
            
            try:
                save_html(url)
            except Exception as e:
                logger.error("downloading the html files.\nException message: " + str(e))
            random_sleep(10)

        driver.quit()
