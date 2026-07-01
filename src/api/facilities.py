import json
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilityAdd

from init import redis_manager

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("/")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schema: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schema)
        await redis_manager.set("facilities", facilities_json,10)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts

@router.post("")
async def create_facilities(db: DBDep,facility_data: FacilityAdd= Body()):
 facilities = await db.facilities.add(facility_data)
 await db.commit()
 return {"status":"OK", "data": facilities}
