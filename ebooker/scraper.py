import datetime
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ebooker.html import HTMLDoc

LOAD_BUFFER = 5
MIN_WAIT = 0.5
MAX_WAIT = 2


def eta(sites_remaining: int) -> str:

    def addSecs(tm, secs):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + datetime.timedelta(seconds=secs)
        return fulldate.time()

    min_eta_secs = sites_remaining * (MIN_WAIT + LOAD_BUFFER)
    max_eta_secs = sites_remaining * (MAX_WAIT + LOAD_BUFFER)
    current_time = datetime.datetime.now().time()
    predicted_min = addSecs(current_time, min_eta_secs)
    predicted_max = addSecs(current_time, max_eta_secs)

    return f"{predicted_min} - {predicted_max} ({min_eta_secs} - {max_eta_secs} seconds) [Current Time: {current_time}]"


def scrape(sites: list, chrome_driver: str, title: str = "Book", content_div_class: str) -> str:
    """  Scrapes data
    config keywords:
        sites (list) - list of sites to scrape
        chrome_driver (str) - list of sites to scrape
        title (str) - title to save files as
        content_div_class (str) - the main div class to save data for
    """

    doc = HTMLDoc(title=title)
    sites_remaining = len(sites)
    print(f"Starting Web Scrape - ETA: {eta(sites_remaining)} seconds ({sites_remaining} remaining)")

    for site in sites:
        print(f"Scraping {site=} - ETA: {eta(sites_remaining)} ({sites_remaining} remaining)")
        driver = webdriver.Chrome(chrome_driver)
        driver.get(site)

        # GET CONTENT
        content = driver.find_elements_by_xpath(f"//div[@class='{content_div_class}']")
        paragraphs = [
            content[p].text
            for p in range(len(content))
        ]

        for para_num, paragraph in enumerate(paragraphs):
            for line_num, line in enumerate(paragraph.split('\n')):
                if para_num == 0 and line_num == 0:  # Use the first line of the site as the chapter heading
                    doc.add_header(line)
                else:
                    doc.add_line(line)

        driver.close()
        driver = None
        sites_remaining -= 1
        # Imitate real world, pause for random number of seconds, ranging from 3-10
        sleep_time = randint(MIN_WAIT, MAX_WAIT)
        print(f"Wating {sleep_time} seconds...")
        sleep(sleep_time)

    print("Web Scrape Complete!")
    return doc
