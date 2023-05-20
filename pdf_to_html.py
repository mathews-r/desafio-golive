import os
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def pdf_to_html(pdf_path, html_path) -> None:
    # Cria um arquivo HTML com configurações padrões
    with open(html_path, "wb") as html_file:
        resource_manager = PDFResourceManager()
        codec = "utf-8"
        laparams = LAParams()
        converter = HTMLConverter(
            resource_manager, html_file, codec=codec, laparams=laparams
        )

        with open(pdf_path, "rb") as pdf_file:
            interpreter = PDFPageInterpreter(resource_manager, converter)

            # Converte cada página do PDF para HTML
            for page in PDFPage.get_pages(pdf_file):
                interpreter.process_page(page)

    os.remove(pdf_path)
