from app.models.PlaceAmenities import PlaceAmenities
from app.persistence.repository import SQLAlchemyRepository


class PlaceAmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(PlaceAmenities)
