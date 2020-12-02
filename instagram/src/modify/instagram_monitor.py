from instagram.data.config import *
from instagram.src.modify.modify_methods import compare_posts, compare_followers_following, compare_igtv
#from instagram.src.instagram import Instagram

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        #Wir untersuchen nur noch die subdirectories fuer jede einzelne Anfrage:
        #Bspweise vergleichen wir nur die Posts Versionen miteinander, wenn auch der type Posts ist
        #Sonst kommt es zu mehrfachen Vergleichen, weil fuer jeden einzelne url('type=posts', 'type=igtv', 'type=tagged')
        #jedes mal alles durchgegangen wird(3*3=9 mal)
        for url in monitoring_map["instagram"]:
            dirname = "./instagram/data/files/"+url["id"]+"/"+url["type"]
                
            oldExist = os.path.isfile(dirname+"/old.html")
            newExist = os.path.isfile(dirname+"/new.html")
 
            #Falls wir keine 2 Dateien haben muessen wir uns noch etwas ueberlegen
            #Z.B. wenn wir ein neuen User laden und erst nur einmal sein Profil gecheckt haben
            if not oldExist or not newExist:
                return

            print("compare ("+url["monitoring_folder"]+"old.html)"+" with ("+url["monitoring_folder"]+"new.html)")
            
            oldHtml = open(dirname+"/old.html", "r").read()
            newHtml = open(dirname+"/new.html", "r").read()
            
            outputHtml = compare_followers_following(oldHtml, newHtml)
            open(dirname+"/new.html", "wb").write(outputHtml)

""" Circular import
if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
"""
