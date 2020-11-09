from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from time import sleep

url = "https://www.instagram.com/jimmyfallon/"
base_url = "https://www.instagram.com/"

geckodriver = "/Users/timo/node_modules/geckodriver/geckodriver"
driver = webdriver.Firefox(executable_path = geckodriver)
driver.get(url)

# Auf Englisch kann es Accept heißen
driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
driver.find_element_by_class_name("dCJp8").click()
sleep(2)
content = driver.page_source
soup = BeautifulSoup(content)
driver.close()


for img in soup.find_all("img", src=True):
    if not img["src"].startswith('http'):
        img["src"] = urljoin(base_url, img["src"])

for img in soup.find_all("img", srcset=True):
    if not img["srcset"].startswith('http'):
        img["srcset"] = urljoin(base_url, img["srcset"])

for a in soup.find_all("a"):
    if not a["href"].startswith("http"):
        a["href"] = urljoin(base_url, a["href"])

for link in soup.find_all("link"):
    if not link["href"].startswith('http'):
        link["href"] = urljoin(base_url, link["href"])

i = 0
for script in soup.find_all("script", src=True):
    if not script["src"].startswith('http'):
        i += 1
        if i == 4: 
            # Dieses script wird ausgeschlossen, weil dadurch die Seite ständig refreshed wird.
            #<script crossorigin="anonymous" src="/static/bundles/es6/Vendor.js/c911f5848b78.js" type="text/javascript"></script>
            continue
        script["src"] = urljoin(base_url, script["src"])

f = open("insta.html", "w")
f.write(soup.prettify())
f.close()