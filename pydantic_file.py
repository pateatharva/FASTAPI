from pydantic import BaseModel, EmailStr
from typing import List,Dict,Optional
class Patient( BaseModel):
    name: str
    email: EmailStr
    age: int
    sex: str
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str, str]




def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.sex)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print("Patient inserted successfully")

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.sex)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print("Patient updated successfully")

patient_info = {'name': 'John Doe', 'email': 'john.doe@example.com', 'age': 30 , 'sex': 'Male' , 'married' : True , 'allergies' : ['pollen','dust'] , 'contact' : {'phone_number':'5896574199'}}
patient1 = Patient(**patient_info)

patient_info = {'name': 'Julia Ann', 'email': 'julia.ann@example.com', 'age': 50 , 'sex': 'Female' , 'married' : False , 'allergies' : None , 'contact' : {'phone_number':'9322306166'}}
patient2 = Patient(**patient_info)

insert_patient(patient1)
update_patient(patient2)
