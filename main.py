import os

import pandas as pd
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
    "EXCEL_FILE": "data_excel/Diário_Oficial_Cidade_RJ.xlsx",
}

PDF_FILE = (
    f"./oficial_diare/rio_de_janeiro_{common_data['date_pdf']}_completo.pdf"
)
EXCEL_FILE_OUTPUT = (
    f"data_excel/Diário_Oficial_Cidade_RJ_{common_data['date_excel']}.xlsx"
)


def get_oficial_diare_data() -> list:
    # Diretório para download do arquivo
    download_dir = f"{os.getcwd()}/oficial_diare"

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


def get_topics(html_path, page_num) -> dict:
    with open(html_path, "r") as file:
        conteudo_html = file.read()

    soup = BeautifulSoup(conteudo_html, "html.parser")

    # Busca todos os topicos da página
    topics = soup.find_all(
        "span", {"style": "font-family: Arial-BoldMT; font-size:14px"}
    )

    # Percorre a lista de tópicos e retorna um dicionário no padrão
    # {"página": [Tópico]}
    topic_dict = {}
    topic_list = []

    for topic in topics:
        topic_list.append(topic.text.rstrip())
        topic_dict[page_num] = topic_list

    os.remove(html_path)
    return topic_dict


def dismember_pdf(pdf_file) -> list:
    file_name = PDF_FILE.replace(".pdf", "")
    output_dir = os.path.join(os.getcwd())

    pdf = PdfReader(pdf_file)

    topics = []

    # Percorre todas as páginas do pdf reescreve cada uma em um arquivo
    # separado e salva na pasta output_dir
    for page_num in range(len(pdf.pages)):
        pdfWriter = PdfWriter()
        pdfWriter.add_page(pdf.pages[page_num])

        with open(
            os.path.join(
                output_dir,
                "{0}_page{1}.pdf".format(file_name, page_num + 1),
            ),
            "wb",
        ) as file_pdf:
            pdfWriter.write(file_pdf)
            file_pdf.close()

        # Chama a função para converter cada página de PDF para HTML
        pdf_to_html(
            os.path.join(
                output_dir,
                "{0}_page{1}.pdf".format(file_name, page_num + 1),
            ),
            "{0}_page{1}.html".format(file_name, page_num + 1),
        )

        # Salva em uma lista todos os dicionários contendo os tópicos
        # de cada página. No padrão {"pagina": [Tópicos]}

        topics.append(
            get_topics(
                "{0}_page{1}.html".format(file_name, page_num + 1),
                page_num + 1,
            )
        )

        print(f"Extraindo dados da página {page_num + 1} por favor aguarde.")

    print("Script finalizado!")
    return list(filter(lambda topic: bool(topic), topics))


def count_words(array) -> str:
    dicionario = {}
    for palavra in array:
        if palavra not in dicionario:
            dicionario[palavra] = 1
        else:
            dicionario[palavra] += 1
    return str(dicionario)


def generate_log() -> None:
    # Cria um log para cada execução do código
    log = open("./log/log.txt", "a")
    log.write(f"- Log: {datetime.today():%d/%m/%Y %H:%M:%S} ")


def excel_report() -> None:
    topics = get_oficial_diare_data()
    tabela = pd.read_excel(common_data["EXCEL_FILE"])

    # Percorre o array de tópicos e adiciona dados na tabela do excel
    for index, topic in enumerate(topics):
        for value in topic.items():
            tabela.loc[index, "Diário Oficial"] = "Cidade do Rio de Janeiro"
            tabela.loc[index, "Títulos Principais"] = ", ".join(value[1])
            tabela.loc[index, "Páginas"] = len(topics)
            tabela.loc[index, "Contagem Total de Títulos da Página"] = len(
                value[1]
            )
            tabela.loc[
                index, "Contagem de Palavras dos Títulos "
            ] = count_words(", ".join(value[1]).split())
            tabela.loc[
                index, "Data de execução"
            ] = f"{datetime.today():%Y_%m_%d_%H_%M_%S}"

    tabela.to_excel(EXCEL_FILE_OUTPUT, index=False)
    generate_log()
    os.remove(PDF_FILE)


excel_report()
