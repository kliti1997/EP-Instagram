from collections import defaultdict
from instagram.src.download.instagram_store import InstagramStore
from instagram.src.helper import *
import time, sys

monitoring_map = defaultdict(list)
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        #"type": "posts", "mode": "1", "monitoring_folder": "./polizei.hannover/posts/",
        "type": "posts", "mode": "1", "monitoring_folder": "polizei.hannover/posts/",
        "change": "", "notify": "", "err": ""}
        
url2 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "polizei.hannover/igtv/",
        "change": "", "notify": "", "err": ""}
        
url3 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/tagged/",
        "type": "tagged", "mode": "1", "monitoring_folder": "polizei.hannover/tagged/",
        "change": "", "notify": "", "err": ""}

monitoring_map["instagram"].append(url1)
monitoring_map["instagram"].append(url2)
monitoring_map["instagram"].append(url3)

InstagramStore(monitoring_map)

tests = 0
succeed = 0

print("\n\t************TEST PHASE************")
for url in monitoring_map["instagram"]:
    folder_path = get_folder_path(url)
    old_html_path = get_old_html_path(url)
    new_html_path = get_new_html_path(url) 
    now = time.time()
    file_missing = False


    print("\nCurrently checking profile: " + url["id"])
    print("Currently checking type: " + url["type"])

    if os.path.exists(old_html_path):
        print("✔   old.html exists")
        old_html_time = os.stat(old_html_path).st_mtime
        tests += 1
        succeed += 1
    else:
        print("❌   old.html doesn't exists")
        file_missing = True
        tests += 1

    if os.path.exists(new_html_path):
        print("✔   new.html exists")
        new_html_time = os.stat(new_html_path).st_mtime
        tests += 1
        succeed += 1
    else:
        print("❌   new.html doesn't exists")
        file_missing = True
        tests += 1

    if not file_missing:
        if old_html_time < new_html_time:
            print("✔   new.html is newer than old.html")
            tests += 1
            succeed += 1
        else:
            print("❌   new.html is older than old.html")
            tests += 1

        if new_html_time > time.time() - 5 * 60:
            print("✔   new.html is not older than 5 minutes")
            tests += 1
            succeed += 1
        else:
            print("❌   new.html is older than 5 minutes")
            tests += 1
    else:
        print("❌   some tests were skipped, because new.html or old.html is missing.")

print("\nTest finished. Score: " + str(succeed) + "/" + str(tests))
if succeed == tests:
    print("✅   All tests succeed. Please manually check html too.\n")
else:
    print("❌   Some tests not succeed\n")

