import requests
import json

BASE_URL = "http://localhost:3000/cars"


def check_server(cid=None):
    try:
        if cid:
            # Ensure the ID is passed as an integer
            response = requests.get(f"{BASE_URL}/{int(cid)}")
            print(f"Debug: Checking ID {cid}, Status Code: {response.status_code}, Response: {response.text}")
            return response.status_code == 200  # Return True if the record exists
        else:
            response = requests.get(BASE_URL)
            return response.status_code == 200
    except Exception as e:
        print(f"Error in check_server: {e}")
        return False



def print_menu():
    print("+-----------------------------------+")
    print("|       Vintage Cars Database       |")
    print("+-----------------------------------+")
    print("M E N U")
    print("=======")
    print("1. List cars")
    print("2. Add new car")
    print("3. Delete car")
    print("4. Update car")
    print("0. Exit")


def read_user_choice():
    choice = input("Enter your choice (0..4): ").strip()
    return choice if choice in ['0', '1', '2', '3', '4'] else None


def print_header():
    print(f"{'id':<10} | {'brand':<15} | {'model':<10} | {'production_year':<15} | {'convertible':<10}")


def print_car(car):
    print(f"{car['id']:<10} | {car['brand']:<15} | {car['model']:<10} | {car['production_year']:<15} | {car['convertible']}")


def list_cars():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        cars = response.json()
        if not cars:
            print("*** Database is empty ***")
        else:
            print_header()
            for car in cars:
                print_car(car)
    else:
        print("Error fetching data from server.")


#def name_is_valid(name):
#    return bool(name and all(c.isalnum() or c.isspace() for c in name))


def enter_id():
    car_id = input("Car ID (empty string to exit): ").strip()
    return int(car_id) if car_id.isdigit() else None


#def enter_production_year():
#    year = input("Car production year (empty string to exit): ").strip()
#   return int(year) if year.isdigit() and 1900 <= int(year) <= 2000 else None


#def enter_name(what):
#    name = input(f"Car {what} (empty string to exit): ").strip()
#   return name if name_is_valid(name) else None


#def enter_convertible():
 #   answer = input("Is this car convertible? [y/n] (empty string to exit): ").strip().lower()
  #  return True if answer == 'y' else False if answer == 'n' else None


def delete_car():
    car_id = enter_id()
    if car_id:
        response = requests.delete(f"{BASE_URL}/{car_id}")
        if response.status_code == 200:
            print("Success!")
        else:
            print("Error: Car not found.")


def input_car_data():
    car = {}

    car['brand'] = input("Enter car brand (empty string to exit): ").strip()
    if not car['brand']:
        return None

    car['model'] = input("Enter car model (empty string to exit): ").strip()
    if not car['model']:
        return None

    production_year = input("Enter production year (empty string to exit): ").strip()
    if not production_year.isdigit() or not (1900 <= int(production_year) <= 2000):
        print("Invalid production year. Please enter a year between 1900 and 2000.")
        return None
    car['production_year'] = int(production_year)

    convertible = input("Is this car convertible? [y/n] (empty string to exit): ").strip().lower()
    if convertible == 'y':
        car['convertible'] = True
    elif convertible == 'n':
        car['convertible'] = False
    else:
        print("Invalid input for convertible. Please enter 'y' or 'n'.")
        return None

    return car




def add_car():
    car_id = input("Enter car ID (empty string to exit): ").strip()
    if not car_id:
        print("Car creation cancelled.")
        return

    car = input_car_data()  # Gather car data excluding ID
    if car:
        car['id'] = str(car_id)  # Add the ID to the car dictionary
        response = requests.post(BASE_URL, json=car)
        if response.status_code == 201:
            print(f"Car {car['brand']} {car['model']} added successfully.")
        else:
            print(f"Failed to add car. Status Code: {response.status_code}, Response: {response.text}")
    else:
        print("Car creation cancelled.")





def update_car():
    car_id = input("Enter the ID of the car to update (empty string to exit): ").strip()
    if not car_id or not check_server(car_id):
        print("Car ID not found or operation cancelled.")
        return

    print("Enter the new car details:")
    car = input_car_data()  # Gather car data excluding ID
    if car:
        response = requests.put(f"{BASE_URL}/{car_id}", json=car)
        if response.status_code == 200:
            print("Car updated successfully!")
        else:
            print("Error updating car.")
    else:
        print("Car update cancelled.")




while True:
    if not check_server():
        print("Server is not responding - quitting!")
        exit(1)
    print_menu()
    choice = read_user_choice()
    if choice == '0':
        print("Bye!")
        exit(0)
    elif choice == '1':
        list_cars()
    elif choice == '2':
        add_car()
    elif choice == '3':
        delete_car()
    elif choice == '4':
        update_car()
