import sys
import argparse
from html2excel.excel.parser import ExcelParser


def run():
    argparser = argparse.ArgumentParser(description="Convert HTML files to excel")
    argparser.add_argument("input_path", type=str, help="HTML file location")
    argparser.add_argument("output_path", type=str, help="Excel file save path")
    argparser.add_argument(
        "--enc",
        type=str,
        default="utf-8",
        help="Encoding to use while reading HTML file",
    )

    args = argparser.parse_args()

    parser = ExcelParser(file_path=args.input_path, enc=args.enc)
    parser.to_excel(args.output_path)


if __name__ == "__main__":
    run()
