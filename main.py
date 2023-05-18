import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PyPDF2 import PdfReader

# import pandas as pd

from time import sleep

# AJUSTAR A DATA AUTOMATICA DEPOIS
PATH_FILE = "./oficial_diare/rio_de_janeiro_2023-05-17_completo.pdf"


def get_oficial_diare():
    URL = "https://doweb.rio.rj.gov.br/"

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

    # Instancia o browser
    browser = webdriver.Chrome(options=options)
    browser.get(URL)

    browser.find_element(By.ID, "imagemCapa").click()

    sleep(5)


def read_pdf(path_file):
    # get_oficial_diare()

    pdf = PdfReader(path_file)

    lista = []

    for index, pdf_pag in enumerate(pdf.pages):
        content = {index + 1: pdf_pag.extract_text()}
        lista.append(content)
    with open("./excel/page_xablau.txt", "a", encoding="utf-8") as txt_file:
        txt_file.write(str(lista))


# 2 - {'atos': 1, 'do': 1, 'prefeito': 1}

# AJUSTAR O NOME DO ARQUIVO AUTOMATICO
#     tabela = pd.read_excel("excel/Diário_Oficial_Cidade_RJ.xlsx")
#     tabela.to_excel(
#         "excel/Diário_Oficial_Cidade_RJ_20230517.xlsx", index=False
#     )


read_pdf(PATH_FILE)
