from instagram.data.config import *
from instagram.src.download.instagram_methods import login, html_posts

class InstagramStore:
    def __init__(self, monitoring_map):
        print("\n\n\t************STORING PHASE************")
        login(ig_credentials["user"], ig_credentials["pass"])
        print("map")
        print(monitoring_map)
        for url in monitoring_map["instagram"]:
            print("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            print("OR in " + url["monitorind_folder"] + "new.html")
            print("--------------------------------------------\n")
