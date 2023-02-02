# Geeko Eats API

A REST API that provides canteen menu in various formats (PDF, JSON, JSON in English).

## Technology Stack

- Python 3.10
- FastAPI
- Google Trans API

## API Endpoints

- `GET /`: Get today's canteen menu
- `GET /docs`: Get all endpoints in swagger
- `GET /today`: Get today's canteen menu in PDF format
- `GET /date/{german_date_string}`: Get canteen menu of the specified date in PDF format. `german_date_string` should be in the format `dd.mm.yyyy`
- `GET /date/{german_date_string}/{format}`: Get canteen menu of the specified date in the specified format (PDF, JSON, JSON in English). `format` should be 
- either `pdf` or `json`, you can also use `json?lang=en`  

## Errors

The API will return a 404 error when the canteen menu is not available for the specified date. If there's any other error, it will return a 500 error.