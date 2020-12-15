from instagram.data.config import *
from instagram.src.instagram_objects import InstagramObjects

# Wird später entfernt. Wird mit den Objekten von Instagram in
# der download Phase initialisiert.
ig_objs = None

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
