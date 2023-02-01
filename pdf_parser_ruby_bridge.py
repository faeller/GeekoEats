#!/bin/python3
import subprocess


def parse_pdf(pdf_file):
    result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
    print(result.stdout)


if(__name__ == "__main__"):
    parse_pdf("pdfs/01_08_2022_bis_14_08_2022_1.pdf")