"""
The module changes the new html file by comparing it's entries with the old html file.
The functions in the module are called in the instagram_monitor module.
"""
from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html

NEW = 0
OLD = 1
"""
Constants to determine whether the old, or new html-file is accessed.
"""

# from instagram.src.instagram import Instagram

def pre_modify(url):
    return os.path.isfile(get_old_html_path(url)) and os.path.isfile(get_new_html_path(url))


def compare_posts(url, ig):
    """
    This function compares the posts of the profile and marks the new one with a green border.

    The href of each post in the old.html file are saved in the old_links_list. The same is done for
    the new.html file in new_links_list. The lists are than compared with one another and the posts with new
    href are marked with a green border to show that it is a new post. We than set change and notify to true.

    Args:
        url (url): The url of the file
        ig (InstagramObject): The instagram profile
    """
    old_links_list = []  # Only holds hrefs
    for link in ig[OLD].get_posts():
        old_links_list.append(link.attrib["href"])

    new_links_list = []  # Only holds hrefs
    for link in ig[NEW].get_posts():
        new_links_list.append(link.attrib["href"])

    # Compare links, if a new one is found we mark it with a green border
    for index in range(len(new_links_list)):
        if new_links_list[index] not in old_links_list:
            parent = ig[NEW].get_posts()[index].getparent()
            parent.attrib["style"] = "border: 4px solid green;"
            set_change(url)
            set_notify(url)

    ig[NEW].write(url)


def compare_followers_following(url, ig):
    oldFollowersCnt = ig[OLD].get_followers()[0].attrib["title"]
    newFollowersCnt = ig[NEW].get_followers()[0].attrib["title"]

    # Substitute the compact Followers number with the precise one
    ig[NEW].get_followers()[0].text = newFollowersCnt

    if oldFollowersCnt != newFollowersCnt:
        ig[NEW].get_followers().attrib['style'] = "background-color: green;"
        set_change(url)
        if get_mode(url) == '1':
            set_notify(url)

    # Following or Abonnierte
    oldFollowingCnt = ig[OLD].get_following()[0].text
    newFollowingCnt = ig[NEW].get_following()[0].text

    if oldFollowingCnt != newFollowingCnt:
        ig[NEW].get_following().attrib['style'] = "background-color: green;"
        set_change(url)
        if get_mode(url) == '1':
            set_notify(url)

    ig[NEW].write(url)


def compare_igtv(url, ig):
    """
    This function compares the posts in the IGTV section of the profile and marks the new one with a green border.

    The href of each IGTV post in the old.html file are saved in the old_igtv_href_list. The same is done for
    the new.html file in new_igtv_href_list. The lists are than compared with one another and the posts with new
    href are marked with a green border to show that it is a new post. We than set change and notify to true.

    Args:
        url (url): The url of the file
        ig (InstagramObject): The instagram profile
    """
    # Getting all links in old igtv html file
    old_igtv_href_list = []
    for link in ig[OLD].get_igtvs():
        old_igtv_href_list.append(link.attrib["href"])

    # Getting all links in new igtv html file
    new_igtv_href_list = []
    for link in ig[NEW].get_igtvs():
        new_igtv_href_list.append(link.attrib["href"])

    # Compare links, if a new one is found we mark it with a green border and set change and notify to true
    # todo implementation check, get parent missing
    for index in range(len(new_igtv_href_list)):
        if new_igtv_href_list[index] not in old_igtv_href_list:
            ig[NEW].get_igtvs()[index].attrib["style"] = "border: 4px solid green;"
            set_change(url)
            set_notify(url)

    ig[NEW].write(url)

def compare_hover_items(url, ig):
    """
    The function checks whether there are any changes in the view-count, the like-count, or the
    commented-count for any posts, igtv, or tagged objects.
    In case of changes the function adds html code to the object that changed. 
    For posts and tags the html code is added in the same way and for igtv objects it's required
    to add the html code in a different way.
    The neccessary css code is added in the header of the html file.

    Args:
        url (url): The url of the file
        ig (InstagramObject): The instagram profile
    """
    if url["type"] == "posts":
        new_elements = ig[NEW].get_posts()
        old_elements = ig[OLD].get_posts()
    elif url["type"] == "igtv":
        new_elements = ig[NEW].get_igtvs()
        old_elements = ig[OLD].get_igtvs()
    else:
        new_elements = ig[NEW].get_tags()
        old_elements = ig[OLD].get_tags()

    head = ig[NEW].get_tree().xpath("//head")

    css = """ <style>
                  .qn-0x{display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-box-orient:vertical;-webkit-box-direction:normal;-webkit-flex-direction:column;-ms-flex-direction:column;flex-direction:column;-webkit-box-pack:center;-webkit-justify-content:center;-ms-flex-pack:center;justify-content:center;bottom:0;left:0;position:absolute;right:0;top:0}
                  .Ln-UN{-webkit-box-align:center;-webkit-align-items:center;-ms-flex-align:center;align-items:center;color:#fff;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;font-size:16px;font-weight:600;height:100%;-webkit-box-pack:center;-webkit-justify-content:center;-ms-flex-pack:center;justify-content:center;width:100%}
                  .-V_eO{display:-webkit-inline-box;display:-webkit-inline-flex;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-orient:horizontal;-webkit-box-direction:reverse;-webkit-flex-direction:row-reverse;-ms-flex-direction:row-reverse;flex-direction:row-reverse;margin-right:30px}
                  .-V_eO:last-child{margin-right:0}
              </style>"""

    hover = """ <div class="qn-0x" style="background-color: rgba(0, 0, 0, 0.3);">
                    <ul class="Ln-UN">
                        <li class="-V_eO" {style_likes_views}>
                            <span>{likes_views}</span>
                            <span class="_1P1TY {icon_likes_views}"></span>
                        </li>
                        <li class="-V_eO" {style_comments}>
                            <span>{comments}</span>
                            <span class="_1P1TY coreSpriteSpeechBubbleSmall"></span>
                        </li>
                    </ul>
                </div>"""

    add_border = "style='background-color: green;'"

    for new_ele in new_elements:
        for old_ele in old_elements:
            if new_ele.attrib["href"] == old_ele.attrib["href"]:

                if new_ele.xpath(".//span[@aria-label='Video']") or url["type"] == "igtv":  # If the current object is a video, compare the view-count.
                    to_cmp = "data-view-count"
                    sprite = "coreSpritePlayIconSmall"
                else:
                    to_cmp = "data-liked-by"
                    sprite = "coreSpriteHeartSmall"

                if url["type"] != "igtv":
                    if new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp] and new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]:
                        # Views- and comments-count changed.
                        new_ele.append(
                            etree.fromstring(
                                hover.format(likes_views=new_ele.attrib[to_cmp],
                                             icon_likes_views=sprite,
                                             comments=new_ele.attrib["data-comment"],
                                             style_likes_views=add_border,
                                             style_comments=add_border)
                            )
                        )
                        set_change(url)
                        set_notify(url)
                    elif new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp]:
                        new_ele.append(  # Only views- XOR likes-count changed.
                            etree.fromstring(
                                hover.format(likes_views=new_ele.attrib[to_cmp],
                                             icon_likes_views=sprite,
                                             comments=new_ele.attrib["data-comment"],
                                             style_likes_views=add_border,
                                             style_comments="")
                            )
                        )
                        set_change(url)
                        if get_mode(url) == '1':
                            set_notify(url)
                    elif new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]:
                        new_ele.append(  # Only the comment-count changed.
                            etree.fromstring(
                                hover.format(likes_views=new_ele.attrib[to_cmp],
                                             icon_likes_views=sprite,
                                             comments=new_ele.attrib["data-comment"],
                                             style_likes_views="",
                                             style_comments=add_border)
                            )
                        )
                        set_change(url)
                        set_notify(url)
                else:
                    # The class qn-0x already exists for igtv objects and needs to be replaced.
                    if new_ele.xpath(".//div[@class='qn-0x']") and (
                            new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp] or new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]):
                        rmv_list = new_ele.xpath(".//div[@class='qn-0x']")
                        for to_rmv in rmv_list:
                            to_rmv.getparent().remove(to_rmv)

                    if new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp] and new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]:
                        # Views- and comments-count changed.
                        new_ele.getchildren()[0].append(
                            etree.fromstring(
                                hover.format(likes_views=new_ele.attrib[to_cmp],
                                             icon_likes_views=sprite,
                                             comments=new_ele.attrib["data-comment"],
                                             style_likes_views=add_border,
                                             style_comments=add_border)
                            )
                        )
                        set_change(url)
                        set_notify(url)
                    elif new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp]:
                        new_ele.getchildren()[0].append(  # Only views- XOR likes-count changed.
                            etree.fromstring(
                                hover.format(likes_views=new_ele.attrib[to_cmp],
                                             icon_likes_views=sprite,
                                             comments=new_ele.attrib["data-comment"],
                                             style_likes_views=add_border,
                                             style_comments="")
                            )
                        )
                        set_change(url)
                        if get_mode(url) == '1':
                            set_notify(url)
                    elif new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]:
                        new_ele.getchildren()[0].append(  # Only the comment-count changed.
                            etree.fromstring(
                                hover.format(likes_views=new_ele.attrib[to_cmp],
                                             icon_likes_views=sprite,
                                             comments=new_ele.attrib["data-comment"],
                                             style_likes_views="",
                                             style_comments=add_border)
                            )
                        )
                        set_change(url)
                        set_notify(url)

    head[0].append(etree.fromstring(css))
    ig[NEW].write(url)


def compare_tagged(url, ig):
    """
    This function compares the posts in the Tagged section of the profile and marks
    the new one with a green border.

    The href of each post in the old.html file are saved in the old_links_list. The same is done for
    the new.html file in new_links_list. The lists are than compared with one another and the posts with new
    href are marked with a green border to show that it is a new post. We than set change and notify to true.

    Args:
        url (url): The url of the file
        ig (InstagramObject): The instagram profile
    """
    # Take the links in the old file
    old_links_list = []  # Only holds hrefs
    for link in ig[OLD].get_tags():
        old_links_list.append(link.attrib["href"])

    # Take the links in the new file
    new_links_list = []  # Only holds hrefs
    for link in ig[NEW].get_tags():
        new_links_list.append(link.attrib["href"])

    # Compare links, if there are new ones, mark them with a green border
    for index in range(len(new_links_list)):
        if new_links_list[index] not in old_links_list:
            parent = ig[NEW].get_tags()[index].getparent()
            parent.attrib["style"] = "border: 4px solid green;"
            set_change(url)
            set_notify(url)

    ig[NEW].write(url)


def compare_stories(url, ig):
    """
    This function compares the timestamps of the stories to check if a new story was published since the
    last control.

    The function gets the data-story-timestamp from both files and checks if new_timestamp is actually
    newer than old_timestamp. If this is the case, the profile picture is marked with a green border.
    The change and notify are than set to true.

    Args:
        url (url): The url of the file
        ig (InstagramObject): The instagram profile
    """
    old_timestamp = ig[OLD].get_profile_pic_modify().attrib["data-story-timestamp"]
    new_timestamp = ig[NEW].get_profile_pic_modify().attrib["data-story-timestamp"]

    if new_timestamp > old_timestamp:
        ig[NEW].get_profile_pic_modify().attrib["style"] = "border: 4px solid green;"
        set_change(url)
        set_notify(url)
