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
    url["err"] = True
