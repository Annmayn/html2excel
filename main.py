import os
import sys
from html2excel import ExcelParser

# SAMPLE CODE
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        save_path = sys.argv[2]
    # file_path = os.path.join(os.getcwd(), "tmp", "html_file.html")
    # save_path = os.path.join(os.getcwd(), "tmp", "trial.xlsx")

    parser = ExcelParser(file_path)
    parser.to_excel(save_path)

# TODO: handle exceptions
