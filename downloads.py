from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from collections import defaultdict
import time


class Instagram:
    def __init__(self, monitoring_map):
        InstagramStore(monitoring_map)
        InstagramMonitor(monitoring_map)

class InstagramStore:
    #substr_list := [substr, substr_ending_token]
    #Zum Beispiel: ['href="/', '"']
    #Wir suchen also einen link "/static/test/trash.css" und wissen, dass dieser
    #als 'href="/static/test/trash.css"' im Code eingebettet ist. Der String beginnt mit 'href="/' und 
    #endet mit '"'

    #link_list := [link_name, link_beg_pos, link_end_pos]
    def findAdditionals(self, page, substr_list, link_list):
        first_substr_ending_token = ""
        first_substr_beg = -1
        first_substr_end = -1
        former_position = -1
        while True:
            find_first = 9999999999
            for substr, substr_ending_token in substr_list:
                pos_beg = page.find(substr, first_substr_beg+1)
                if pos_beg != -1:
                    pos_beg += len(substr)
                if find_first > pos_beg and pos_beg != -1:
                    find_first = pos_beg
                    first_substr_ending_token = substr_ending_token
            first_substr_beg = find_first
            if first_substr_beg < former_position or first_substr_beg == -1 or find_first == 9999999999:
                break
            first_substr_end = page.find(first_substr_ending_token, first_substr_beg)
            if first_substr_beg == first_substr_end:
                first_substr_beg = first_substr_beg-1
            #print(page[first_substr_beg : first_substr_end])
            link_list.append([page[first_substr_beg : first_substr_end], first_substr_beg, first_substr_end])
            former_position = first_substr_beg
            first_substr_beg = first_substr_end

    def downloadAdditionals(self, driver, link_list, destination_directory):
        links = [link_triple[0] for link_triple in link_list]
        for link in links:
            former_position = -1
            divider_position = -1
            while True:
                former_position = divider_position
                divider_position = link.find("/", divider_position+1)
                if divider_position == -1:
                    break
            name = link[former_position+1 : ]
            if ".css" in name or ".js" in name or ".json" in name:
                driver.get("https://instagram.com/" + link)
                f = open(destination_directory + "/" + name, "w")
                f.write(driver.page_source)

    def __init__(self, monitoring_map):
        options = Options()
        options.headless = True
        options.binary_location = '/usr/bin/firefox-esr'
        serv = Service('./driver/geckodriver')
        driver = webdriver.Firefox(service=serv, options=options)
        print("\n\n\t********STORING PHASE********")
        for url in monitoring_map["instagram"]:
            print("store the html code of : ("+url["href"]+ ") in "+url["monitoring_folder"]+"old.html")
            print("OR in "+url["monitoring_folder"]+"new.html")
            print("-----------------------------\n")
            driver.get(url["href"])
            
            f = open(url["monitoring_folder"]+"new.html", "w")
            f.write(driver.page_source)
            #page = driver.page_source
            page = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            page_size = len(page)
            
            substr_list = [["href=\"/", "\""], ["src=\"/", "\""], [":\"/", "\""]]
            links = []
            self.findAdditionals(page, substr_list, links)
            self.downloadAdditionals(driver, links, url["monitoring_folder"] + "AdditionalsNew")
        driver.quit()

class InstagramMonitor:
    def __init__(self, monitoring_map):
        print("\n\n\t********MONITORING PHASE********")
        for url in monitoring_map["instagram"]:
            print("compare ("+url["monitoring_folder"]+"old.html)"+" with ("+url["monitoring_folder"]+"new.html)")

if __name__ == "__main__":
    monitoring_map = defaultdict(list)
    url1 = {"id":"polizei.hannover",
        "href":"https://www.instagram.com/polizei.hannover/",
        "type":"posts","mode":"1","monitoring_folder":"./polizei.hannover/posts/",
        "change":"","notify":"","err":""}
    #url2 = {"id":"polizei.hannover",
    #    "href":"https://www.instagram.com/polizei.hannover/channel",
    #    "type":"IGTV","mode":"1","monitoring_folder":"./polizei.hannover/IGTV/",
    #    "change":"","notify":"","err":""}
    monitoring_map["instagram"].append(url1)
    #monitoring_map["instagram"].append(url2)
    Instagram(monitoring_map)
    print("\n\n")
