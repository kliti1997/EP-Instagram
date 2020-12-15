from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html


# from instagram.src.instagram import Instagram

def pre_modify(url):
    return os.path.isfile(get_old_html_path(url)) and os.path.isfile(get_new_html_path(url))


def compare_posts(url):
    old_html_path = get_old_html_path(url)
    new_html_path = get_new_html_path(url)

    # Links in alte Datei rausholen
    tree = html.parse(old_html_path)
    old_links = tree.xpath("//div[@id='react-root']//article//a")  # Contains complete <a> Tags
    old_links_list = []  # Only holds hrefs
    for link in old_links:
        old_links_list.append(link.attrib["href"])

    # Links in neue Datei rausholen
    new_tree = html.parse(new_html_path)
    new_links = new_tree.xpath("//div[@id='react-root']//article//a")  # Contains complete <a> Tags
    new_links_list = []  # Only holds hrefs
    for link in new_links:
        new_links_list.append(link.attrib["href"])


    # Links vergleichen
    for index in range(len(new_links_list)):
        if new_links_list[index] not in old_links_list:
            parent = new_links[index].getparent()
            parent.attrib["style"] = "border: 4px solid green;"

    open(new_html_path, "wb").write(etree.tostring(new_tree, method="html"))


def compare_followers_following(url):
    old_html = html.parse(get_old_html_path(url))
    new_html = html.parse(get_new_html_path(url))

    oldFollowersElement = list(old_html.xpath("//a[@href='https://www.instagram.com/" + url["id"] +  "/followers/']")[0].iter())
    #oldSubElement = list(oldFollowersElement.iter())
    oldFollowersCnt = [element.attrib['title'] for element in oldFollowersElement if element.tag == "span"][0]

    print("Debug")
    print(oldFollowersElement)
    #print(oldSubElement)

    newFollowersElement = new_html.xpath("//a[@href='https://www.instagram.com/" + url["id"] +  "/followers/']")[0]
    newSubElement = list(newFollowersElement.iter())
    newFollowersCnt = [element.attrib['title'] for element in newSubElement if element.tag == "span"][0]


    #Ungefaehre Follower Anzahl mit genauer Anzahl ersetzen
    #Geht bestimmt schoener, allerdings weiss ich leider aktuell nicht wie    
    for element in newSubElement:
        if element.tag == "span":
            element.text = newFollowersCnt
            break

    if oldFollowersCnt != newFollowersCnt:
        newFollowersElement.attrib['style'] = "border: 4px solid green;"
                
    #Following bzw. Abonnierte
    #Komischerweise hat der Container kein 'title' Wert wie er bei den Abonnenten existiert
    #Wir muessen deshalb aus dem 'text' direkt lesen
    oldElements = list(old_html.iter("a"))
    oldFollowingElement = [element for element in oldElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/" + url["id"] + "/following/"][0]
    oldSubElement = list(oldFollowingElement.iter())
    oldFollowingCnt = [element.text for element in oldSubElement if element.tag == "span"][0]

    newElements = list(new_html.iter("a"))
    newFollowingElement = [element for element in newElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/" + url["id"] + "/following/"][0]
    newSubElement = list(newFollowingElement.iter())
    newFollowingCnt = [element.text for element in newSubElement if element.tag == "span"][0]
                
    if oldFollowingCnt != newFollowingCnt:
        newFollowingElement.attrib['style'] = "border: 4px solid green;"
    
    open(get_new_html_path(url), "wb").write(etree.tostring(new_html, method="html"))


def compare_igtv(url):
    old_html_path = get_old_html_path(url)
    new_html_path = get_new_html_path(url)

    # Getting all links in old igtv html file
    tree = html.parse(old_html_path)
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
    new_tree = html.parse(new_html_path)
    new_links = new_tree.xpath("//div[@id='react-root']//main//div//a")  # Contains complete <a> Tags

    new_igtv_a_list = []
    new_igtv_href_list = []

    # Saving only elements with tv/ links
    for link in new_links:
        if link.attrib["href"].startswith("https://www.instagram.com/tv/"):
            new_igtv_a_list.append(link)

    # Only saving href attribute for comparison
    for href in new_igtv_a_list:
        new_igtv_href_list.append(href.attrib["href"])

    for index in range(len(new_igtv_href_list)):
        if new_igtv_href_list[index] not in old_igtv_href_list:
            new_igtv_a_list[index].attrib["style"] = "border: 4px solid green;"


    open(new_html_path, "wb").write(etree.tostring(new_tree, method="html"))


def compare_hover_items(url):
    """
    Benötigte html-Attribute:
    - data-typename (GraphSidecar, GraphImage, GraphVideo)
                                            => bereits vorhanden: aria-label="Video" == GraphVideo
                                                                  aria-label="Carousel" == GraphSidecar
                                                                  no aria-label == GraphImage
    - data-id (unnötig, einfach href verwenden)
    In Abhängigkeit vom typename:
    - data-liked-by (GraphSidecar, GraphImage)
    - data-view-count (GraphVideo)
    - data-comment (GraphSidecar, GraphImage, GraphVideo)
    """
    old_tree = html.parse(get_old_html_path(url))
    new_tree = html.parse(get_new_html_path(url))

    new_posts = new_tree.xpath("//div[@id='react-root']//article//a")
    old_posts = old_tree.xpath("//div[@id='react-root']//article//a")
    head = new_tree.xpath("//head")

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

    add_border = "style='border: 4px solid green;'"

    # Posts miteinander vergleichen
    for new_post in new_posts:
        for old_post in old_posts:
            if new_post.attrib["href"] == old_post.attrib["href"]:

                if new_post.xpath(".//span[@aria-label='Video']") or url["type"] == "igtv": # Falls es ein Video ist, vergleiche view-count.
                    to_cmp = "data-view-count"
                else:
                    to_cmp = "data-liked-by"

                if new_post.attrib[to_cmp] != old_post.attrib[to_cmp] and new_post.attrib["data-comment"] != old_post.attrib["data-comment"]:
                    new_post.append( # Views und comments haben sich verändert.
                        etree.fromstring(
                            hover.format(likes_views = new_post.attrib[to_cmp],
                            icon_likes_views="coreSpritePlayIconSmall",
                            comments = new_post.attrib["data-comment"],
                            style_likes_views = add_border,
                            style_comments = add_border)
                        )
                    )
                elif new_post.attrib[to_cmp] != old_post.attrib[to_cmp]:
                    new_post.append( # Nur die views, oder likes, haben sich verändert.
                        etree.fromstring(
                            hover.format(likes_views = new_post.attrib[to_cmp],
                            icon_likes_views="coreSpritePlayIconSmall",
                            comments = new_post.attrib["data-comment"],
                            style_likes_views = add_border,
                            style_comments = "")
                        )
                    )    
                elif new_post.attrib["data-comment"] != old_post.attrib["data-comment"]:
                    new_post.append( # Nur die comments haben sich verändert.
                        etree.fromstring(
                            hover.format(likes_views = new_post.attrib[to_cmp],
                            icon_likes_views="coreSpritePlayIconSmall",
                            comments = new_post.attrib["data-comment"],
                            style_likes_views = "",
                            style_comments = add_border)
                        )
                    )

    head[0].append(etree.fromstring(css))
    open(get_new_html_path(url), "wb").write(etree.tostring(new_tree, method="html"))

def compare_tagged(url):
    old_html_path = get_old_html_path(url)
    new_html_path = get_new_html_path(url)

    # Links in alte Datei rausholen
    tree = html.parse(old_html_path)
    old_links = tree.xpath("//div[@id='react-root']//article//a")  # Contains complete <a> Tags
    old_links_list = []  # Only holds hrefs
    for link in old_links:
        old_links_list.append(link.attrib["href"])

     # Links in neue Datei rausholen
    new_tree = html.parse(new_html_path)
    new_links = new_tree.xpath("//div[@id='react-root']//article//a")  # Contains complete <a> Tags
    new_links_list = []  # Only holds hrefs
    for link in new_links:
        new_links_list.append(link.attrib["href"])

    # Links vergleichen
    for index in range(len(new_links_list)):
        if new_links_list[index] not in old_links_list:
            parent = new_links[index].getparent()
            parent.attrib["style"] = "border: 4px solid green;"

    open(new_html_path, "wb").write(etree.tostring(new_tree, method="html"))
