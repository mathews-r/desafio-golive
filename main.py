import os
import pandas as pd
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PyPDF2 import PdfReader


date_excel = f"{datetime.today():%Y%m%d}"
date_pdf = f"{datetime.today():%Y-%m-%d}"
PATH_FILE = f"./oficial_diare/rio_de_janeiro_{date_pdf}_completo.pdf"
URL = "https://doweb.rio.rj.gov.br/"


def get_oficial_diare():
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

    # Tempo que o browser fica aberto (em segundos)
    sleep(5)


def read_pdf(path_file) -> None:
    get_oficial_diare()

    # Faz a leitura do PDF
    pdf = PdfReader(path_file)
    number_of_pages = len(pdf.pages)

    print(pdf.metadata.creation_date)

    topics_list = []

    # Percorre as páginas, extrai os textos e transforma em um array
    for page in range(number_of_pages):
        content = pdf.pages[page].extract_text()
        data = content.split("\n")

        # Percorre a nova lista, verifica se esta em Uppercase e adiciona
        #  o novo dict no array topic_list
        for topics in data:
            if topics.isupper():
                topic_dict = {f"{page + 1}": topics}
                topics_list.append(topic_dict)

    # Filtra o resultado e pega somente os valores que foram duplicados
    filter_repeated(topics_list)


# 2 - {'atos': 1, 'do': 1, 'prefeito': 1}


def filter_repeated(list_dicts) -> None:
    ocurrences = {}
    repeated_values = []

    for dicts in list_dicts:
        for value in dicts.values():
            if value in ocurrences:
                if ocurrences[value] == 1:
                    repeated_values.append({f"{list(dicts.keys())[0]}": value})
                ocurrences[value] += 1
            else:
                ocurrences[value] = 1
    with open("./excel/pdf_text.txt", "a", encoding="utf-8") as txt_file:
        txt_file.write(str(repeated_values))
    tabela = pd.read_excel(f"excel/Diário_Oficial_Cidade_RJ_{date_excel}.xlsx")
    tabela.to_excel(
        f"excel/Diário_Oficial_Cidade_RJ_{date_excel}.xlsx", index=False
    )


# Exemplo de uso
read_pdf(PATH_FILE)
