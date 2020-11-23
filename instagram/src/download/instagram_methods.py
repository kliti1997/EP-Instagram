import re
import os
from instagram.data.config import *
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from pprint import pprint
from lxml import etree, html
from pathlib import Path


# Loggt sich auf Instagram ein.
def login(username, password):
    driver.get(login_url)
    random_sleep(5)
    cookie_consent()
    random_sleep(5)

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)

    try:  # Existiert as Element auf englisch?
        driver.find_element_by_xpath("//*[text()='Log In']").click()
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath("//*[text()='Anmelden']").click()
        except NoSuchElementException:
            raise RuntimeError

    random_sleep(10)

    if "onetap" in driver.current_url:  # "Save your Login?"-Page
        try:  # Existiert as Element auf englisch?
            driver.find_element_by_xpath("//*[text()='Save Info']").click()
        except NoSuchElementException:
            try:
                driver.find_element_by_xpath("//*[text()='Informationen speichern']").click()
            except NoSuchElementException:
                raise RuntimeError

    random_sleep(10)


# Ggf. das cookie consent Fenster akzeptieren.
def cookie_consent():
    try:  # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
    except NoSuchElementException:  # Existiert es auf englisch?
        try:
            driver.find_element_by_xpath("//*[text()='Accept']").click()
        except NoSuchElementException:
            pass


# Ändert die relativen links aller img, a und link tags, indem es die
# base_url an die relativen Pfade anhängt.
def convert_links(source):
    """for img in soup.find_all("img", src=True):
        if not img["src"].startswith("http"):
            img["src"] = urljoin(base_url, img["src"])

    for img in soup.find_all("img", srcset=True):
        if not img["srcset"].startswith("http"):
            img["srcset"] = urljoin(base_url, img["srcset"])

    for a in soup.find_all("a"):
        if not a["href"].startswith("http"):
            a["href"] = urljoin(base_url, a["href"])

    for link in soup.find_all("link"):
        if not link["href"].startswith("http"):
            link["href"] = urljoin(base_url, link["href"])"""

    return re.sub(r'(href="|src="|srcset="|:")/', r'\1' + base_url, source)


# Lade den Html-Code der Beiträge-Seite herunter.
def save_html(url):
    type = str(url["type"])
    link = str(url["href"])
    if type != 'posts':
        link += type
    driver.get(link)
    random_sleep(10)
    content = convert_links(driver.execute_script("return new XMLSerializer().serializeToString(document);"))
    print(content)
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(content, etree.HTMLParser())

    pre_download(url)
    with open(os.path.join(monitoring_folder, url["monitoring_folder"], type + ".html"), "w") as f:
        f.write(content)


def random_sleep(max_time):
    # set arbitrary minimum sleep time
    min_time = 3
    if max_time < min_time:
        max_time = min_time + 10
    random_time = randint(3, max_time)
    sleep(random_time)


def pre_download(url):
    folder = os.path.join(monitoring_folder, url["monitoring_folder"])
    type = str(url["type"])
    filepath = os.path.join(monitoring_folder, url["monitoring_folder"], type + ".html")
    oldFilepath = os.path.join(monitoring_folder, url["monitoring_folder"], type + "_old.html")

    Path(folder).mkdir(parents=True, exist_ok=True)
        
    if os.path.exists(oldFilepath):        
        os.remove(oldFilepath)
    if os.path.exists(filepath):
        os.rename(filepath, oldFilepath)


def compare_posts():
    old_html_url = "instagram/data/files/polizei.hannover/posts/posts_old.html"
    new_html_url = "instagram/data/files/polizei.hannover/posts/posts.html"
    # TODO Zur richtige Verzeichnis wechseln, muss noch geaendert werden
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")

    # Links in alte Datei rausholen
    tree = html.parse(old_html_url)
    old_links = tree.xpath("//div[@id='react-root']//article//a")  # Contains complete <a> Tags
    old_links_list = []  # Only holds hrefs
    for link in old_links:
        old_links_list.append(link.attrib["href"])
    print("old links: ")
    old_links_list[0] = "test"  # Erkennungstest, danach zu löschen TODO
    print(old_links_list)

    # Links in neue Datei rausholen
    new_tree = html.parse(new_html_url)
    new_links = new_tree.xpath("//div[@id='react-root']//article//a")  # Contains complete <a> Tags
    new_links_list = []  # Only holds hrefs
    for link in new_links:
        new_links_list.append(link.attrib["href"])
    print("new links: ")
    print(new_links_list)

    # Links vergleichen
    for index in range(len(new_links_list)):
        if new_links_list[index] not in old_links_list:
            parent = new_links[index].getparent()
            parent.attrib["style"] = "border = 5px solid green"
            print(etree.tostring(parent))
            print("New link: " + new_links_list[index])

    open("aaa.html", "wb").write(etree.tostring(tree))


compare_posts()



