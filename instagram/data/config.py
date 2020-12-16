"""
The module is used to define objects which will be used by almost every other module.
Nearly every other module will import this subpackage, respectively module, to gain
access to these objects.

Examples:
    Instagram Login credentials.
    Essential import statements which are used by multiple subpackages.
"""
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import ActionChains
from collections import defaultdict
from urllib.parse import urljoin
from time import sleep
import os
import logging
import re
from pathlib import Path

config_folder = os.path.dirname(os.path.abspath(__file__))
monitoring_folder = os.path.join(config_folder, "files")
profile_folder = os.path.join(config_folder, "profile")
geckodriver = os.path.join(config_folder, "geckodriver")
#geckodriver = os.path.join(config_folder, "geckodriver_macOS")
"""
Different path variables.
"""

Path(profile_folder).mkdir(parents=True, exist_ok=True)
driver_profile = webdriver.FirefoxProfile(profile_folder)
driver_profile.set_preference('intl.accept_languages','de')
driver = webdriver.Firefox(firefox_profile=driver_profile, executable_path = geckodriver)
#driver = webdriver.Firefox(executable_path = geckodriver)
"""
Seleniumwire driver and it's options.
"""

logger = logging.getLogger("myLogger")
f_handler = logging.FileHandler(os.path.join(config_folder, "exception.log"))
f_format = logging.Formatter('%(asctime)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
"""
Error logging, including options to represent the output and an output file.
"""

base_url = "https://www.instagram.com/"
login_url = "https://www.instagram.com/accounts/login/?next=%2Fexplore%2F&source=desktop_nav"  # TODO: Randomize 'next' page
ig_credentials = {"user": "swp_ep_ig_1_test",
                  "pass": "Test123!"}
"""
Instagram credentials and other login information.
"""
