from instagram.data.config import *
from instagram.src.helper import *
from lxml import etree, html

NEW = 0
OLD = 1

# from instagram.src.instagram import Instagram

def pre_modify(url):
    return os.path.isfile(get_old_html_path(url)) and os.path.isfile(get_new_html_path(url))


def compare_posts(url, ig):
    old_links_list = []  # Only holds hrefs
    for link in ig[OLD].get_posts():
        old_links_list.append(link.attrib["href"])

    new_links_list = []  # Only holds hrefs
    for link in ig[NEW].get_posts():
        new_links_list.append(link.attrib["href"])

    # Links vergleichen
    for index in range(len(new_links_list)):
        if new_links_list[index] not in old_links_list:
            parent = ig[NEW].get_posts()[index].getparent()
            parent.attrib["style"] = "border: 4px solid green;"

    ig[NEW].write(url)


def compare_followers_following(url, ig):
    oldFollowersCnt = ig[OLD].get_followers()[0].attrib["title"]
    newFollowersCnt = ig[NEW].get_followers()[0].attrib["title"]

    #Ungefaehre Follower Anzahl mit genauer Anzahl ersetzen
    ig[NEW].get_followers()[0].text = newFollowersCnt

    if oldFollowersCnt != newFollowersCnt:
        ig[NEW].get_followers().attrib['style'] = "background-color: green;"
                
    #Following bzw. Abonnierte
    oldFollowingCnt = ig[OLD].get_following()[0].text
    newFollowingCnt = ig[NEW].get_following()[0].text
                
    if oldFollowingCnt != newFollowingCnt:
        ig[NEW].get_following().attrib['style'] = "background-color: green;"
    
    ig[NEW].write(url)


def compare_igtv(url, ig):
    # Getting all links in old igtv html file
    old_igtv_a_list = []
    old_igtv_href_list = []

    # Saving only elements with tv/ links
    for link in ig[OLD].get_igtvs():
        old_igtv_a_list.append(link)

    # Only saving href attribute for comparison
    for href in old_igtv_a_list:
        old_igtv_href_list.append(href.attrib["href"])

    # Getting all links in new igtv html file
    new_igtv_href_list = []
    new_igtv_a_list = []

    # Saving only elements with tv/ links
    for link in ig[NEW].get_igtvs():
        new_igtv_a_list.append(link)

    # Only saving href attribute for comparison
    for href in new_igtv_a_list:
        new_igtv_href_list.append(href.attrib["href"])

    for index in range(len(new_igtv_href_list)):
        if new_igtv_href_list[index] not in old_igtv_href_list:
            new_igtv_a_list[index].attrib["style"] = "border: 4px solid green;"


    ig[NEW].write(url)


def compare_hover_items(url, ig):
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

    add_border = "style='border: 4px solid green;'"

    # Posts miteinander vergleichen #TODO Für igtv, tagged anpassen
    for new_ele in new_elements:
        for old_ele in old_elements:
            if new_ele.attrib["href"] == old_ele.attrib["href"]:

                if new_ele.xpath(".//span[@aria-label='Video']") or url["type"] == "igtv": # Falls es ein Video ist, vergleiche view-count.
                    to_cmp = "data-view-count"
                else:
                    to_cmp = "data-liked-by"

                if new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp] and new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]:
                    new_ele.append( # Views und comments haben sich verändert.
                        etree.fromstring(
                            hover.format(likes_views = new_ele.attrib[to_cmp],
                            icon_likes_views="coreSpritePlayIconSmall",
                            comments = new_ele.attrib["data-comment"],
                            style_likes_views = add_border,
                            style_comments = add_border)
                        )
                    )
                elif new_ele.attrib[to_cmp] != old_ele.attrib[to_cmp]:
                    new_ele.append( # Nur die views, oder likes, haben sich verändert.
                        etree.fromstring(
                            hover.format(likes_views = new_ele.attrib[to_cmp],
                            icon_likes_views="coreSpritePlayIconSmall",
                            comments = new_ele.attrib["data-comment"],
                            style_likes_views = add_border,
                            style_comments = "")
                        )
                    )    
                elif new_ele.attrib["data-comment"] != old_ele.attrib["data-comment"]:
                    new_ele.append( # Nur die comments haben sich verändert.
                        etree.fromstring(
                            hover.format(likes_views = new_ele.attrib[to_cmp],
                            icon_likes_views="coreSpritePlayIconSmall",
                            comments = new_ele.attrib["data-comment"],
                            style_likes_views = "",
                            style_comments = add_border)
                        )
                    )

    head[0].append(etree.fromstring(css))
    ig[NEW].write(url)

def compare_tagged(url, ig):
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
