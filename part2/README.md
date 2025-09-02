# Holberton School - HBnB (Part 2)

This project is the second part of the **HBnB** series.  
It implements a simple RESTful API using **Flask** and **Flask-RESTX**,  
with data managed through Python classes (no database yet).  

The focus of this part is the **implementation of business logic and API endpoints**,  
providing a structured way to interact with the application data.

---

## 🚀 Technologies Used
- **Python 3.8+**
- **Flask** – to create the web server
- **Flask-RESTX** – to define, document, and manage API routes
- **UUID** – for generating unique identifiers
- **OOP (Classes)** – for modeling data instead of using a database

---

## 📂 Project Structure
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── Base_Model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── tests/
│   ├── test_amenity.py
│   ├── test_BaseModel.py
│   ├── test_facade.py
│   ├── test_place.py
│   ├── test_review.py
│   ├── test_user.py
│   ├── TestAmenitiesAPI.py
│   ├── TestPlacesAPI.py
│   ├── TestReviewsAPI.py
│   ├── TestUsersAPI.py
├── run.py
├── config.py
├── requirements.txt
├── README.md



---

## ⚙️ Installation & Running

1. **Clone the repository:**
```bash
git clone https://github.com/Ry-88/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

python3 run.py


## Authors

- **Ry-88** - [ryan-055@outlook.com](mailto:ryan-055@outlook.com)
- **moha88z** - [mohammed.alayda88@gmail.com](mailto:mohammed.alayda88@gmail.com)
- **Raed-Alqabas** - [rayeddd55@gmail.com](mailto:rayeddd55@gmail.com)