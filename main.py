from fastapi import FastAPI
from exceptions import (
    PincodeNotFoundError,
    pincode_not_found_handler,
    InvalidPincodeError,
    invalid_pincode_handler
)

from data import pincode_db

from models import LocationResponse,  BulkRequest, BulkResponse

app = FastAPI(
    title="Pinecode Loopkup API",
    description="Autofill city and state from Indian Pincode"
)

# Register custom exception handler
app.add_exception_handler(PincodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPincodeError,invalid_pincode_handler)


@app.get('/')
def root():
    return {"message": "Pincode lookup!"}



@app.get('/pincode/{code}', response_model=LocationResponse)
def lookup_pincode(code:str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincodeError(code, "Must be 6 digit!")
    if code not in pincode_db:
        raise PincodeNotFoundError(code)
    return pincode_db[code]


@app.post('/pincode/bulk', response_model=BulkResponse)
def bulk_lookup(request:BulkRequest):
    results = []
    missing = []
    
    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)
    return BulkResponse(
        found = len(results),
        not_found= len(missing),
        missing=missing,
        results=results,
    )