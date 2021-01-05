# HTML2Excel Documentation
Library to convert HTML Tables to Excel file.


## Usage

```python
from html2excel import ExcelParser

input_file = '/tmp/text_file.html'
output_file = '/tmp/converted_file.xlsx'

parser = ExcelParser(input_file)
parser.to_excel(output_file)
```