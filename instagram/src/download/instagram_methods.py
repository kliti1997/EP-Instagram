from instagram.data.config import *

# Loggt sich auf Instagram ein.
def login(username, password):
    driver.get(login_url)
    cookie_consent()

    #TODO Zufahlswert generieren
    sleep(1)

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)

    if driver.find_elements_by_xpath("//*[text()='Log In']"): # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Log In']").click()
    else:
        driver.find_element_by_xpath("//*[text()='Anmelden']").click()

    #TODO Zufahlswert generieren
    sleep(4)

# Ggf. das cookie consent Fenster akzeptieren.
def cookie_consent():
    if driver.find_element_by_xpath("//*[text()='Akzeptieren']"): # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
    elif driver.find_element_by_xpath("//*[text()='Accept']"): # Existiert es auf englisch?
        driver.find_element_by_xpath("//*[text()='Accept']").click()

# Lade den Html-Code der Beiträge-Seite herunter.
def html_posts(url):
    driver.get(url["href"])
    #TODO Zufahlswert generieren
    sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content)

    convert_links(base_url=base_url, soup=soup)

    f = open(os.path.join(url["monitoring_folder"], "posts.html"), "w")
    f.write(soup.prettify())
    f.close()

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

# ------ Funktionsaufrufe zum testen ------
login(ig_credentials["user"], ig_credentials["pass"])
for url in monitoring_map["instagram"]:
    html_posts(url)
driver.quit()