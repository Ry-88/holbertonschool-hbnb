from app.models.Base_Model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        # Keep bidirectional link if owner is provided
        if owner:
            owner.add_place(self)

    def add_review(self, review):
        """add new review"""
        if review not in self.reviews:
            self.reviews.append(review)
            review.place = self

    def add_amenity(self, amenity):
        """add new amenity"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            if hasattr(amenity, "places") and self not in amenity.places:
                amenity.places.append(self)

    def __str__(self):
        return f"Place({self.id}, {self.title}, {self.price})"