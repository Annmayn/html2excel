import sys
from html2excel import ExcelParser


def run():
    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        save_path = sys.argv[2]
        parser = ExcelParser(file_path)
        parser.to_excel(save_path)
    else:
        # First argument for file name, we'll ignore that
        print("Expected 2 arguments. Got {num}".format(num=len(sys.argv)-1))


if __name__ == "__main__":
    run()

# TODO: handle exceptions
