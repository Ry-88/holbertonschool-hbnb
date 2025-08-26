from Base_Model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        self.name = name