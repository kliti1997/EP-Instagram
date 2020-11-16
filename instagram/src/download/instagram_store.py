from instagram.data.config import *
from instagram.src.download.instagram_methods import login, html_posts, html_igtv, html_tagged, random_sleep

class InstagramStore:
    def __init__(self, monitoring_map):
        print("\n\n\t************STORING PHASE************")
        login(ig_credentials["user"], ig_credentials["pass"])
        for url in monitoring_map["instagram"]:
            print("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            print("OR in " + url["monitorind_folder"] + "new.html")
            print("--------------------------------------------\n")

            html_posts(url)
            random_sleep(10)
            html_igtv(url)
            random_sleep(10)
            html_tagged(url)
            driver.quit()