# Ebooker

A simple tool to scrape websites and save them into EPUB format

## Setting Up

Install python requirements
```
pip install -r requirements.txt
```

There are a couple of non-python package requirements:

### Pandoc

Install pandoc, can use the pypandoc provided download function:
```python
# expects an installed pypandoc: pip install pypandoc
from pypandoc.pandoc_download import download_pandoc
# see the documentation how to customize the installation path
# but be aware that you then need to include it in the `PATH`
download_pandoc()
```

### ChromeDriver (for Selenium)

Selenium requires a chromedriver, to run chromium.

Check for your version of Chrome (Top right dotted button - Help - About Google Chrome) 
and download the corresponding ChromeDriver from https://chromedriver.chromium.org/downloads

After downloading, unzip and note down the path to the .exe, this needs to be specified
in the Ebooker config file.

## Running

Can either run CLI and specify the path to the Ebooker Config File:
```
python -m ebooker [PATH TO CONFIG FILE]
```

Or use directly in python script:
```python
from ebooker.scraper import scrape
from ebooker.converter import convert_to_epub

# Specify config
config = {
    'sites': ['Some list of websites to scrape'],
    'chrome_driver': "Path to Chrome Driver",
    'content_div_class': 'Div Class to Find',
    'title': "Book Title"
}
html_doc = scrape(**config)
html_doc_file = html_doc.save_to_file()
epub_file = convert_to_epub(html_doc_file)
print(f"Finished! Saved to {epub_file=}")
```

## Config File

The config file is a Yaml file, currently this is only used for the scrape function.

Example Config:
``` yaml
title: Book Title
sites:
  - https://site/ddd
  - https://site/123
chrome_driver: "chromedriver.exe"
content_div_class: reading-content
```

The scrape function header:
``` python
def scrape(sites: list, chrome_driver: str, title: str = "Book", content_div_class: str) -> str:
    """  Scrapes data
    config keywords:
        sites (list) - list of sites to scrape
        chrome_driver (str) - list of sites to scrape
        title (str) - title to save files as
        content_div_class (str) - the main div class to save data for
    """
```

## Future Works
- Better support for specifying bulk number of sites, using regex?
- Add support to also find other html tags, not just div
- Multithreading support to improve scraping speed and reduce runtime
- Options for varying wait time, to target different (more open vs more protected) online resources
- Option to use basic requests instead of selenium, if selenium isn't needed
- Save scraped data to different (non-HTML) format
- Converting to different non-epub formats as well
- GUI to launch the tool?
- Add build and install so the tool can be launched via cmdline, without calling python
