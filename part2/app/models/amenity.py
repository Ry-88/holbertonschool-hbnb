from app.models.Base_Model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or len(name) > 50:
            raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        self.name = name
        self.places = []

    def add_place(self, place):
        """Link an amenity to a place (many-to-many)"""
        if place not in self.places:
            self.places.append(place)
            place.add_amenity(self)