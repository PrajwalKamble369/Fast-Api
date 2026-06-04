# why pydantic
# problem :
        # 1) Type Validation
        # 2) Data Validation

# this is problem
'''
def insert_patient_data(name:str,age:int ):  # this is type hinting
    print(name)
    print(age)
    print("inserted into database")

insert_patient_data("rahul",30)
'''

# solution 
"""
def insert_patient_data(name:str,age:int ):  # this is type hinting
    print(name)
    print(age)
    print("inserted into database")

insert_patient_data("rahul",30)
"""


# another solution but this is not scalable
'''
def insert_patient_data(name:str,age:int ):  # this is type hinting
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age cant be negative")
        else:
            print(name)
            print(age)
            print("inserted into database")
    else:
        raise TypeError("Incorrect DataType")

insert_patient_data("rahul",30)

def update_patient_data(name:str,age:int ):  # this is type hinting
    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age cant be negative")
        else:
            print(name)
            print(age)
            print("Updated")
    else:
        raise TypeError("Incorrect DataType")
'''

# absolute solution

# step one pydantic model
from pydantic import BaseModel, EmailStr, AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    # defining idel schema
    name: str = Annotated[str,Field(max_length=50,title="Name of Patient",description="less than 50 char",examples=["Prajwal","Viraj"])]
    email : EmailStr
    likedin : AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0,strict=True)]
    heigth : Annotated[float, Field(gt=0,strict=True)]
    married : Annotated[Optional[bool],Field(default=None,description="Patient Married?")] # optional
    alergies : List[str] = Field(max_length=5) # two level validation
    contact_detail : Dict[str, str]

    # field validator
    @field_validator("email")
    @classmethod
    def email_validator(cls,value):
        valid_domadins = ["hdfc.com","union.com"]
        domian_name = value.split("@")[-1]
        if domian_name not in valid_domadins:
            raise ValueError("Not a valid domain")
        return value
    
    @field_validator("name")
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
    # model validator
    @model_validator(mode="after")
    def validate_emergency_contact(self):
        if self.age > 60 and "emergency" not in self.contact_detail:
            raise ValueError("Patients older than 60 must have emergency contact")
        return self

    # computed field
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.heigth**2),2)
        return bmi
    

# step 3 pass to function
def insert_patient(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")

def update_patient(patient:Patient):
    print(patient.name,patient.age,patient.married,patient.bmi)
    print("Update")


patient_info = {
                "name":"Prajwal",
                "email":"abc@hdfc.com", 
                "likedin":"http://linkedint.com/12132",
                "age": 60,
                "weight":87,
                "heigth":1.72,
                "alergies":["dust","yogurt"],
                "contact_detail":{"phone":"146641468613","emergency":"14678653"}
                 }

# step 2 object of pydantic moadel
patient1 = Patient(**patient_info)
insert_patient(patient1)
update_patient(patient1)
