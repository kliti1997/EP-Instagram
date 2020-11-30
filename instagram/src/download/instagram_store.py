from instagram.data.config import *
from instagram.src.download.instagram_methods import login, random_sleep, pre_download, save_html, compare_posts

class InstagramStore:
    def __init__(self, monitoring_map):
        print("\n\n\t************STORING PHASE************")
        login(ig_credentials["user"], ig_credentials["pass"])
        for url in monitoring_map["instagram"]:
            print("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            print("OR in " + url["monitoring_folder"] + "new.html")
            print("--------------------------------------------\n")
            
            try:
                save_html(url)
            except Exception as e:
                logger.error("downloading the html files.\nException message: " + str(e))

        driver.quit()