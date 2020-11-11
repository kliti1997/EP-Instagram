from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import ActionChains
from collections import defaultdict
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os

this_path = os.getcwd()

# Selenium Einsetllungen
geckodriver = urljoin(this_path, "geckodriver")
driver = webdriver.Firefox(executable_path = geckodriver)
url = "https://www.instagram.com/jimmyfallon/"
driver.get(url)