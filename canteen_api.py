#!/bin/python3

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import canteen_menu_manager as canteen

# initial setup
# canteen.downloadArchiveTxt()
# canteen.downloadMenuPDFs()
canteen.parseAndMapPDFs()

app = FastAPI(root_path="/canteen")


@app.get("/")
@app.get("/today")
@app.get("/today.pdf")
@app.get("/heute")
@app.get("/date/today")
@app.get("/vorüberübergestern")
async def current_menu():
    try:
        return FileResponse(canteen.dateToPDF(canteen.datetime.now()))
    except:
        raise HTTPException(status_code=404, detail="Canteen menu was not provided for this week yet")


german_date_format = '%d.%m.%Y'


@app.get("/date/{german_date_string}")
async def menu_at_date(german_date_string: str):
    try:
        date = canteen.datetime.strptime(german_date_string, german_date_format)
        return FileResponse(canteen.dateToPDF(date))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
