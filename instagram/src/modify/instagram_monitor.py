from EP-Instagramm-1/data/config.py import *

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        for url in monitoring_map["instagram"]:
            print("compare ("+url["monitoring_folder"]+"old.html)"+" with ("+url["monitoring_folder"]+"new.html)")

if __name__ == "__main__":
    monitoring_map = defaultdict(list)
    url1 = {"id":"polizei.hannover",
        "href":"https://www.instagram.com/polizei.hannover/",
        "type":"posts","mode":"1","monitoring_folder":"./polizei.hannover/posts/",
        "change":"","notify":"","err":""}
    #url2 = {"id":"polizei.hannover",
    #    "href":"https://www.instagram.com/polizei.hannover/channel",
    #    "type":"IGTV","mode":"1","monitoring_folder":"./polizei.hannover/IGTV/",
    #    "change":"","notify":"","err":""}
    monitoring_map["instagram"].append(url1)
    #monitoring_map["instagram"].append(url2)
    Instagram(monitoring_map)
    print("\n\n")
