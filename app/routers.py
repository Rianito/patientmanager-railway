from fastapi import APIRouter, Request, HTTPException
from models import CpfStr, Limit, PatientCreate, PatientUpdate

def canUseCpf(request: Request, cpf: CpfStr):
    if request.app.mongodb["patients"].find_one({"cpf": cpf}):
        return False
    return True

patients = APIRouter(prefix="/patients", tags=["patients"])

@patients.post("/", status_code=201)
def create_patient(request: Request, patient: PatientCreate):
    patient_dict = dict(patient)
    if canUseCpf(request, patient_dict["cpf"]):
        new_patient = request.app.mongodb["patients"].insert_one(patient_dict)
        return request.app.mongodb["patients"].find_one({"_id": new_patient.inserted_id}, {"_id": False})
    raise HTTPException(400, "Cpf já está cadastrado.")

@patients.get("/", status_code=200)
def read_patients(request: Request, skip: int = 0):
    return list(request.app.mongodb["patients"].find({}, {"_id": False}, skip=skip, limit=50))

@patients.get("/{patient_cpf}", status_code=200)
def read_patient(request: Request, patient_cpf: CpfStr):
    result = request.app.mongodb["patients"].find_one({"cpf": patient_cpf}, {"_id": False})
    if result:
        return result
    raise HTTPException(404, "Paciente não encontrado.")

@patients.patch("/{patient_cpf}", status_code=204)
def update_patient(request: Request, patient: PatientUpdate, patient_cpf: CpfStr):
    patient = {k: v for k, v in patient.dict().items() if v is not None}
    if len(patient) >= 1:
        result = request.app.mongodb["patients"].update_one({"cpf": patient_cpf}, {"$set": patient})
        if not result.matched_count >= 1:
            return HTTPException(404, "Paciente não encontrado.")

@patients.delete("/{patient_cpf}", status_code=204)
def delete_patient(request: Request, patient_cpf: CpfStr):
    result = request.app.mongodb["patients"].delete_one({"cpf": patient_cpf})
    if not result.deleted_count >= 1:
        return HTTPException(404, "Paciente não encontrado.")