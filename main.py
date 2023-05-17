import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PyPDF2 import PdfReader
import tabula

# import pandas as pd

from time import sleep


def get_oficial_diare():
    URL = "https://doweb.rio.rj.gov.br/"
    download_dir = (
        f"{os.path.dirname(os.path.realpath(__file__))}/oficial_diare"
    )
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
    browser.get(URL)

    browser.find_element(By.ID, "imagemCapa").click()

    sleep(5)


def read_pdf():
    with open(
        "./oficial_diare/rio_de_janeiro_2023-05-17_completo.pdf", "rb"
    ) as pdf_file:
        pdf = PdfReader(pdf_file)

        number_of_pages = len(pdf.pages)

        for page in range(number_of_pages):
            content = pdf.pages[page].extract_text()
            with open(
                f"./excel/page_{page}.txt", "w", encoding="utf-8"
            ) as txt_file:
                txt_file.write(content)


# get_oficial_diare()
read_pdf()
