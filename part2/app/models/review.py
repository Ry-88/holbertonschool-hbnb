from Base_Model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place=None, user=None):
        super().__init__()
        if not text:
            raise ValueError("Invalide 'text': review content must not be empty")
        if not (1 <= rating <= 5):
            raise ValueError("Invalid 'rating': must be between 1 and 5.")
        
        from .place import Place
        if not isinstance(place, Place):
            raise TypeError("Invalid 'place': must be an instance of Place.")

        from .user import User
        if not isinstance(user, User):
            raise TypeError("Invalid 'user': must be an instance of User.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        place.add_review(self)
        if hasattr(user, "add_review"):
            user.add_review(self)

    def __str__(self):
        return f"Review({self.id}, {self.rating}, {self.text})"