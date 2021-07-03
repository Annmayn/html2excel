from bs4.element import Tag
from collections import defaultdict

from typing import List, Union, Iterator, Tuple, Dict, Optional


class BaseParser:
    def __init__(self, file_path: str, enc: str):
        self.file_path = file_path
        self.encoding = enc

    def _read_file(self):
        """
        returns the data contained in a file
        Returns
        -------
        data : bytes
                File stream
        """
        try:
            with open(self.file_path, 'r', encoding=self.encoding) as f:
                data = f.read()
            return data
        except:
            raise Exception("Error while reading input file")

    def _get_row(self, table: Tag, tags: Union[List, str]) -> Iterator[Tag]:
        '''
            reads all tags present inside a parent tag
            and returns a generator
            Parameters
            ----------
            table : Tag
                    parent tag
            tags : List[str] or str
                    tags to search for in parent tag `table`
            Returns
            -------
            iter_tag : Iterator[Tag]
                    Generator consisting of all occurences of `tags` in `table`
        '''
        row_data = table.find_all(tags)
        for each in row_data:
            yield each

    def set_parsed_cells_to_invalid(
        self, row_no: int, col_no: int, rowspan: int, colspan: int, valid_cols_for_rows
    ) -> None:
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

    def set_neighbor_cells_to_valid(
        self, row_no, col_no, rowspan, colspan, valid_cols_for_rows
    ):
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

    def get_cell_value_map(
        self, all_data_html: Tag
    ) -> Dict[int, List[Tuple[int, Tag]]]:
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
        valid_cols_for_rows: Dict[int, Dict[int, Optional[bool]]] = defaultdict(
            lambda: defaultdict(lambda: None)
        )
        offset = 0
        for each in all_data_html:
            # respect line breaks if <br> tag is added so as to mimic excel's parsing strategy
            if each.name == "br":
                offset += 1
            elif each.name == "table":
                data_rows = self._get_row(each, ["tr"])
                for row_no, row in enumerate(data_rows, 1):
                    row_no += offset
                    columns = self._get_row(row, ["th", "td"])

                    next_col = 1
                    for col in columns:
                        col_no = next_col
                        while not (
                            valid_cols_for_rows[row_no][col_no]
                            or valid_cols_for_rows[row_no][col_no] is None
                        ):
                            col_no += 1
                        attrs = col.attrs
                        cell_map_dict[row_no].append((col_no, col))
                        next_col = col_no + 1

                        colspan = int(attrs.get("colspan", 1))
                        rowspan = int(attrs.get("rowspan", 1))
                        self.set_neighbor_cells_to_valid(
                            row_no, col_no, rowspan, colspan, valid_cols_for_rows
                        )
                        self.set_parsed_cells_to_invalid(
                            row_no, col_no, rowspan, colspan, valid_cols_for_rows
                        )
                offset += row_no
        return cell_map_dict

    def _pre_validate_and_format(self, start_row: int, start_col: int, col: Tag) -> str:
        """
            formats cells according to attribute tags/ metadata
            Parameters
            ----------
            start_row : int
                    Start of the row
            start_col : int
                    Start of the column
            col : Tag
                    Cell details including value and metadata
            Returns
            -------
            value: str
                    Cell value
        """
        raise NotImplementedError
            

    

    
