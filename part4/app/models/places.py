from app.models.baseModel import BaseModel
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship
import uuid
from app import db

class Place(BaseModel):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    _title = db.Column(db.String(120), nullable=False)
    _description = db.Column(db.String(500), nullable=False)
    _price = db.Column(db.Numeric(10,2), nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True)
    reviews = relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary="place_amenities", back_populates="places", cascade="all, delete", viewonly=True)
    place_amenities = relationship("PlaceAmenities", back_populates="place", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'reviews': [review.to_dict() if hasattr(review, 'to_dict') else review for review in self.reviews],
            'amenities': self.amenities
        }

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self.name_length(value, "title", 50)
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self.name_length(value, "description", 100)
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    def add_review(self, review):
        if review.owner_id and review.place_id:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_review(self, review_id):
        """Remove a review by ID from the place's reviews list."""
        self.reviews = [review for review in self.reviews if (review.id if hasattr(review, 'id') else review.get('id')) != review_id]
