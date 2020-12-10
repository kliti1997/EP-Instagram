from instagram.data.config import *
from instagram.src.helper import *
from instagram.src.modify.modify_methods import pre_modify, compare_posts, compare_followers_following, compare_igtv, compare_hover_items
#from instagram.src.instagram import Instagram

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        #Wir untersuchen nur noch die subdirectories fuer jede einzelne Anfrage:
        #Bspweise vergleichen wir nur die Posts Versionen miteinander, wenn auch der type Posts ist
        #Sonst kommt es zu mehrfachen Vergleichen, weil fuer jeden einzelne url('type=posts', 'type=igtv', 'type=tagged')
        #jedes mal alles durchgegangen wird(3*3=9 mal)
        for url in monitoring_map["instagram"]:
           
            html_type = get_type(url)
            old_html_path = get_old_html_path(url)
            new_html_path = get_new_html_path(url)

            print("compare ("+old_html_path+") with ("+new_html_path+")") 
            
            if not pre_modify(url):
                print("error while compare: "+old_html_path+" or "+new_html_path+"is missing")
                return
            
            compare_followers_following(url)

            if html_type == "posts":
                compare_posts(url)
            elif html_type == "igtv":
                compare_igtv(url)
            

            #compare_hover_items(url)

""" Circular import
if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
"""
