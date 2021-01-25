from openpyxl import Workbook

from typing import List, Union, Iterator, Tuple
from bs4.element import Tag


class Parser:
    def __init__(self, file_path):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.file_path = file_path
        self.load_workbook()

    def load_workbook(self):
        raise NotImplemented

    def _read_file(self):
        """
        returns the data contained in a file
        """
        try:
            with open(self.file_path, 'r') as f:
                data = f.read()
            return data
        except:
            raise Exception("Error while reading input file")

    def _get_row(self, table: Tag, tags: Union[List, str]) -> Iterator[Tag]:
        row_data = table.find_all(tags)
        for each in row_data:
            yield each

    def _pre_validate_and_format(self, i: int, j: int, col: Tag) -> Tuple[int, str]:
        attrs = col.attrs
        end = j
        if "colspan" in attrs:
            colspan = int(attrs.get("colspan", 1))
            end += colspan - 1
            self.ws.merge_cells(start_row=i, end_row=i,
                                start_column=j, end_column=end)
        # TODO: Handle bold, italics and other attributes
        end += 1
        return (end, col.text.strip())

    def _write_cell(self, row, col, val) -> None:
        self.ws.cell(row=row, column=col).value = val

    def get_workbook(self) -> Workbook:
        return self.wb

    def _save_workbook(self, loc) -> bool:
        try:
            self.wb.save(loc)
            return True
        except:
            return False
