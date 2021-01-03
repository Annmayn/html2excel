from openpyxl import Workbook
from bs4 import BeautifulSoup
import re

from typing import List, Union, Iterator, Tuple
from bs4.element import Tag

from base.parser import Parser


class ExcelParser(Parser):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def to_excel(self, save_file_path: str, ignore_merged_row: bool = True) -> bool:
        # TODO: handle case when rows are merged
        data = self.read_file()
        soup = BeautifulSoup(data, features='html.parser')
        table_data = self.get_table_data(soup)
        data_rows = self.get_row(table_data, ["tr"])
        for i, row in enumerate(data_rows, 1):
            columns = self.get_row(row, ["th", "td"])
            next_j = 1
            for j, col in enumerate(columns, 1):
                j = next_j
                next_j, col_data = self.pre_validate_and_format(i, j, col)
                self.write_cell(i, j, col_data)

        self.save_workbook(save_file_path)
