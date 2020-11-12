from instagram.data.config import *

# Loggt sich auf Instagram ein.
def login(username, password):
    driver.get(login_url)
    cookie_consent()

    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)

    if driver.find_elements_by_xpath("//*[text()='Log In']"): # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Log In']").click()
    else:
        driver.find_element_by_xpath("//*[text()='Anmelden']").click()

# Ggf. das cookie consent Fenster akzeptieren.
def cookie_consent():
    if driver.find_element_by_xpath("//*[text()='Akzeptieren']"): # Existiert as Element auf deutsch?
        driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
    elif driver.find_element_by_xpath("//*[text()='Accept']"): # Existiert es auf englisch?
        driver.find_element_by_xpath("//*[text()='Accept']").click()

# Lade den Html-Code der Beiträge-Seite herunter.
def html_posts(url):
    driver.get(url["href"])
    content = driver.page_source
    soup = BeautifulSoup(content)

    f = open(url["monitoring_folder"]+ "/posts.html", "w")
    f.write(soup.prettify())
    f.close()

login(ig_credentials["user"], ig_credentials["pass"])
for url in monitoring_map["instagram"]:
    html_posts(url)