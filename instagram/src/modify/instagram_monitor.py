from instagram.data.config import *
from instagram.src.instagram import Instagram

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        for url in monitoring_map["instagram"]:
            print("compare ("+url["monitoring_folder"]+"old.html)"+" with ("+url["monitoring_folder"]+"new.html)")

if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
