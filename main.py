from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import os

import os


def get_profile_photo(driver, name):

    driver.get(f"https://www.facebook.com/{name}")
    time.sleep(5)

    # scroll down
    # increase the range to sroll more
    # example: range(0,10) scrolls down 650+ images
    for j in range(0, 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    # target all the link elements on the page
    anchors = driver.find_elements_by_tag_name('a')
    anchors = [a.get_attribute('href') for a in anchors]
    # narrow down all links to image links only
    anchors = [a for a in anchors if str(a).startswith("https://www.facebook.com/photo")]

    driver.get(anchors[1])  # navigate to link
    time.sleep(5)  # wait a bit
    img = driver.find_elements_by_tag_name("img")
    __img = img[18].get_attribute("src")
    return __img


def save_photo(output_path, name, link):

    if "php?" in name:
        name = name[name.find("id=")+3:]
    r = requests.get(link, allow_redirects=True)

    with open(os.path.join(output_path, f'{name.replace(".", "_")}.png'), 'wb') as f:
        f.write(r.content)


def login_to_fb(_username, _password):

    #code by pythonjar, not me
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)

    #specify the path to chromedriver.exe (download and save on your computer)
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("no-sandbox")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless")
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\chrome.exe"
    chrome_driver_binary = r"C:\Projects\fb_scrap\driver\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=chrome_options)


    #open the webpage
    driver.get("http://www.facebook.com")

    #target username
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    #enter username and password
    username.clear()
    username.send_keys(_username)
    password.clear()
    password.send_keys(_password)
    #
    # #target the login button and click it
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    return driver
# #We are logged in!

output_path = r"C:\Projects\fb_scrap\output"

names = ["profile.php?id=100044249088373", "tonde.wadula.92"]


_username = ""
_password = ""

driver = login_to_fb(_username, _password)
for name in names:

    print(f"Scrapping {name} photo")
    link = get_profile_photo(driver, name)
    save_photo(output_path, name, link)

