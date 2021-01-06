from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name = "html2excel",
    version = "0.0.2",
    author = "Neema Tsering",
    author_email = "ntvirus333@gmail.com",
    description = ("Convert HTML Table to Excel file"),
    long_description = readme,
    long_description_content_type = "text/markdown",
    install_requires = ['bs4', 'openpyxl'],
    license = "MIT",
    packages = ["html2excel"],
    entry_points = {
        "console_scripts": [
            "html2excel = __main__:main"
        ]
    }
)