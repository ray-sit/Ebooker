from secrets import token_hex

class HTMLDoc:
    def __init__(self, title: str):
        self.__data = ""
        self._title = title
        self.add_title(self._title)
    
    def prepend(self, text):
        self.__data = f'{text}\n{self.__data}'

    def add_title(self, title):
        self.prepend(f"<h1>{title}<h1>")

    def add_header(self, header: str):
        self.__data += f"<h2>{header}</h2>\n"

    def add_line(self, line: str):
        self.__data += f"<p>{line}</p>\n"

    def bulk_add_content(self, content: list):
        for paragraph in content:
            for line in paragraph.split('\n'):
                self.add_line(line)

    def data(self) -> str:
        return self.__data

    def save_to_file(self, file_path: str = "") -> str:
        print("Saving HTML to File...")
        if not file_path:
            file_path = f"{self._title}.{token_hex(4)}.html"
        with open(file_path, "w") as fd:
            fd.write(self.__data)
        return file_path
