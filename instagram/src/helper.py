from instagram.data.config import *

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
