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

# end point for query parameter
@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="Sort on the basis of height,weight or bmi"),order:str= Query("asc",description="sort in ascending or descending order")):
    valid_field = ["height","weight","bmi"]
    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f"Invalid Field select from {valid_field}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail=f"Invalid order select from {["asc","desc"]}")
    
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)

    return sorted_data

    