#!/bin/python3
import requests
import os
import pathlib
from bs4 import BeautifulSoup
from datetime import datetime

# Define the URL of the Mailman archive
url = "https://mailman.suse.de/pipermail/canteen/" 
downloads_dir = "./downloads"
pdfs_dir = "./pdfs"

pdf_mapping = {} # {"$YEAR_$CW": "pdfPath"}


def getPDFFromDate(date):
    pass


def main():
    # downloadArchiveTxt()
    # downloadMenuPDFs()
    parseAndMapPDFs()
    print(dateToPDF(datetime.now()))


def dateToPDF(date: datetime):
    return pdf_mapping[dateToCWYearString(date)]


def parseAndMapPDFs():
    date_format = '%d_%m_%Y'
    for pdf_file in pathlib.Path(pdfs_dir).glob("*.pdf"):
        pdf_file_str = str(pdf_file)
        pdf_file_str = pdf_file_str[5:pdf_file_str.index("_1.pdf")]
        dateRange = pdf_file_str.split("_bis_")
        pdf_mapping[dateToCWYearString(datetime.strptime(
            dateRange[0], date_format))] = pdf_file
        pdf_mapping[dateToCWYearString(datetime.strptime(
            dateRange[1], date_format))] = pdf_file


def dateToCWYearString(date: datetime):
    return f"{date.year}_{date.isocalendar().week}"


def downloadMenuPDFs():
    for txt_file in pathlib.Path(downloads_dir).glob('*.txt'):
        print(f"Reading PDFs for: {txt_file}")
        with open(txt_file, "r+") as file:
            lastFileName = ""
            for line in file:
                if line.startswith("Name: "):
                    lastFileName = line.split(" ")[1]

                if line.startswith("URL: "):
                    attachmentUrl = line[line.index("<")+1:line.index(">")]
                    if attachmentUrl.endswith("pdf"):
                        os.system(
                            f"curl {attachmentUrl} --output {pdfs_dir}/" + lastFileName)

        file.close()


def downloadArchiveTxt():
    # Make a request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.text

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table with the archives
    table = soup.find("table", border="3")

    # Loop through each row in the table
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        archive_file = cells[2].find("a")["href"]

        print(archive_file)
        # Download the archive file
        archive_response = requests.get(url + archive_file)
        with open(f"{downloads_dir}/{archive_file}", "wb") as file:
            file.write(archive_response.content)

    os.system('gunzip --keep -f ' + f"{downloads_dir}/*.gz")


if __name__ == "__main__":
    main()
