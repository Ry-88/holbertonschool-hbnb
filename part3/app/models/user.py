from app.models.Base_Model import BaseModel
import re
from app.extensions import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate_email()
        self.places = []
        self.reviews = []

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Assign a place to this user"""
        if place not in self.places:
            self.places.append(place)
            place.owner = self

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)
            review.user = self

    def validate_email(self):
        """Validate email"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Email non valide")
    
    def __str__(self):
        return f"User({self.id}, {self.first_name} {self.last_name}, {self.email})"