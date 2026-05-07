from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("/")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(db: DBDep,facility_data: FacilityAdd= Body()):
 facilities = await db.facilities.add(facility_data)
 await db.commit()
 return {"status":"OK", "data": facilities}
