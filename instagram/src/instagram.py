from instagram.data.config import *
from instagram.src.download.instagram_store import InstagramStore
from instagram.src.modify.instagram_monitor import InstagramMonitor

class Instagram:
    def __init__(self, monitoring_map):
        InstagramStore(monitoring_map)
        InstagramMonitor(monitoring_map)