from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import ActionChains
from collections import defaultdict
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from time import sleep
import os
import logging
import re
from pathlib import Path

# Pfade
config_folder = os.path.dirname(os.path.abspath(__file__))
monitoring_folder = os.path.join(config_folder, "files")
profile_folder = os.path.join(config_folder, "profile")
geckodriver = os.path.join(config_folder, "geckodriver")

# Selenium Einsetllungen
Path(profile_folder).mkdir(parents=True, exist_ok=True)
driver_profile = webdriver.FirefoxProfile(profile_folder)
driver = webdriver.Firefox(firefox_profile=driver_profile, executable_path = geckodriver)

# Logger um error und info messages zu speichern
logger = logging.getLogger("myLogger")
f_handler = logging.FileHandler(os.path.join(os.getcwd(), "exception.log"))
f_format = logging.Formatter('%(asctime)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

# Instagram Daten
base_url = "https://www.instagram.com/"
login_url = "https://www.instagram.com/accounts/login/?next=%2Fexplore%2F&source=desktop_nav"  # TODO: Randomize 'next' page
ig_credentials = {"user": "swp_ep_ig_1_test",
                  "pass": "Test123!"}

# URL's zum testen
monitoring_map = defaultdict(list)
url1 = {"id":"polizei.hannover",
    "href":"https://www.instagram.com/polizei.hannover/",
    "type":"posts","mode":"1","monitoring_folder": monitoring_folder,
    "change":"","notify":"","err":""}
#url2 = {"id":"polizei.hannover",
#    "href":"https://www.instagram.com/polizei.hannover/channel",
#    "type":"IGTV","mode":"1","monitoring_folder":"./polizei.hannover/IGTV/",
#    "change":"","notify":"","err":""}
monitoring_map["instagram"].append(url1)
#monitoring_map["instagram"].append(url2)