"""
This module is used to provide functionalities to perform the storing phase of the package.

The core functionalities in this module are the login process at instagram and the
downloading and saving of html files.

#TODO Make the login process unnecessary.
"""
from instagram.data.config import *
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from pprint import pprint
from lxml import etree, html
from pathlib import Path
from html import unescape
import json

MIN_TIME = 3
INCR_UPPER_BOUND = 10
"""
Constants to calculate the sleep timer.
"""



def login(username, password):
    """
    The function is used to perform the login process at instagram.com.
    It also accepts the cookie banner and saves the login information.

    Args:
        username (str): The username which is used to log in.
        password (str): The password which is used to log in.
    """
    driver.get(base_url)
    random_sleep(5)
    if driver.find_elements_by_xpath("//*[contains(., 'Cookies') or contains(., 'cookies')]"):
        cookie_consent()
        random_sleep(5)

    # Log into account only if not already logged in.
    if driver.find_elements_by_xpath("//*[text()='Log In']") or driver.find_elements_by_xpath("//*[text()='Anmelden']"):
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        if driver.find_elements_by_xpath("//*[text()='Log In']"):
            driver.find_element_by_xpath("//*[text()='Log In']").click()
        else:
            driver.find_element_by_xpath("//*[text()='Anmelden']").click()
        random_sleep(10)


    if "onetap" in driver.current_url:  # "Save your Login?"-Page
        if driver.find_elements_by_xpath("//*[text()='Save Info']"):
            driver.find_element_by_xpath("//*[text()='Save Info']").click()
        else:
            driver.find_element_by_xpath("//*[text()='Informationen speichern']").click()

    random_sleep(10)


def cookie_consent():
    """
    Accepts the cookie banner, if it exists. Otherwise the downloaded html-files
    are obfuscated by the banner.
    """
    if driver.find_elements_by_xpath("//*[text()='Akzeptieren']"):
        driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
    elif driver.find_elements_by_xpath("//*[text()='Accept']"):
        driver.find_element_by_xpath("//*[text()='Accept']").click()


def convert_links(source):
    """
    Converts relative to absolute links in a given string by appending a base-url, which is specified
    in the config-file.
    Only links which are the content of the html attributes href, src, or srcset, or of a dictionary
    will be changed.

    Example:
        Let's assume the base_url is https://instagram.com
        <a href="/sta/exmpl.css"> will be converted to <a href="https://instagram.com/sta/exmpl.css">
        dic = {a: "/sta/exmpl.css"} will be converted to dic = {a: "https://instagram.com/sta/exmpl.css"}

    Args:
        source (str): The string representation of the parsed html file.

    Returns:
        str: The same string as source, but with converted links.
    """
    return re.sub(r'(href="|src="|srcset="|:")/', r'\1' + base_url, source)


def save_html(url):
    """
    Saves the html content of a website and saves it in a file.
    Depending on the input, the function will either save the content of the "posts" intsagram subdirectory,
    the "tagged" subdirectory, or the "IGTV" subdirectory.

    Args:
        url (dict): Containts the url to the website that has to be saved, as well as the type in terms of
                    "posts", "tagged", or "IGTV". It also contains a path where the generated files are going
                    to be saved.
    """
    type = str(url["type"])
    link = str(url["href"])

    driver.get(link)
    random_sleep(10)
    latest_story_timestamp()

    content = unescape(convert_links(driver.execute_script("return new XMLSerializer().serializeToString(document);")))
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(content, etree.HTMLParser())

    pre_download(url)
    with open(os.path.join(monitoring_folder, url["monitoring_folder"], type + ".html"), "w") as f:
        f.write(content)


def latest_story_timestamp() -> int:
    """
    Checks if an active story exists.

    Returns:
        int: timestamp of last story, 0 if none exists
    """
    for request in driver.requests:
        if request.response:
            if 'graphql' in request.url:
                reply_content = request.response.body.decode('utf-8')
                if 'latest_reel_media' in reply_content and 'edge_suggested_users' not in reply_content:  # Identifying correct request
                    reply_json = json.loads(reply_content)
                    return reply_json['data']['user']['reel']['latest_reel_media']
    return 0


def random_sleep(max_time):
    """
    Pauses the program sequence for a pseudo random time, depending on the input.
    The program sequence will be paused for at least 3 seconds.

    Args:
        max_time (int): Determines how long the program sequence is paused at most.
    """
    if max_time < MIN_TIME:
        max_time = MIN_TIME + INCR_UPPER_BOUND
    random_time = randint(MIN_TIME, max_time)
    sleep(random_time)


def pre_download(url):
    """
    If a file already exists in the monitoring folder, it's name will be changed
    by appending _old.html.
    If there is already an old file, it will be deleted.

    Args:
        url (dict): Containts the path of the monitoring folder and one of the types
                    "posts", "tagged", or "IGTV" to determine the file name.
    """
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

    open("aaa.html", "wb").write(etree.tostring(new_tree))



def compare_followers_following(oldHtml, newHtml):
    #Wir brauchen einheitliche Namen fuer die .html Dateien
    #Ich war der Meinung er meinte wir sollen "old.html" und "new.html" verwenden
    oldDoc = etree.HTML(oldHtml)
    newDoc = etree.HTML(newHtml)
                
    #Followers bzw. Abonneten
    oldElements = list(oldDoc.iter("a"))
    oldFollowersElement = [element for element in oldElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/polizei.hannover/followers/"][0]
    oldSubElement = list(oldFollowersElement.iter())
    oldFollowersCnt = [element.attrib['title'] for element in oldSubElement if element.tag == "span"][0]

    newElements = list(newDoc.iter("a"))
    newFollowersElement = [element for element in newElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/polizei.hannover/followers/"][0]
    newSubElement = list(newFollowersElement.iter())
    newFollowersCnt = [element.attrib['title'] for element in newSubElement if element.tag == "span"][0]
                
    print(oldFollowersCnt)
    print(newFollowersCnt)
                
    if oldFollowersCnt != newFollowersCnt:
        newFollowersElement.attrib['style'] = "border: 5px solid green;"
                
    #Following bzw. Abonnierte
    #Komischerweise hat der Container kein 'title' Wert wie er bei den Abonnenten existiert
    #Wir muessen deshalb aus dem 'text' direkt lesen
    oldElements = list(oldDoc.iter("a"))
    oldFollowingElement = [element for element in oldElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/polizei.hannover/following/"][0]
    oldSubElement = list(oldFollowingElement.iter())
    oldFollowingCnt = [element.text for element in oldSubElement if element.tag == "span"][0]

    newElements = list(newDoc.iter("a"))
    newFollowingElement = [element for element in newElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/polizei.hannover/following/"][0]
    newSubElement = list(newFollowingElement.iter())
    newFollowingCnt = [element.text for element in newSubElement if element.tag == "span"][0]

    print(oldFollowingCnt)
    print(newFollowingCnt)
                
    if oldFollowersCnt != newFollowersCnt:
        newFollowingElement.attrib['style'] = "border: 1px solid green;"
    
    #Im Regelbetrieb dann in new.html schreiben "bbb.html" ist nur zum testen          
    open("bbb.html", "wb").write(etree.tostring(newDoc))

    return 0


def compare_igtv():
    old_html_url = "instagram/data/files/polizei.hannover/igtv/igtv_old.html"
    new_html_url = "instagram/data/files/polizei.hannover/igtv/igtv.html"
    # TODO Zur richtige Verzeichnis wechseln, muss noch geaendert werden
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")

    # Getting all links in old igtv html file
    tree = html.parse(old_html_url)
    old_links = tree.xpath("//div[@id='react-root']//main//div//a")  # Contains complete <a> Tags

    old_igtv_a_list = []
    old_igtv_href_list = []
    # Saving only elements with tv/ links
    for link in old_links:
        if link.attrib["href"].startswith("https://www.instagram.com/tv/"):
            old_igtv_a_list.append(link)

    # Only saving href attribute for comparison
    for href in old_igtv_a_list:
        old_igtv_href_list.append(href.attrib["href"])

    # Getting all links in new igtv html file
    new_tree = html.parse(new_html_url)
    new_links = new_tree.xpath("//div[@id='react-root']//main//div//a")  # Contains complete <a> Tags
    # print(etree.tostring(new_divs[1]))

    new_igtv_a_list = []
    new_igtv_href_list = []

    # Saving only elements with tv/ links
    for link in new_links:
        if link.attrib["href"].startswith("https://www.instagram.com/tv/"):
            new_igtv_a_list.append(link)

    # Only saving href attribute for comparison
    for href in new_igtv_a_list:
        new_igtv_href_list.append(href.attrib["href"])

    old_igtv_href_list[0] = "test"  # should be remove afterwards

    for index in range(len(new_igtv_href_list)):
        if new_igtv_href_list[index] not in old_igtv_href_list:
            new_igtv_a_list[index].attrib["style"] = "border = 5px solid green"
            print("New link: " )
            print(etree.tostring(new_igtv_a_list[index]))

    open("igtv.html", "wb").write(etree.tostring(new_tree))
