import re
from instagram.data.config import *
from random import randint
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint
from lxml import etree
from pathlib import Path


MIN_TIME = 3
SUMMAND = 10
"""
Module level constants
"""

def login(username, password):
    """
    The function is used to perform the login process at instagram.com.
    It also accepts the cookie banner and saves the login information.

    Args:
        username (str): The username which is used to log in.
        password (str): The password which is used to log in.
    """
    driver.get(login_url)
    random_sleep(5)
    cookie_consent()
    random_sleep(5)

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)

    if driver.find_elements_by_xpath("//*[text()='Log In']"):
        driver.find_element_by_xpath("//*[text()='Log In']").click()
    else:
        driver.find_element_by_xpath("//*[text()='Anmelden']") 

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
    if type != 'posts':
        link += type

    driver.get(link)
    random_sleep(10)

    content = convert_links(driver.execute_script("return new XMLSerializer().serializeToString(document);"))
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(content, etree.HTMLParser())

    pre_download(url)
    with open(os.path.join(monitoring_folder, url["monitoring_folder"], type + ".html"), "w") as f:
        f.write(content)


def random_sleep(max_time):
    """
    Pauses the program sequence for a pseudo random time, depending on the input.
    The program sequence will be paused for at least 3 seconds.

    Args:
        max_time (int): Determines how long the program sequence is paused at most.
    """
    if max_time < MIN_TIME:
        max_time = MIN_TIME + SUMMAND
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
