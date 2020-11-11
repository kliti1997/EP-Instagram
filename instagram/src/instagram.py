from instagram/data/config.py import *
from instagram/src/download/instagram_store.py import *
from instagram/src/modify/instagram_modify.py import *

class Instagram:
    def __init__(self, monitoring_map):
        InstagramStore(monitoring_map)
        InstagramMonitor(monitoring_map)