from app.models.baseModel import BaseModel
from app import db
from sqlalchemy.orm import relationship, validates
from sqlalchemy import CheckConstraint, ForeignKey, Column, Integer
import uuid

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete="CASCADE"), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Review initialized with:", kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'owner_id': self.owner_id,
            'place_id': self.place_id
        }

    @validates("rating")
    def set_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
