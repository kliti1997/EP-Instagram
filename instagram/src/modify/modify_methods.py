from instagram.data.config import *
from lxml import etree, html


# from instagram.src.instagram import Instagram


def compare_posts():
    old_html_url = "instagram/data/files/polizei.hannover/posts/old.html"
    new_html_url = "instagram/data/files/polizei.hannover/posts/new.html"
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
            parent.attrib["style"] = "border: 5px solid green;"
            print(etree.tostring(parent))
            print("New link: " + new_links_list[index])

    open("aaa.html", "wb").write(etree.tostring(new_tree, method="html"))


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
    oldElements = list(oldDoc.iter("a"))
    oldFollowingElement = [element for element in oldElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/polizei.hannover/following/"][0]
    oldSubElement = list(oldFollowingElement.iter())
    oldFollowingCnt = [element.text for element in oldSubElement if element.tag == "span"][0]

    newElements = list(newDoc.iter("a"))
    newFollowingElement = [element for element in newElements if element.tag == "a" and element.attrib['href'] == "https://www.instagram.com/polizei.hannover/following/"][0]
    newSubElement = list(newFollowingElement.iter())
    newFollowingCnt = [element.text for element in newSubElement if element.tag == "span"][0]
                
    if oldFollowingCnt != newFollowingCnt:
        newFollowingElement.attrib['style'] = "border: 4px solid green;"
    
    outputHtml = etree.tostring(newDoc, method="html")

    return outputHtml


def compare_igtv():
    old_html_url = "instagram/data/files/polizei.hannover/igtv/old.html"
    new_html_url = "instagram/data/files/polizei.hannover/igtv/new.html"
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
            new_igtv_a_list[index].attrib["style"] = "border: 5px solid green;"
            print("New link: ")
            print(etree.tostring(new_igtv_a_list[index]))

    open("igtv.html", "wb").write(etree.tostring(new_tree, method="html"))
