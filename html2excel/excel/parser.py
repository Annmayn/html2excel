from bs4 import BeautifulSoup
from html2excel.base.parser import Parser
# from base.parser import Parser
from bs4.element import Tag
from collections import defaultdict

from typing import Dict, List, Tuple, Set, Optional



class ExcelParser(Parser):
    def __init__(self, file_path: str):
        """
        Parameters
        ----------
        file_path : str
                Path where the html file is located
        """
        super().__init__(file_path)

    def set_parsed_cells_to_invalid(self, row_no: int, col_no: int, rowspan: int, colspan: int, valid_cols_for_rows) -> None:
        """
            Sets all iterated cells to False
            Parameters
            ----------
            row_no : int
                    Row number
            col_no : int
                    Column number
            rowspan : int
                    Number of rows the current cell spans
            colspan : int
                    Number of columns the current cell spans
            valid_cols_for_rows : Dict[int, Dict[int, bool | None]]
                    dictionary of dictionary which contains information about the validity of each cell
        """
        rowspan -= 1
        while rowspan >= 0:
            tmp_colspan = colspan - 1
            while tmp_colspan >= 0:
                valid_cols_for_rows[row_no + rowspan][col_no + tmp_colspan] = False
                tmp_colspan -= 1
            rowspan -= 1
    
    def set_neighbor_cells_to_valid(self, row_no, col_no, rowspan, colspan, valid_cols_for_rows):
        """
            sets neighboring cells from current cell to valid
            Parameters
            ----------
            row_no : int
                    Row number
            col_no : int
                    Column number
            rowspan : int
                    Number of rows the current cell spans
            colspan : int
                    Number of columns the current cell spans
            valid_cols_for_rows : Dict[int, Dict[int, bool | None]]
                    dictionary of dictionary which contains information about the validity of each cell

        """ 
        # add bottom cell as valid
        i = row_no + rowspan
        if valid_cols_for_rows[i][col_no] != False:
            valid_cols_for_rows[row_no + rowspan][col_no] = True

        # add side cells as valid
        rowspan_iter = rowspan - 1
        while rowspan_iter >= 0:
            i = row_no + rowspan_iter
            j = col_no + colspan
            if valid_cols_for_rows[i][j] != False:
                valid_cols_for_rows[i][j] = True
            rowspan_iter -= 1
    
    def get_cell_value_map(self, all_data_html: Tag) -> Dict[int, List[Tuple[int, Tag]]]:
        """
            iterates over the html body and creates
            a cell value mapping
            Parameters
            ----------
            all_data_html: Tag
                    Html body
            Returns
            -------
            cell_map_dict : Dict[int, List[Tuple[int, Tag]]]
                    dictionary that maps a row to its corresponding columns and values
        """
        # cell_map_dict = {"1":[(1, 'a'), (2, 'b'), (3,'c'), (4,'d'), (5,'e'), (6,'f')], "2":[(3,'g'),(5,'h'), (6,'i')], "3":[(2,'j')]}
        cell_map_dict = defaultdict(list)
        valid_cols_for_rows: Dict[int, Dict[int, Optional[bool]]] = defaultdict(lambda : defaultdict(lambda: None))
        offset = 0
        for each in all_data_html:
            # respect line breaks if <br> tag is added so as to mimic excel's parsing strategy
            if each.name == 'br':
                offset += 1
            elif each.name == 'table':
                data_rows = self._get_row(each, ["tr"])
                for row_no, row in enumerate(data_rows, 1):
                    row_no += offset
                    columns = self._get_row(row, ["th", "td"])

                    next_col = 1
                    for col in columns:
                        col_no = next_col
                        while not (valid_cols_for_rows[row_no][col_no] or valid_cols_for_rows[row_no][col_no] is None):
                            col_no += 1
                        attrs = col.attrs
                        cell_map_dict[row_no].append((col_no, col))
                        next_col = col_no + 1
                        
                        colspan = int(attrs.get("colspan", 1))
                        rowspan = int(attrs.get("rowspan", 1))
                        self.set_neighbor_cells_to_valid(row_no, col_no, rowspan, colspan, valid_cols_for_rows)
                        self.set_parsed_cells_to_invalid(row_no, col_no, rowspan, colspan, valid_cols_for_rows)
                offset += row_no
        return cell_map_dict
    

    def load_workbook(self):
        data = self._read_file()
        soup = BeautifulSoup(data, features='html5lib')

        all_data_html = soup.html.body.find_all(recursive=False)
        if all_data_html is None:
            raise Exception("No table found")
        
        cell_map_dict = self.get_cell_value_map(all_data_html)
        for row in cell_map_dict:
            for col, tag in cell_map_dict[row]:
                cell_value = self._pre_validate_and_format(row, col, tag)
                self._write_cell(row, col, cell_value)

    def to_excel(self, save_file_path: str) -> None:
        """
            convert html file to excel and save it to a path
            Parameters
            ----------
            save_file_path : str
                    file path where the excel file is saved
        """
        self._save_workbook(save_file_path)
