from fastapi import APIRouter, FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from models import Request, BloodType, Urgency
from schemas import RequestSchema
from auth import get_current_hospital

router = APIRouter()

# create a new request


@router.post("/request")
async def create_request(request: RequestSchema, current_hospital=Depends(get_current_hospital)):
    # this code checks if blood request is within the blood type range
    if request.blood_type not in [bt.value for bt in BloodType]:
        raise HTTPException(status_code=400, detail="invalid blood type")
    # checks if the urgency field in the request field is valid
    if request.urgency not in [u.value for u in Urgency]:
        raise HTTPException(status_code=400, detail="invalid Urgency")

    new_request = Request(**request.dict())
    return {"message": "Request successfully created"}


@router.get("/request")
async def list_request(blood_type: Optional[str] = None, location: Optional[str] = None, urgency: Optional[str] = None):
    requests = []
    if blood_type:
        request = [
            request for request in requests if request.blood_type == blood_type]
    if location:
        request = [
            request for request in requests if request.location == location]
    if urgency:
        request = [request for request in requests if request.urgency == urgency]
    return request


@router.put("/request/{id}")
async def update_request(id: int, request: RequestSchema, current_hospital=Depends(get_current_hospital)):
    existing_request = Request.get(id)
    if not existing_request:
        raise HTTPException(status_code=404, detail="request not found")
    # makes sure blood type and urgency is valid
    if request.blood_type not in [bt.value for bt in BloodType]:
        raise HTTPException(status_code=400, detail="invalid blood type")
    # checks if the urgency field in the request field is valid
    if request.urgency not in [u.value for u in Urgency]:
        raise HTTPException(status_code=400, detail="invalid Urgency")

    if request.id != None:  # this is done such that when you change 1 attribute the value of the others is not null
        Request[id].name = request.id
    if request.request != None:
        Request[request].name = request.request
    if request.current_hospital != None:
        Request[current_hospital].name = request.current_hospital

    existing_request.update(**request.dict())
    return {"message": "Request successfully updated"}


@router.delete("/request/{id}")
async def delete_request(id: int, request: RequestSchema, current_hospital=Depends(get_current_hospital)):
    existing_request = Request.get(id)
    if not existing_request:
        raise HTTPException(status_code=404, detail="request does not exists")
    del request[id]
    return {"message": "Request deleted successfully"}
