import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

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
