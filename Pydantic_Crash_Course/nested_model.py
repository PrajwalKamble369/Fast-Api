from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state : str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address : Address

address_dit = {"city":"Pune","state":"maharashtra","pin":"12545"}

address1 = Address(**address_dit)

patient_dict= {"name":"ansba","gender":"M","age":29,"address":address1}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)
print(patient1.address.state)