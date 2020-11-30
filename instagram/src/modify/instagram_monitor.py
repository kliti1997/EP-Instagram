from instagram.data.config import *
from instagram.src.download.instagram_methods import compare_followers_following
#from instagram.src.instagram import Instagram

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        for url in monitoring_map["instagram"]:
            dirname = "instagram/data/files/"+url["id"]
            #TODO name error fixen (subdirectory -> subdirectories)
            """
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
            """

            #TODO entfernen, nachdem name errors oben gefixt worden sind
            try:
                compare_followers_following("/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/data/files/polizei.hannover/posts/posts_old.html", "/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/data/files/polizei.hannover/posts/posts.html")
                compare_followers_following("/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/data/files/polizei.hannover/igtv/igtv_old.html", "/Users/timo/Documents/Uni/SP/EP-Instagramm-1/instagram/data/files/polizei.hannover/igtv/igtv.html")
            except Exception as e:
                eType = e.__class__.__name__
                logger.error("comparing the html files.\nException message: " + eType + ": " + str(e))
""" Circular import
if __name__ == "__main__":
    Instagram(monitoring_map)
    print("\n\n")
"""