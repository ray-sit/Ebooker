import argparse
import yaml
from pathlib import Path
from ebooker.scraper import scrape
from ebooker.converter import convert_to_epub
from ebooker.packager import BookHTML


parser = argparse.ArgumentParser(description="Scrape Websites and convert into EBook")
parser.add_argument("ScrapeConfig", type=str)


def load_yaml_config(config_file_path: Path) -> dict:
    with open(config_file_path, "r") as fd:
        return yaml.safe_load(fd)


def parse_cli_config() -> dict:
    args = parser.parse_args()
    config_file_path = Path(args.ScrapeConfig)
    return load_yaml_config(config_file_path)


def main(config: dict) -> str:
    scraped_data = scrape(config['sites'], config['chrome_driver'], config['content_div_class'], config['num_threads'])
    doc = BookHTML(title=config['title'], data=scraped_data, ignore_lines=config['ignore_lines'])
    html_doc_file = doc.save_to_file()
    return convert_to_epub(html_doc_file)
