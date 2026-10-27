from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pincode: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'Gurgaon', 'state': 'Haryana', 'pincode': '122018'}
address1 = Address(**address_dict)

patient_info = {'name': 'nitish', 'gender': 'male', 'age': 65, 'address': address1}
patient1 = Patient(**patient_info)
print(patient1)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.pincode)