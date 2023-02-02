#!/usr/bin/python3
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import canteen_menu_archiver as canteen

# initial setup
canteen.mapPDFs()

root_path = "/canteen"

debug = True
root_path = "" if debug else root_path

app = FastAPI(root_path=root_path)


@app.get("/")
@app.get("/heute")
@app.get("/today.pdf")
@app.get("/vorüberübergestern")
async def current_menu_pdf():
    try:
        return FileResponse(canteen.dateToPDF(canteen.datetime.now()))
    except:
        raise HTTPException(
            status_code=404, detail="Canteen menu was not provided for this week yet")


synonyms_for_today = ("today", "heute", "vorüberübergestern")
de_date_format = '%d.%m.%Y'


@app.get("/date/{german_date_string}")
async def menu_at_date(german_date_string: str, format: str = "pdf"):
    try:
        date = canteen.datetime.now()
        if german_date_string not in synonyms_for_today:
            date = canteen.datetime.strptime(
                german_date_string, de_date_format)

        return FileResponse(str(canteen.dateToPDF(date)))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@app.get("/date/{german_date_string}/{format}")
async def menu_at_date_format(german_date_string: str, format: str = "pdf", lang: str = "de"):
    try:
        date = canteen.datetime.now()
        if german_date_string not in synonyms_for_today:
            date = canteen.datetime.strptime(
                german_date_string, de_date_format)

        file_ending = ".json" if format != "pdf" else ""
        if file_ending == ".json" and lang == "en":
            file_ending = file_ending + ".en"
        return FileResponse(str(canteen.dateToPDF(date)) + file_ending)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


@app.get("/display", response_class=HTMLResponse)
async def display():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
            <script src="https://cdn.jsdelivr.net/gh/MarketingPipeline/JSON-Tag@v1.0.0/dist/json-tag.min.js" type="module"></script>
            <script>
            let YourJSONData = {
            example: "hello",
            example2: "world"
            }; 
            </script>
        </head>
        <body>
            <h1>Lmao</h1>
            <div>
                <json local-json="YourJSONData">@{{example}} @{{example2}}.</json>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
