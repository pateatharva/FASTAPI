from pydantic import BaseModel, EmailStr,Field
from typing import List,Dict,Optional, Annotated
class Patient( BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100 , title = "Name of the patient" , description = "Name should be between 1 and 100 characters", examples = ["John Doe", "Jane Smith"])]
    email: EmailStr
    age: int = Field(gt = 0 , lt = 120)
    sex: str
    weight: float = Field(gt=0)
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str, str]




def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.sex)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print("Patient inserted successfully")

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.sex)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print("Patient updated successfully")

patient_info = {'name': 'John Doe', 'email': 'john.doe@example.com', 'age': 30 , 'sex': 'Male' , 'weight': 70.5, 'married' : True , 'allergies' : ['pollen','dust'] , 'contact' : {'phone_number':'5896574199'}}
patient1 = Patient(**patient_info)

patient_info = {'name': 'Julia Ann', 'email': 'julia.ann@example.com', 'age': 50 , 'sex': 'Female' , 'weight': 65.0, 'married' : False , 'allergies' : None , 'contact' : {'phone_number':'9322306166'}}
patient2 = Patient(**patient_info)

insert_patient(patient1)
update_patient(patient2)
