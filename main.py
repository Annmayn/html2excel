import os

from excel.parser import ExcelParser

# SAMPLE CODE
file_path = os.path.join(os.getcwd(), "tmp", "html_file.html")
save_path = os.path.join(os.getcwd(), "tmp", "trial.xlsx")
parser = ExcelParser(file_path)
parser.to_excel(save_path)

# TODO: handle exceptions
