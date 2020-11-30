from instagram.data.config import *
#from instagram.src.instagram import Instagram

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        for url in monitoring_map["instagram"]:
            dirname = "instagram/data/files/"+url["id"]
            subdirectories = [x[0] for x in os.walk(dirname) if x[0] != dirname]

            oldExist = os.path.isfile(subdirectory+"/old.html")
            newExist = os.path.isfile(subdirectory+"/new.html")
 
            #Falls wir keine 2 Dateien haben muessen wir uns noch etwas ueberlegen
            #Z.B. wenn wir ein neuen User laden und erst nur einmal sein Profil gecheckt haben
            if not oldExist or not newExist:
                return 1

            print("compare ("+url["monitoring_folder"]+"old.html)"+" with ("+url["monitoring_folder"]+"new.html)")

            oldHtml = open(subdirectory+"/old.html", "r").read()
            oldHtml = html.unescape(oldHtml)

            newHtml = open(subdirectory+"/new.html", "r").read()
            newHtml = html.unescape(newHtml)
            
            #Verstehe nicht so recht warum die Post-Vergleichfunktion nicht hier aufgerufen wird
            #Warum wird sie direkt in der Definitionsdatei aufgerufen?

            compare_followers_following(oldHtml, newHtml)

            
""" Circular import
if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
"""