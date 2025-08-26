from Base_Model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """add new review"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """add new amenity"""
        self.amenities.append(amenity)

    def __str__(self):
        return f"Place({self.id}, {self.title}, {self.price})"