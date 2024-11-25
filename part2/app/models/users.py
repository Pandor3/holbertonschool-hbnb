from app.models.baseModel import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.place = []

    def validate_email(self, email):
        """Vérifie le format de l'email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email or not re.match(pattern, email):
            raise ValueError("Email is required and must be valid.")


    def add_place(self, place):
        self.place.append(place)


    def update(self, data):
        super().update(data)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'places': [place.to_dict() for place in self.place]
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
