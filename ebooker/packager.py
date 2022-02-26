from secrets import token_hex


class BookHTML:
    def __init__(self, title: str, data: dict = {}, ignore_lines: list = []):
        self.__data = ""
        self._title = title
        self._ignore_list = [
            line.lower()
            for line in ignore_lines
        ]
        self.add_title(self._title)
        if data:
            self.add_book(data)

    def _in_ignore_list(self, line):
        return any([
            ignore_line in line.lower()
            for ignore_line in self._ignore_list
        ])

    def add_book(self, book_map: dict, ignore_lines: list = []):
        """ Adds a 'book' as a dictionary of chapters.
            Dictionary is assumed to be ordered.
        """
        self._ignore_list += [
            line.lower()
            for line in ignore_lines
        ]
        chapter_number = 1
        for chapter_url, chapter in book_map.items():
            # Some chapters have repeated html text
            # This adds some trackers to skip repeated chapters
            # and only adds it once to the book
            chapter_header = None
            reached_end = False

            for paragraphs in chapter:
                for line in paragraphs.split('\n'):  # Each paragraph is read '\n' separated
                    if self._in_ignore_list(line):
                        continue

                    if chapter_header is None:  # First line of a chapter is always taken as the heading
                        if line.lower().startswith('chapter'):
                            chapter_header = line
                            self.add_header(line)
                            continue
                        else:
                            chapter_header = f"Chapter {chapter_number}"
                            self.add_header(chapter_header)

                    if chapter_header == line:  # If the header ever repeats we know we have reached the end of the chapter
                        reached_end = True

                    if reached_end:  # And can skip any line that comes after
                        continue

                    self.add_line(line)

            chapter_number += 1

    def prepend(self, text):
        self.__data = f'{text}\n{self.__data}'

    def add_title(self, title):
        self.prepend(f"<h1>{title}<h1>")

    def add_header(self, header: str):
        self.__data += f"<h2>{header}</h2>\n"

    def add_line(self, line: str):
        self.__data += f"<p>{line}</p>\n"

    def data(self) -> str:
        return self.__data

    def save_to_file(self, file_path: str = "") -> str:
        print("Saving HTML to File...")
        if not file_path:
            file_path = f"{self._title}.{token_hex(4)}.html"
        with open(file_path, "w") as fd:
            fd.write(self.__data)
        return file_path
