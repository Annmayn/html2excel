from setuptools import setup, find_packages

setup(
    name = "html2excel",
    version = "0.0.1",
    author = "Neema Tsering",
    author_email = "ntvirus333@gmail.com",
    description = ("Convert HTML Table to Excel file"),
    install_requires = ['bs4', 'openpyxl'],
    license = "MIT",
    packages = ["html2excel"],
)