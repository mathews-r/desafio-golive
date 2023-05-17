import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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


get_oficial_diare()
