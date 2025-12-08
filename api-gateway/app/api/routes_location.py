from fastapi import APIRouter, Depends
from app.core.security import validate_token
from app.services.location_client import (
    read_locations, create_location, delete_location, edit_location
)

router = APIRouter(prefix="/location", tags=["Location"])

@router.post("/")
async def gateway_create_location(data: dict, payload=Depends(validate_token)):
    user_id = payload["sub"]
    result, status = await create_location(data, user_id)
    return result

@router.get("/")
async def gateway_get_locations(payload=Depends(validate_token)):
    user_id = payload["sub"]
    result, status = await read_locations(user_id)
    return result

@router.delete("/{loc_id}")
async def gateway_delete_location(loc_id: int, payload = Depends(validate_token)):
    user_id = payload["sub"]
    return (await delete_location(loc_id, user_id))[0]

@router.put("/{loc_id}")
async def gateway_edit_location(loc_id: int, data: dict, payload = Depends(validate_token)):
    user_id = payload["sub"]
    return (await edit_location(loc_id, data, user_id))[0]