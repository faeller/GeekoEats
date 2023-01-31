#!/bin/python3

from fastapi import FastAPI
from fastapi.responses import FileResponse
import canteen_menu_manager as canteen

# initial setup
# canteen.downloadArchiveTxt()
# canteen.downloadMenuPDFs()
canteen.parseAndMapPDFs()

app = FastAPI()


@app.get("/")
@app.get("/today")
@app.get("/date/today")
async def current_menu():
    return FileResponse(canteen.dateToPDF(canteen.datetime.now()))


german_date_format = '%d.%m.%Y'

@app.get("/date/{german_date_string}")
async def current_menu(german_date_string: str):
    date = canteen.datetime.strptime(german_date_string, german_date_format)
    return FileResponse(canteen.dateToPDF(date))

