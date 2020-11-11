from instagram.data.config import *

class InstagramStore:
    #substr_list := [substr, substr_ending_token]
    #Zum Beispiel: ['href="/', '"']
    #Wir suchen also einen link "/static/test/trash.css" und wissen, dass dieser
    #als 'href="/static/test/trash.css"' im Code eingebettet ist. Der String beginnt mit 'href="/' und 
    #endet mit '"'

    #link_list := [link_name, link_beg_pos, link_end_pos]
    def findAdditionals(self, page, substr_list, link_list):
        return None

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