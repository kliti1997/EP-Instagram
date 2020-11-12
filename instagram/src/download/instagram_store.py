from instagram.data.config import *

class InstagramStore:
    def __init__(self, monitoring_map):
        print("\n\n\t************STORING PHASE************")
        for url in monitoring_map["instagram"]:
            print("store the html code of : (" + url["href"] + ") in " + url["monitoring_folder"] + "old.html")
            print("OR in " + url["monitorind_folder"] + "new.html")
            print("--------------------------------------------\n")
            