from app.models.Base_Model import BaseModel
import re
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

     # --- RELATIONS ---
    places = db.relationship(
        "Place",
        backref="owner",
        cascade="all, delete-orphan",
        lazy='selectin'
    )
    reviews = db.relationship(
        "Review",
        backref="user",
        cascade="all, delete-orphan",
        lazy='selectin'
    )

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        if not first_name or len(first_name) > 50:
            raise ValueError("Le prénom est requis et doit faire max 50 caractères")
        if not last_name or len(last_name) > 50:
            raise ValueError("Le nom est requis et doit faire max 50 caractères")
        if not email or "@" not in email:
            raise ValueError("Email invalide")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    # def add_place(self, place):
    #     """Assign a place to this user"""
    #     if place not in self.places:
    #         self.places.append(place)
    #         place.owner = self

    # def add_review(self, review):
    #     if review not in self.reviews:
    #         self.reviews.append(review)
    #         review.user = self

    def validate_email(self):
        """Validate email"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Email non valide")
    
    def __str__(self):
        return f"User({self.id}, {self.first_name} {self.last_name}, {self.email})"