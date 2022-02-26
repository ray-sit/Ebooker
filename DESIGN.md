# Ebooker

The tool will have 2 essential modules
1. Web Scraper
2. Doc Generator

User Gives Websites -> Web Scraper gets HTML of Websites -> HTML is processed to only keep necessary lines -> Ran through PyPandoc to reformat from HTML to EPUB -> Save to File

## Web Scraper

The web scraper shall be a simple tool that can be called and given:
- Website/List of Websites
- Config File to configure how the Web scraper behaves and processes HTML data
  - recursive - tells scraper to recursively pull text from other links in website/s provided
  - tags to include - explicitly defines what HTML tags to include (default saves all if empty, acts as allow-list if not empty)
  - tags to ignore - explicitly defines what HTML tags to ignore (acts as block list, overrides the allow-list if specified)

And return a file/sum of all scraped text data.

Some Pseudo-code
```
def scrape_web(websites: list, scrape_conf: dict):
    result = temp_file()

    for website in websites:
        get_html(website)
        processed_html = parse_html(website, scrape_conf)
        result.write(processed_html)
    
    return result
```


## Doc Generator

The tool shall simply take in HTML formatted text/file and any additional config to transform into EPUB format.
This will rely on pypandoc.

Some Pseudo-code
```
import pypandoc

def generate_doc(raw_html: str/file, pandoc_extra_args):
    converted = pypandoc.convert_text(  # or convert_file
        raw_html,
        'epub',  # output format
        format='html',  # input format
        # Any extra args
        extra_args=[...]
    )
    
    save_to_file(converted)

```
