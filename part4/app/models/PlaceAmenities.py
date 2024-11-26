from app import db
from sqlalchemy.orm import relationship


class PlaceAmenities(db.Model):

    __tablename__ = "place_amenities"

    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), primary_key=True)
    amenity_id = db.Column(
        db.String(36), db.ForeignKey("amenities.id"), primary_key=True
    )
    place = relationship("Place", back_populates="place_amenities", overlaps="amenities,places")
    amenity = relationship("Amenity", back_populates="amenityplaces", overlaps="amenities,places")
