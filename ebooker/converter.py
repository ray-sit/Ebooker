import tempfile
from pypandoc import convert_file


def convert_to_epub(html_file: str) -> str:
    print("Converting HTML to EPUB...")
    output_epub = html_file.replace('.html', '.epub')
    convert_file(
        html_file,
        'epub',
        outputfile=output_epub,
    )
    return output_epub
