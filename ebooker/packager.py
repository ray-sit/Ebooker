from enum import Enum
from secrets import token_hex


class Format(Enum):
    HTML = "html"


class HtmlSection(Enum):
    TITLE = "h1"
    HEADING = "h2"
    TEXT = "p"


class Book:
    def __init__(self, title: str, data: dict, format: Format, ignore_lines: list = []):
        self._title = title
        self._data = data
        self._path = f"{title}.{token_hex(8)}.{format.value}"
        self._format = format
        self._ignore_list = [
            line.lower()
            for line in ignore_lines
        ]
        self.package_into_book()

    @property
    def path(self) -> str:
        return self._path

    def _in_ignore_list(self, line):
        return any([
            ignore_line in line.lower()
            for ignore_line in self._ignore_list
        ])

    def _write_to_html(self):
        chapter_number = 1
        with open(self._path, 'w') as output_file:

            def write(text, section: HtmlSection):
                try:
                    output_file.write(f'<{section.value}>{text}</{section.value}>')
                except Exception as ex:
                    print(f"Failed to write - {text}\n{ex}")

            write(self._title, HtmlSection.TITLE)

            for chapter in self._data.values():
                # Some chapters have repeated html text
                # This adds some trackers to skip repeated chapters
                # and only adds it once to the book
                chapter_header = None
                reached_end = False

                for paragraphs in chapter:
                    for line in paragraphs.split('\n'):  # Each paragraph is read '\n' separated
                        if self._in_ignore_list(line) or reached_end:
                            continue

                        if chapter_header is None:  # First line of a chapter is always taken as the heading
                            chapter_header = line if line.lower().startswith('chapter') else f"Chapter {chapter_number}"
                            write(chapter_header, HtmlSection.HEADING)
                            if line.lower().startswith('chapter'):
                                continue

                        if chapter_header == line:  # If the header ever repeats we know we have reached the end of the chapter
                            reached_end = True
                            continue

                        write(line, HtmlSection.TEXT)

                chapter_number += 1

    def package_into_book(self):
        packager_map = {
            Format.HTML: self._write_to_html
        }
        print(f"Packaging Scraped Data into {self._format.name} Book")
        packager_map[self._format]()
        print("Packaging Finished.")


class HtmlBook(Book):
    def __init__(self, title: str, data: dict, ignore_lines: list = []):
        super().__init__(
            title=title,
            data=data,
            format=Format.HTML,
            ignore_lines=ignore_lines
        )
