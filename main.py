import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PyPDF2 import PdfReader
import pandas as pd

from time import sleep

download_dir = f"{os.path.dirname(os.path.realpath(__file__))}/oficial_diare"


def get_oficial_diare():
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
    browser = webdriver.Chrome(options=options)
    browser.get("https://doweb.rio.rj.gov.br/")

    browser.find_element(By.ID, "imagemCapa").click()

    sleep(5)


def read_pdf():
    pdf = open("./oficial_diare/rio_de_janeiro_2023-05-17_completo.pdf", "rb")

    teste = PdfReader(pdf)
    pagina = teste.pages[0]
    content = pagina.extract_text()

    tabela = pd.read_excel("excel/testando.xlsx")
    tabela.to_excel(
        "excel/Diário_Oficial_Cidade_RJ_20230517.xlsx", index=False
    )


# get_oficial_diare()
read_pdf()
