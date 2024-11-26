from .baseModel import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app import db, bcrypt
import uuid
import re


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    _first_name = db.Column(db.String(50), nullable=False)
    _last_name = db.Column(db.String(50), nullable=False)
    _email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    user_place = relationship('Place', backref='owner', lazy=True, cascade="all, delete-orphan")
    user_review = relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def validate_email(self, email):
        """Vérifie le format de l'email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(pattern, email):
            raise ValueError("Email is required and must be valid.")


    def add_place(self, place):
        self.user_place.append(place)


    def update(self, data):
        super().update(data)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.name_length(value, "first_name", 50)
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self.name_length(value, "last_name", 50)
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self.validate_email(value)
        self._email = value
