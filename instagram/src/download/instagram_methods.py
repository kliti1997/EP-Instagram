from instagram.data.config import *
from random import randint

# Loggt sich auf Instagram ein.
def login(username, password):
    driver.get(login_url)
    cookie_consent()

    random_sleep(10)

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)

    if driver.find_elements_by_xpath("//*[text()='Log In']"): # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Log In']").click()
    else:
        driver.find_element_by_xpath("//*[text()='Anmelden']").click()

    random_sleep(10)

# Ggf. das cookie consent Fenster akzeptieren.
def cookie_consent():
    if driver.find_element_by_xpath("//*[text()='Akzeptieren']"): # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
    elif driver.find_element_by_xpath("//*[text()='Accept']"): # Existiert es auf englisch?
        driver.find_element_by_xpath("//*[text()='Accept']").click()

# Ändert die relativen links aller img, a und link tags, indem es die
# base_url an die relativen Pfade anhängt.
def convert_links(base_url, soup):
    for img in soup.find_all("img", src=True):
        if not img["src"].startswith("http"):
            img["src"] = urljoin(base_url, img["src"])
    
    for img in soup.find_all("img", srcset=True):
        if not img["srcset"].startswith("http"):
            img["srcset"] = urljoin(base_url, img["srcset"])
    
    for a in soup.find_all("a"):
        if not a["href"].startswith("http"):
            a["href"] = urljoin(base_url, a["href"])
    
    for link in soup.find_all("link"):
        if not link["href"].startswith("http"):
            link["href"] = urljoin(base_url, link["href"])
    #TODO Scripts mit enbinden. Vgl. Marlons .html-Datei
    """ 
    for script in soup.find_all("script", src=True):
        if not script["src"].startswith("http"):
            script["src"] = urljoin(base_url, script["src"])
    # Ändere die relativen Pfade im Source-Code der <script> Tags.
    for script in soup.find_all("script"):
        if script.contents: # not empty?
            find_js = re.findall("/[\w./]*js", script.contents[0])
            find_css = re.findall("/[\w./]*css", script.contents[0])
            script_tmp = script.contents[0]
            for js in find_js:
                script_tmp = script_tmp.replace(js, base_url + js)
                print("js")
            for css in find_css:
                script_tmp = script_tmp.replace(css, base_url + css)
                print("css")
            # Änderungen in der soup-Variable, statt in lokaler Kopie, vornehmen
            print(script_tmp)
            print()
            script.string.replace_with(script_tmp)
    """
# Lade den Html-Code der Beiträge-Seite herunter.
def html_posts(url):
    driver.get(url["href"])
    random_sleep(10)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    convert_links(base_url=base_url, soup=soup)

    f = open(os.path.join(url["monitoring_folder"], "posts.html"), "w")
    f.write(soup.prettify())
    f.close()

# Lade den Html-Code der Beiträge-Seite herunter.
def html_igtv(url):
    driver.get(url["href"] + "channel")
    random_sleep(10)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    convert_links(base_url=base_url, soup=soup)

    f = open(os.path.join(url["monitoring_folder"], "igtv.html"), "w")
    f.write(soup.prettify())
    f.close()

# Lädt den Html-Code der Markiert-Seite herunter
def html_tagged(url):
    driver.get(url["href"] + "tagged")
    random_sleep(10)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    convert_links(base_url=base_url, soup=soup)

    f = open(os.path.join(url["monitoring_folder"], "tagged.html"), "w")
    f.write(soup.prettify())
    f.close()


def random_sleep(max_time):
    # set arbitrary minimum sleep time
    min_time = 3
    if max_time < min_time:
        max_time = min_time + 10
    random_time = randint(3, max_time)
    sleep(random_time)
