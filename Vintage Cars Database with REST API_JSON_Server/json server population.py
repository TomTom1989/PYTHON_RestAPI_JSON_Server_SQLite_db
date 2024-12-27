import requests

BASE_URL = "http://localhost:3000/cars"

# List of cars to populate the database
cars_data = [
    {
        "id": 1,
        "brand": "Porsche",
        "model": "911",
        "production_year": 1963,
        "convertible": False
    },
    {
        "id": 2,
        "brand": "Ford",
        "model": "Mustang",
        "production_year": 1972,
        "convertible": True
    },
    {
        "id": 3,
        "brand": "Chevrolet",
        "model": "Corvette",
        "production_year": 1967,
        "convertible": True
    },
    {
        "id": 4,
        "brand": "Jaguar",
        "model": "E-Type",
        "production_year": 1961,
        "convertible": False
    },
    {
        "id": 5,
        "brand": "Volkswagen",
        "model": "Beetle",
        "production_year": 1950,
        "convertible": False
    }
]

def populate_database():
    for car in cars_data:
        response = requests.post(BASE_URL, json=car)
        if response.status_code == 201:
            print(f"Car {car['brand']} {car['model']} added successfully.")
        else:
            print(f"Failed to add car {car['brand']} {car['model']}. Error: {response.text}")

if __name__ == "__main__":
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("Server is running. Populating the database...")
            populate_database()
        else:
            print("Server is not responding. Please check if JSON Server is running.")
    except Exception as e:
        print(f"Error: {e}")
