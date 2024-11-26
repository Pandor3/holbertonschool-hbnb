from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def name_length(self, name, field_name, value):
        if not name:
            raise ValueError(f"{field_name} cannot be empty")
        if len(name) > value:
            raise ValueError(f"{field_name} must not exceed {value} characters")
        return name
