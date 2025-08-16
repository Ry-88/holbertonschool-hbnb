classDiagram
    class BaseEntity {
        - UUID id
        - DateTime created_at
        - DateTime updated_at
        + void save()
        + void delete()
    }

    class User {
        - String name
        - String email
        - String password_hash
        + Boolean authenticate(password)
        + void update_profile(data)
        + void delete_account()
    }

    class Place {
        - String title
        - String description
        - String address
        - String city
        - Float price_per_night
        + void update_details(data)
        + Float calculate_average_rating()
        + void add_amenity(amenity)
    }

    class Review {
        - Integer rating
        - String comment
        + void edit_review(new_comment, new_rating)
        + void delete_review()
    }

    class Amenity {
        - String name
        - String description
        + void update_info(data)
    }

    %% Inheritance
    BaseEntity <|-- User
    BaseEntity <|-- Place
    BaseEntity <|-- Review
    BaseEntity <|-- Amenity

    %% Relationships
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has
    Place "0..*" --> "0..*" Amenity : includes
