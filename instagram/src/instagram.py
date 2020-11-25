"""
The module contains the class Instagram, which does the whole monitoring process.

The monitoring process is divided into the storing phase and the monitoring phase,
which are implemented in the classes InstagramStore, respectively InstagramMonitor.
"""
from instagram.data.config import *
from instagram.src.download.instagram_store import InstagramStore
from instagram.src.modify.instagram_monitor import InstagramMonitor


class Instagram:
    def __init__(self, m_map):
        InstagramStore(m_map)
        InstagramMonitor(m_map)
