from bs4 import BeautifulSoup
from html2excel.base.parser import Parser


class ExcelParser(Parser):
    def __init__(self, file_path: str):
        super().__init__(file_path)

    def load_workbook(self):
        data = self._read_file()
        soup = BeautifulSoup(data, features='html.parser')
        table_data = soup.table
        if table_data is None:
            raise Exception("No table found")
        data_rows = self._get_row(table_data, ["tr"])
        for i, row in enumerate(data_rows, 1):
            columns = self._get_row(row, ["th", "td"])
            next_j = 1
            for j, col in enumerate(columns, 1):
                j = next_j
                next_j, col_data = self._pre_validate_and_format(i, j, col)
                self._write_cell(i, j, col_data)

    def to_excel(self, save_file_path: str, ignore_merged_row: bool = True) -> bool:
        # TODO: handle case when rows are merged
        self._save_workbook(save_file_path)
