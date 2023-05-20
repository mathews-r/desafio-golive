from datetime import datetime

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
