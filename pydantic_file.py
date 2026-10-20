from pydantic import BaseModel
class Patient( BaseModel):
    name: str
    age: int




def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Patient inserted successfully")

patient_info = {'name': 'John Doe', 'age': 30}
patient1 = Patient(**patient_info)

insert_patient(patient1)
