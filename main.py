import os
import pandas as pd
import json
from time import sleep
from PyPDF2 import PdfReader
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import io
import pdfminer
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

import json
from pdfminer.converter import TextConverter


# Dados comuns
common_data = {
    "date_excel": f"{datetime.today():%Y%m%d}",
    "date_pdf": f"{datetime.today():%Y-%m-%d}",
    "URL": "https://doweb.rio.rj.gov.br/",
}

PATH_FILE = (
    f"./oficial_diare/rio_de_janeiro_{common_data['date_pdf']}_completo.pdf"
)


def get_oficial_diare() -> None:
    # Diretório para download do arquivo
    download_dir = (
        f"{os.path.dirname(os.path.realpath(__file__))}/oficial_diare"
    )

    # Altera o diretório de download padrão
    options = Options()
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    # Instancia o navegador
    browser = webdriver.Chrome(options=options)
    browser.get(common_data["URL"])

    browser.find_element(By.ID, "imagemCapa").click()

    # Tempo que o browser fica aberto (em segundos)
    sleep(4)


def read_pdf(path_file) -> None:
    # get_oficial_diare()

    # Faz a leitura do PDF
    pdf = PdfReader(path_file)
    number_of_pages = len(pdf.pages)
    teste = pdf.pages[3].extract_text()
    mathews = dict(teste)
    print(mathews)


def pdf_to_html(pdf_path, html_path):
    # Criar um arquivo de saída HTML
    with open(html_path, "wb") as html_file:
        # Configurar o conversor HTML
        resource_manager = PDFResourceManager()
        codec = "utf-8"
        laparams = LAParams()
        converter = HTMLConverter(
            resource_manager, html_file, codec=codec, laparams=laparams
        )

        # Abrir o arquivo PDF de entrada
        with open(pdf_path, "rb") as pdf_file:
            # Configurar o interpretador PDF
            interpreter = PDFPageInterpreter(resource_manager, converter)

            # Converter cada página do PDF para HTML
            for page in PDFPage.get_pages(pdf_file):
                interpreter.process_page(page)


# 2 - {'atos': 1, 'do': 1, 'prefeito': 1}


# tabela = pd.read_excel(
#     f"excel/Diário_Oficial_Cidade_RJ_{common_data['date_excel']}.xlsx"
# )
# tabela.to_excel(
#     f"excel/Diário_Oficial_Cidade_RJ_{common_data['date_excel']}.xlsx",
#     index=False,
# )


def get_topics(html_path):
    with open(html_path, "r") as file:
        conteudo_html = file.read()

    soup = BeautifulSoup(conteudo_html, "html.parser")

    # topics = soup.find_all(
    #     "span", {"style": "font-family: Arial-BoldMT; font-size:14px"}, "a"
    # )
    topics = soup.find_all("a")

    for i in topics:
        print(i.text)
        # with open("./excel/pdf_text.txt", "a", encoding="utf-8") as txt_file:
        #     txt_file.write(i.text)


get_topics("resultado.html")

# read_pdf(PATH_FILE)
