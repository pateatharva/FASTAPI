
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[
        str,
        Field(..., description="ID of the patient", examples=["P001"])
    ]
    name: Annotated[
        str,
        Field(..., description="Name of the patient", examples=["John Doe"])
    ]
    city: Annotated[
        str,
        Field(..., description="City of the patient", examples=["New York"])
    ]
    age: Annotated[
        int,
        Field(..., gt=0, lt=120, description="Age of the patient", examples=[30])
    ]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(..., description="Gender of the patient", examples=["Male"])
    ]
    height: Annotated[
        float,
        Field(..., gt=0, description="Height in centimeters", examples=[175.5])
    ]
    weight: Annotated[
        float,
        Field(..., gt=0, description="Weight in kilograms", examples=[70.0])
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / ((self.height / 100) ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25.0:
            return "Normal weight"
        elif self.bmi < 30.0:
            return "Overweight"
        else:
            return "Obesity"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default = None)]
    city: Annotated[Optional[str],Field(default = None)]
    age: Annotated[Optional[int],Field(default = None)]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]],Field(default = None)]
    height: Annotated[Optional[float],Field(default = None)]
    weight: Annotated[Optional[float],Field(default = None)]

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patient records."}


@app.get("/view")
def view():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the DB",
        examples=["P001"]
    )
):
    data = load_data()

    if patient_id in data:
        return {"id": patient_id, **data[patient_id]}

    raise HTTPException(
        status_code=404,
        detail="Patient not found."
    )


# IMPORTANT: This endpoint must be outside view_patient()
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort by height, weight or bmi"
    ),
    order: str = Query(
        "asc",
        description="Sort in ascending or descending order"
    )
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Valid orders are: asc, desc"
        )

    data = load_data()

    # Sort the patient records
    sorted_data = sorted(
        data.items(),
        key=lambda item: item[1].get(sort_by, 0),
        reverse=(order == "desc")
    )

    return [
        {"id": patient_id, **patient_data}
        for patient_id, patient_data in sorted_data
    ]


@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient with this ID already exists."
        )

    # Store patient data under the patient's ID
    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully."}
    )


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    # Step 1: Load existing patient data
    data = load_data()

    # Step 2: Check whether patient exists
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    # Step 3: Update the provided fields
    for field, value in patient_update.model_dump(exclude_unset=True).items():
        data[patient_id][field] = value

    # Step 4: Recalculate BMI using updated height and weight
    height = data[patient_id]["height"]
    weight = data[patient_id]["weight"]

    bmi = round(weight / ((height / 100) ** 2), 2)

    # Step 5: Recalculate verdict
    if bmi < 18.5:
        verdict = "Underweight"
    elif bmi < 25:
        verdict = "Normal weight"
    elif bmi < 30:
        verdict = "Overweight"
    else:
        verdict = "Obesity"

    # Step 6: Update BMI and verdict in patient data
    data[patient_id]["bmi"] = bmi
    data[patient_id]["verdict"] = verdict

    # Step 7: Save updated data
    save_data(data)

    return {"message": "Patient updated successfully."}
