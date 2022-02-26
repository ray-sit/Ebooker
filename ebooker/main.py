import argparse
import yaml
from pathlib import Path
from ebooker.scraper import scrape
from ebooker.converter import convert_to_epub

parser = argparse.ArgumentParser(description="Scrape Websites and convert into EBook")
parser.add_argument("ScrapeConfig", type=str)


def load_yaml_config(config_file_path: Path):
    with open(config_file_path, "r") as fd:
        return yaml.safe_load(fd)


def main():
    args = parser.parse_args()
    config_file_path = Path(args.ScrapeConfig)
    config = load_yaml_config(config_file_path)
    html_doc = scrape(**config)
    html_doc_file = html_doc.save_to_file()
    epub_file = convert_to_epub(html_doc_file)
    print(f"Finished! Saved to {epub_file=}")

