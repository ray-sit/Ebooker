import concurrent.futures
from selenium import webdriver

MAX_THREADS = 16
# Initialise options to run in headless mode - this saves alot of CPU and GPU
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--window-size=1920,1080")
OPTIONS.add_argument("--headless")
OPTIONS.add_argument("--disable-gpu")
OPTIONS.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")


def scrape(sites: list, chrome_driver: str, content_div_class: str, num_threads: int = MAX_THREADS) -> dict:
    """ Scrapes data from given list of sites, using selenium chrome driver in headless mode.
        Multithreading is used to speed up process.

    config keywords:
        sites (list) - list of sites to scrape
        chrome_driver (str) - list of sites to scrape
        content_div_class (str) - the main div class to save data for
        num_threads (int) - Number of processing threads to use
    Returns:
        data (dict) - map of scraped data sites
    """
    num_threads = max(min(num_threads, MAX_THREADS), 1)
    print(f"Scraping {len(sites)} Sites with {num_threads} Worker Threads")

    # initiate data buffer
    data = {  
        site: None for site in sites
    }

    # Retrieve a single page and report the URL and contents
    def scrape_page(url):
        print(f"Scraping Page - {url}")
        driver = webdriver.Chrome(
            executable_path=chrome_driver,
            options=OPTIONS
        )
        driver.get(url)
        content = driver.find_elements_by_xpath(f"//div[@class='{content_div_class}']")
        paragraphs = [
            content[p].text
            for p in range(len(content))
        ]
        driver.close()
        return paragraphs

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        execution_map = {
            executor.submit(scrape_page, site): site
            for site in sites
        }
        for future in concurrent.futures.as_completed(execution_map):
            data[execution_map[future]] = future.result()  # Saves data to buffer as each task completes

    print("Web Scrape Complete!")
    return data
