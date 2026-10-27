
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    sex: str
    weight: float
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']

        domain_name = value.split('@')[-1].lower()

        if domain_name not in valid_domains:
            raise ValueError(
                f"Invalid email domain. Valid domains are: "
                f"{', '.join(valid_domains)}"
            )

        return value
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()


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


patient_info = {
    'name': 'John Doe',
    'email': 'john.doe@hdfc.com',
    'age': 30,
    'sex': 'Male',
    'weight': 70.5,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact': {'phone_number': '5896574199'}
}

patient1 = Patient(**patient_info)

patient_info = {
    'name': 'Julia Ann',
    'email': 'julia.ann@icici.com',
    'age': 50,
    'sex': 'Female',
    'weight': 65.0,
    'married': False,
    'allergies': None,
    'contact': {'phone_number': '9322306166'}
}

patient2 = Patient(**patient_info)

insert_patient(patient1)
update_patient(patient2)
