from pydantic import BaseModel, Field, ConfigDict
from src.schemas.facilities import Facility

class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities_ids: list[int] = []


class Room(RoomAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PatchRoomRequest(BaseModel):
    title: str| None = Field(None)
    description: str | None = Field(None)
    price: int| None = Field(None)
    quantity: int| None = Field(None)
    facilities_ids: list[int] = []


class PatchRoom(BaseModel):
    hotel_id: int| None = Field(None)
    title: str| None = Field(None)
    description: str | None = Field(None)
    price: int| None = Field(None)
    quantity: int| None = Field(None)


class RoomWithRels(Room):
    facilities: list[Facility]