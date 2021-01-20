"""
This module has different getters und setter helper methods which we use to read different information and set
the values for notify, error and change in the monitoring map.
"""
from instagram.data.config import *

logger = logging.getLogger('instagram')

def get_folder_path(url):
    return os.path.join(monitoring_folder, url["monitoring_folder"])
    
def get_new_html_path(url):
    return os.path.join(monitoring_folder, url["monitoring_folder"], "new.html")

def get_old_html_path(url):
    return os.path.join(monitoring_folder, url["monitoring_folder"], "old.html")

def get_href(url):
    return str(url["href"])

def get_type(url):
    return str(url["type"])

def get_mode(url):
    return str(url["mode"])
    
def init_return_values(url):
    url["change"] = False
    url["notify"] = False
    url["err"] = False

def set_change(url):
    url["change"] = True

def set_notify(url):
    url["notify"] = True

def set_err(url):
    url["change"] = False
    url["notify"] = False
    url["err"] = True
    logger.error('Error while processing. URL: ' + get_href(url))

def get_err(url):
    return url["err"]
