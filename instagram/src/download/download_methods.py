"""
This module is used to provide functionalities to perform the storing phase of the package.

The core functionalities in this module are the login process at instagram and the
downloading and saving of html files.

"""
from instagram.src.helper import *
from instagram.src.instagram_object import InstagramObject
from random import randint
from lxml import etree
from pathlib import Path
from .profile_data import ProfileData
import lxml
import datetime

from ...data.config import RANDOM_SLEEP_MIN_TIME

"""
Constants to calculate the sleep timer.
"""

logger = logging.getLogger('instagram')


def login(username, password):
    """
    The function is used to perform the login process at instagram.com.
    It also accepts the cookie banner and saves the login information.

    Args:
        username (str): The username which is used to log in.
        password (str): The password which is used to log in.
    """
    # Accepts the "stay logged in" banner, if it exists.
    if driver.find_elements_by_xpath("//*[contains(text(),'Als') and contains(text(),'fortfahren')]"):
        driver.find_element_by_xpath("//*[contains(text(),'Als') and contains(text(),'fortfahren')]").click()
        random_sleep(10)

    # Accepts the "stay logged in" banner, if it exists. (english)
    if driver.find_elements_by_xpath("//*[contains(text(),'Continue as')]"):
        driver.find_element_by_xpath("//*[contains(text(),'Continue as')]").click()
        random_sleep(10)

    # Accepts the cookie banner, if it exists.
    if driver.find_elements_by_xpath("//*[text()='Akzeptieren' or text()='Accept']"):
        driver.find_element_by_xpath("//*[text()='Akzeptieren' or text()='Accept']").click()
        random_sleep(6)

    # Log into account only if not already logged in.
    if driver.find_elements_by_xpath("//*[text()='Anmelden' or text()='Log In']"):
        logger.warn('Wasn\'t logged in already. Please check your Firefox-Profile.')
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_xpath("//*[text()='Anmelden' or text()='Log In']").click()
        random_sleep(10)

    # Accepts the stay logged in banner, if it exists.
    if driver.find_elements_by_xpath("//*[text()='Informationen speichern' or text()='Save Info']"):
        driver.find_element_by_xpath("//*[text()='Informationen speichern' or text()='Save Info']").click()
        random_sleep(10)

    # Accepts the cookie banner, if it exists.
    if driver.find_elements_by_xpath("//*[text()='Jetzt nicht' or 'Not Now']"):
        driver.find_element_by_xpath("//*[text()='Jetzt nicht' or 'Not Now']").click()
        random_sleep(10)


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
    # remove javascript inline script parts
    source = re.sub(r'(?is)<script[^>]*>(.*?)</script>', '', source)

    # remove javascript import links
    source = re.sub(r'<link.*?type="text/javascript".*?/>', '', source)

    # converts relative to absolute links
    source = re.sub(r'(href="|src="|srcset="|:")/', r'\1' + base_url, source)
    return source


def add_html_tags(url, ig_obj: InstagramObject, prof_data: ProfileData) -> None:
    """
    The following things are added to the XML tree:
    - the number of views and comments for videos or likes and comments for photos when they have changed.
    - the timestamp of the last posted story is added to the profile picture for comparison.
    - the (exact) number of followers / following
    """
    if url["type"] == "posts":
        for i, post in enumerate(ig_obj.get_posts()):
            if prof_data.posts[i]["type"] == 'video':
                post.attrib["data-view-count"] = str(prof_data.posts[i]["view_count"])
                replace_video_thumbnail(ig_obj, post)
            else:
                post.attrib["data-liked-by"] = str(prof_data.posts[i]["likes"])
            post.attrib["data-comment"] = str(prof_data.posts[i]["comments"])

    if url["type"] == "tagged":
        for i, tag in enumerate(ig_obj.get_tags()):
            if prof_data.tagged[i]["type"] == 'video':
                tag.attrib["data-view-count"] = str(prof_data.tagged[i]["view_count"])
            else:
                tag.attrib["data-liked-by"] = str(prof_data.tagged[i]["likes"])
            tag.attrib["data-comment"] = str(prof_data.tagged[i]["comments"])

    elif url["type"] == "igtv":
        for i, igtv in enumerate(ig_obj.get_igtvs()):
            igtv.attrib["data-view-count"] = str(prof_data.igtvs[i]["view_count"])
            igtv.attrib["data-comment"] = str(prof_data.igtvs[i]["comments"])

    # Adding the timestamp of the last posted story
    profile_pic = ig_obj.get_profile_pic_download(prof_data.profile_pic_url)
    profile_pic.attrib["data-story-timestamp"] = str(prof_data.story_timestamp)

    # Setting the instagram.com/stories/profile_name url
    anchor = lxml.etree.Element('a', href="https://instagram.com/stories/" + url["id"])
    anchor.extend(profile_pic)
    profile_pic.append(anchor)

    # Adding the number of followers
    ig_obj.get_followers()[0].attrib["data-followers"] = str(prof_data.num_followers)

    #Adding the nummber of users followed
    ig_obj.get_following()[0].attrib["data-following"] = str(prof_data.num_following)

    ig_obj.write(url)


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

    driver.get(get_href(url))
    random_sleep(10)

    return convert_links(driver.execute_script("return new XMLSerializer().serializeToString(document);"))


def random_sleep(max_time):
    """
    Pauses the program sequence for a pseudo random time, depending on the input.
    The program sequence will be paused for at least 3 seconds.

    Args:
        max_time (int): Determines how long the program sequence is paused at most.
    """
    if max_time <= RANDOM_SLEEP_MIN_TIME:
        max_time += RANDOM_SLEEP_MIN_TIME
    random_time = randint(RANDOM_SLEEP_MIN_TIME, max_time)
    sleep(random_time)


def pre_download(url):
    """
    If new.html already exists in the monitoring folder, it's name will be changed
    to old.html.
    If there is already an old file, it will be deleted.
    If the new.html is missing, nothing will be deleted to avoid data loss.

    Args:
        url (dict): Containts the path of the monitoring folder and one of the types
                    "posts", "tagged", or "IGTV" to determine the file path.
    """
    folder_path = get_folder_path(url)
    old_html_path = get_old_html_path(url)
    new_html_path = get_new_html_path(url)
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=True)        #if folder doesn't exists, it will create it
        if os.path.exists(new_html_path):                           #if new.html is missing, nothing will be deleted
            if os.path.exists(old_html_path):
                os.remove(old_html_path)
            if os.path.exists(new_html_path):
                os.rename(new_html_path, old_html_path)

    except Exception as e:
        e_type = e.__class__.__name__
        logger.error("Error in pre-download phase.\nException message: " + e_type + ": " + str(e))
        set_err(url)


def delete_new_html(url):
    """
    Avoid data loss in multiple override of new.html.
    If download fails, new.html will be deleted to skip renaming to old.html.

    Args:
        url (dict): Containts the path of the monitoring folder and one of the types
                    "posts", "tagged", or "IGTV" to determine the file path.
    """
    try:
        new_html_path = get_new_html_path(url)
        if os.path.exists(new_html_path): 
            os.remove(new_html_path)

    except Exception as e:
        e_type = e.__class__.__name__
        logger.error("Error while trying to delete new.html.\nException message: " + e_type + ": " + str(e))
        set_err(url)


def replace_video_thumbnail(ig, post_object):
    """
    In case the video thumbnails are broken (the thumbnails are dynamically generated by instagram and get deleted after ca. 1 day), we replace the broken thumbnails
    with our default thumbnail. The default thumbnail is just a black picture with the label "VIDEO" in the upper part.
    
    Args:
        ig(InstagramObject): Contains the path to the default thumbnail
        post_object(lxml.etree): Is the part of the etree, that contains the posts. We use it to access its <img> tag and to change the thumbnail if
        a error occurs (means: the dynamically thumbnail is expired).
    """
    video_object = post_object
    video_div = video_object.xpath(".//img[@src]")[0]
    video_div.attrib["onerror"] = "this.src='" + ig.get_video_thumbnail_path() + "';this.srcset='';"

def validate_obj(ig, url):
    """
    This method validates the Instagram object and checks if the page was correctly downloaded, otherwise it raises
    a Runtime Error.
    :param ig: The Instagram profile
    :param url: The url of the monitoring_map
    """
    if url["type"] == "posts":
        posts = ig.get_posts()
        logger.debug("len(posts) = " + str(len(posts)))
        if posts is None:
            raise RuntimeError
    if url["type"] == "igtv":
        igtvs = ig.get_igtvs()
        logger.debug("len(igtvs) = " + str(len(igtvs)))
        if igtvs is None:
            raise RuntimeError
    if url["type"] == "tagged":
        tags = ig.get_tags()
        logger.debug("len(tags) = " + str(len(tags)))
        if tags is None:
            raise RuntimeError