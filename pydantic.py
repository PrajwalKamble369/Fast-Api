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


# absolute solution
