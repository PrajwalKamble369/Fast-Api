from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

# function to load data
def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
    
    return data


# end point for home page
@app.get("/")
def hello():
    return {"message":"Patient Management System API"}


# end point for about page
@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient record"}

# end point to view data
@app.get("/view")
def view():
    data = load_data()
    return data

# end point for path parameter
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str= Path(...,description="Id of patient in data",example="P001")):
    # load all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")