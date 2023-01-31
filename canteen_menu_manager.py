#!/bin/python3
import requests
import os
import pathlib
from bs4 import BeautifulSoup
from datetime import datetime

# Define the URL of the Mailman archive
url = "https://mailman.suse.de/pipermail/canteen/" 
downloadsDir = "./downloads"
pdfsDir = "./pdfs"

calendarWeekToMealPlanDict = {}

# {"$YEAR_$CW": "pdfPath"}
pdfMapping = {}


def getPDFFromDate(date):
    pass


def main():
    # downloadArchiveTxt()
    # downloadMenuPDFs()
    parseAndMapPDFs()
    print(dateToPDF(datetime.now()))


def dateToPDF(date: datetime):
    return pdfMapping[dateToCWYearString(date)]


def parseAndMapPDFs():
    # pdfs/16_01_2023_bis_29_01_2023_1.pdf
    date_format = '%d_%m_%Y'
    for pdf_file in pathlib.Path(pdfsDir).glob("*.pdf"):
        pdf_file_str = str(pdf_file)
        pdf_file_str = pdf_file_str[5:pdf_file_str.index("_1.pdf")]
        dateRange = pdf_file_str.split("_bis_")
        pdfMapping[dateToCWYearString(datetime.strptime(
            dateRange[0], date_format))] = pdf_file
        pdfMapping[dateToCWYearString(datetime.strptime(
            dateRange[1], date_format))] = pdf_file


def dateToCWYearString(date: datetime):
    return f"{date.year}_{date.isocalendar().week}"


def downloadMenuPDFs():
    for txt_file in pathlib.Path(downloadsDir).glob('*.txt'):
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
                            f"curl {attachmentUrl} --output {pdfsDir}/" + lastFileName)

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
        with open(f"{downloadsDir}/{archive_file}", "wb") as file:
            file.write(archive_response.content)

    os.system('gunzip --keep -f ' + f"{downloadsDir}/*.gz")


if __name__ == "__main__":
    main()
