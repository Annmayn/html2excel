# HTML2Excel Documentation
Library to convert HTML Tables to Excel file.

While libraries like pandas do read html files, they often don't work with merged cells and line breaks.
This library was created with the sole intention of converting HTML tables to Excel files
as they're seen while opening them with softwares such as MS Excel and LibreOffice. 

A sample flask host code is provided [in this link](https://github.com/Annmayn/sample-host-html2excel)

## Installation
```pip install html2excel```


## Usage

### Running from command line

```python -m html2excel input_file output_file```

### Using as package
```python
from html2excel import ExcelParser

input_file = '/tmp/text_file.html'
output_file = '/tmp/converted_file.xlsx'

parser = ExcelParser(input_file)
parser.to_excel(output_file)
```