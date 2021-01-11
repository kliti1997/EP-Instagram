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
import logging.config
import re
from pathlib import Path

config_folder = os.path.dirname(os.path.abspath(__file__))
monitoring_folder = os.path.join(config_folder, "files")
profile_folder = os.path.join(config_folder, "profile")
log_folder = os.path.join(config_folder, "logs")
geckodriver = os.path.join(config_folder, "geckodriver")
geckodriver_log = os.path.join(log_folder, "geckodriver.log")
"""
Different path variables.
"""

Path(profile_folder).mkdir(parents=True, exist_ok=True)
driver_profile = webdriver.FirefoxProfile(profile_folder)
driver_profile.set_preference('intl.accept_languages','de')
#driver = webdriver.Firefox(firefox_profile=driver_profile, executable_path = geckodriver, log_path=geckodriver_log)
driver = webdriver.Firefox(executable_path = os.path.join(config_folder, "geckodriver_macOS"))
"""
Seleniumwire driver and it's options.
"""

LOGGING_CONFIG = {
    'version': 1, # required
    'disable_existing_loggers': True, # this config overrides all other loggers
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S'
        },
        'detailed': {
            'format': '[%(asctime)s]\t%(levelname)s -- %(processName)s %(filename)s:%(lineno)s -- %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_folder, "error.log"),
            'formatter': 'detailed'
        },
        'error_console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'instagram': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_folder, "instagram.log"),
            'formatter': 'simple'
        },
        'testing': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_folder, "testing.log"),
            'formatter': 'detailed',
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['error', 'error_console']
        },
        'instagram': {
            'level': 'INFO',
            'handlers': ['console', 'testing']
        },
        'basic_test': {
            'level': 'DEBUG',
            'handlers': ['console', 'testing']
        },
        'download_test': {
            'level': 'DEBUG',
            'handlers': ['console', 'testing']
        },
        'compare_test': {
            'level': 'DEBUG',
            'handlers': ['console', 'testing']
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

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
