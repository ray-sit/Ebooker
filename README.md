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
from ebooker.main import main

def build_site_list(base_url, chapter_range):
    return [
        f"{base_url}{chapter}"
        for chapter in chapter_range
    ]

config = {
    'sites': build_site_list('https://some-website/book/chapter-', list(range(1, 32))),
    'chrome_driver': "chromedriver.exe",
    'content_div_class': 'reading-content',
    'title': "Book",
    'num_threads': 16,
    'ignore_lines': ['Advertisement']
}
epub_file = main(config)
print(f"Finished! Saved to {epub_file=}")
```

## Example Config File

``` yaml
title: Book Title
sites:
  - https://website.com/some-book/Chapter-1
  - https://website.com/some-book/Chapter-2
  - https://website.com/some-book/Chapter-3
  - https://website.com/some-book/Chapter-4  
chrome_driver: "C:/Users/user/OneDrive/Desktop/chromedriver_win32/chromedriver.exe"
content_div_class: reading-content
num_threads: 8
ignore_lines:
  - Advertisement
```

Note: The tool limits itself to 16 workers maximum. This will be dependant on your own CPU power.

## Future Works
- Better support for specifying bulk number of sites, using regex?
- Add support to also find other html tags, not just div
- Options for varying wait time, to target different (more open vs more protected) online resources
- Option to use basic requests instead of selenium, if selenium isn't needed
- Save scraped data to different (non-HTML) format
- Converting to different non-epub formats as well
- GUI to launch the tool?
- Add build and install so the tool can be launched via cmdline, without calling python
