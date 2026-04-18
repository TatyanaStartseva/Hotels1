from datetime import date

from sqlalchemy import insert, select, update, delete

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from pydantic import BaseModel

from src.schemas.hotels import Hotel

from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel
    async def get_all(self,id,location,title,limit,offset):
            query = select(self.model)
            if id:
                query = query.filter_by(id=id)
            if title:
                query = query.filter_by(title=title)
            if location:
                query = query.filter(self.model.location.ilike(f"%{location}%")) # ilike чтобы при вводе данных они были регистро независимые
            query = (
                query
                .limit(limit)
                .offset(offset)
            )

            result = await self.session.execute(query)
            return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


    async def get_hotel(self,id:int):
        query = select(self.model).filter_by(id=id)
        result = await self.session.execute(query)
        return result.scalar_one()


    async def get_filtered_by_time(self, date_from:date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from,date_to=date_to)
        hotels_ids_to_get = (
             select(RoomsOrm.hotel_id)
             .select_from(RoomsOrm)
             .filter(RoomsOrm.id.in_(rooms_ids_to_get))
         )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))


