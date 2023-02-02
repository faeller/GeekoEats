#!/usr/bin/python3
import subprocess
import json

def parse_pdf(pdf_file):
    result = subprocess.check_output(
        ['./mahlzeit-parser/mahlzeit.rb', pdf_file])
    # print(result.stdout)
    return json.loads(result)


if(__name__ == "__main__"):
    print(parse_pdf("pdfs/01_08_2022_bis_14_08_2022_1.pdf"))
