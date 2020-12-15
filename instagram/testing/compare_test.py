from collections import defaultdict
from shutil import copyfile
import re
from instagram.src.modify.instagram_monitor import InstagramMonitor
from instagram.data.config import *
from instagram.src.helper import *

driver.quit()

monitoring_map = defaultdict(list)
url1 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/",
        #"type": "posts", "mode": "1", "monitoring_folder": "./polizei.hannover/posts/",
        "type": "posts", "mode": "1", "monitoring_folder": "testfiles/polizei.hannover/posts/",
        "change": "", "notify": "", "err": ""}
        
url2 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/channel/",
        "type": "igtv", "mode": "1", "monitoring_folder": "testfiles/polizei.hannover/igtv/",
        "change": "", "notify": "", "err": ""}
        
url3 = {"id": "polizei.hannover",
        "href": "https://www.instagram.com/polizei.hannover/tagged/",
        "type": "tagged", "mode": "1", "monitoring_folder": "testfiles/polizei.hannover/tagged/",
        "change": "", "notify": "", "err": ""}

monitoring_map["instagram"].append(url1)
monitoring_map["instagram"].append(url2)
monitoring_map["instagram"].append(url3)


print("\n\t************PRE-TEST PHASE************")
for url in monitoring_map["instagram"]:
    folder_path = get_folder_path(url)
    old_html_path = get_old_html_path(url)
    new_html_path = get_new_html_path(url)
    compare_test_old = os.path.join(folder_path, "compare_test_old.html")
    compare_test_new = os.path.join(folder_path, "compare_test_new.html")

    if os.path.exists(old_html_path):
        os.remove(old_html_path)
    if os.path.exists(new_html_path):
        os.remove(new_html_path)
    if os.path.exists(compare_test_old):
        copyfile(compare_test_old, old_html_path)
        print(old_html_path + ' overwritten.')
    if os.path.exists(compare_test_new):
        copyfile(compare_test_new, new_html_path)
        print(new_html_path + ' overwritten.')


InstagramMonitor(monitoring_map)


def border_counter(html_file) -> int:
    with open(str(html_file)) as f:
        html = f.read()
        counter = html.count('border: 4px solid green;')

    return counter


print("\n\t************TEST PHASE************")
tests_passed = True
for url in monitoring_map["instagram"]:
    folder_path = get_folder_path(url)
    new_html_path = get_new_html_path(url)
    expected_new_html = os.path.join(folder_path, "compare_expected_new.html")

    borders = border_counter(new_html_path)
    expected_borders = border_counter(expected_new_html)

    print("    Found borders " + str(borders) + " borders after compare.")
    print("    Expected borders " + str(expected_borders) + ".")

    if borders == expected_borders:
        print("[SUCCESS]   Compare test succeed.\n")
    else:
        print("[FAILURE]   Compare test not succeed in file: " + new_html_path + "\n")
        tests_passed = False

if tests_passed:
    print("[SUCCESS]   All tests succeeded. Please manually check html too.\n")
else:
    print("[FAILURE]   Some tests did not succeed\n")
