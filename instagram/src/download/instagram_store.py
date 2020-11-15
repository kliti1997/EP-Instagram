from instagram.data.config import *
from instagram.src.download.instagram_methods import login, html_posts, html_igtv, html_tagged

class InstagramStore:
    def __init__(self, monitoring_map):
        print("\n\n\t************STORING PHASE************")
        login(ig_credentials["user"], ig_credentials["pass"])
        for url in monitoring_map["instagram"]:
            print("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            print("OR in " + url["monitorind_folder"] + "new.html")
            print("--------------------------------------------\n")
            #TODO sleep statements zufällig generieren
            html_posts(url)
            sleep(2)
            html_igtv(url)
            sleep(2)
            html_tagged(url)
            driver.quit()