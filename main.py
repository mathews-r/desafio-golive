import os

# import pandas as pd
from time import sleep
from datetime import datetime

# Importações para trabalhar com PDF
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

# Importações para trabalhar com o scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Dados comuns
common_data = {
    "date_excel": f"{datetime.today():%Y%m%d}",
    "date_pdf": f"{datetime.today():%Y-%m-%d}",
    "URL": "https://doweb.rio.rj.gov.br/",
}

PDF_FILE = (
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

    return dismember_pdf(PDF_FILE)


def pdf_to_html(pdf_path, html_path) -> None:
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
    os.remove(pdf_path)


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

    # Busca todos os topicos da página
    topics = soup.find_all(
        "span", {"style": "font-family: Arial-BoldMT; font-size:14px"}
    )

    # Busca o número da página
    page = soup.find(
        "span",
        {"style": "font-family: Arial-BoldMT; font-size:12px"},
    )

    # Percorre a lista de tópicos e retorna um dicionário no padrão

    topic_dict = {}

    for topic in topics:
        topic_list = []
        topic_list.append(topic.text.rstrip())
        topic_dict[page.text.rstrip()] = topic_list

    os.remove(html_path)
    return topic_dict


# --------------------------------------------------------------


def dismember_pdf(pdf_file):
    file_base_name = PDF_FILE.replace(".pdf", "")
    output_dir = os.path.join(os.getcwd())

    pdf = PdfReader(pdf_file)

    # Percorre todas as páginas do pdf reescreve cada uma em um arquivo
    # separado e salva na pasta output_dir
    topics = []

    for page_num in range(len(pdf.pages)):
        pdfWriter = PdfWriter()
        pdfWriter.add_page(pdf.pages[page_num])

        with open(
            os.path.join(
                output_dir,
                "{0}_page{1}.pdf".format(file_base_name, page_num + 1),
            ),
            "wb",
        ) as file_pdf:
            pdfWriter.write(file_pdf)
            file_pdf.close()

        # Chama a função para converter cada página de PDF para HTML
        pdf_to_html(
            os.path.join(
                output_dir,
                "{0}_page{1}.pdf".format(file_base_name, page_num + 1),
            ),
            "{0}_page{1}.html".format(file_base_name, page_num + 1),
        )

        # Salva em uma lista todos os dicionários contendo os tópicos
        # de cada página
        topics.append(
            get_topics("{0}_page{1}.html".format(file_base_name, page_num + 1))
        )

        with open("./excel/pdf_text.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(str(topics))
        print(f"Extraindo dados da página {page_num} por favor aguarde.")

    print("Script finalizado!")
    return topics


get_oficial_diare()
