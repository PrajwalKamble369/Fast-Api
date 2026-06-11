from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal,Optional
import json

app = FastAPI()

# pydyantic model
class Patient(BaseModel):
    id : Annotated[str,Field(...,description="ID of Patient",examples=["P001"])]
    name : Annotated[str,Field(...,description="Name of Patient",examples=["FirstName LastName"])]
    city : Annotated[str,Field(...,description="Enter city of Patient",examples=["Mumbai"])]
    age : Annotated[int,Field(...,gt=0,lt=120,description="Age of Patient",examples=[12])]
    gender : Annotated[Literal["male","female","others"],Field(...,description="gender of patient")]
    height : Annotated[float,Field(...,gt=0,description="height of patient in kgs")]
    weight : Annotated[float,Field(...,gt=0,description="weight of patient in meters")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"
        
class PatientsUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Name")]
    city: Annotated[Optional[str], Field(None, description="City")]
    age: Annotated[Optional[int], Field(None, gt=0, lt=120)]
    gender: Annotated[
        Optional[Literal["male","female","others"]],
        Field(None)
    ]
    height: Annotated[Optional[float], Field(None, gt=0)]
    weight: Annotated[Optional[float], Field(None, gt=0)]


# function to load data
def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
    
    return data

# utility function
def save_data(data):
    with open("patient.json","w") as f:
        json.dump(data,f)

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

# end point to create(post request)
@app.post("/create")
def create_patient(patient:Patient):
    # load existing data
    data = load_data()

    # check if the patient alreay exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient Already Exsist")

    # new patient add to datbase
    data[patient.id] = patient.model_dump(exclude=["id"])

    # save into json file
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"patient created successfully"})

# end point for update (edit)
@app.put("/edit/{patient_id}")
def update_patient(patient_id:str,patient_update:PatientsUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    #existing_patient_info -> pydantic object -> update bmi + verdict
    existing_patient_info["id"] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
     #-> pydantic object -> dict
    existing_patient_info =patient_pydantic_object.model_dump(exclude="id")
    # add this dict to daata
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200,content={"message":"patient updated"})

# end point for delete
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    # load data 
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code= 200, content={"message":"patient deleted"})


    