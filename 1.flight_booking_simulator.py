import csv
import os

DATA_FILE = "flights_data.csv"

# -----------------------------
# Utility Functions
# -----------------------------

def load_data():
    data = {"flights": []}

    if not os.path.exists(DATA_FILE):
        print("CSV file not found!")
        return data

    with open(DATA_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            flight = {
                "id": row["id"],
                "source": row["source"],
                "destination": row["destination"],
                "seats": int(row["seats"]),
                "booked": row["booked"].split(",") if row["booked"] else []
            }
            data["flights"].append(flight)

    return data


def save_data(data):
    with open(DATA_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "source", "destination", "seats", "booked"])

        for flight in data["flights"]:
            writer.writerow([
                flight["id"],
                flight["source"],
                flight["destination"],
                flight["seats"],
                ",".join(flight["booked"])
            ])


def find_flight(data, flight_id):
    for flight in data["flights"]:
        if flight["id"] == flight_id:
            return flight
    return None


# -----------------------------
# Core Features
# -----------------------------

def view_flights(data):
    if not data["flights"]:
        print("No flights available.\n")
        return

    print("\nAvailable Flights:")
    for flight in data["flights"]:
        available = flight["seats"] - len(flight["booked"])
        print(f"ID: {flight['id']} | {flight['source']} -> {flight['destination']} | Seats Left: {available}")
    print()


def book_ticket(data):
    flight_id = input("Enter Flight ID to book: ")
    flight = find_flight(data, flight_id)

    if not flight:
        print("Flight not found!\n")
        return

    if len(flight["booked"]) >= flight["seats"]:
        print("No seats available!\n")
        return

    name = input("Enter Passenger Name: ")

    flight["booked"].append(name)
    save_data(data)

    print(f"Ticket booked successfully for {name}!\n")


def cancel_ticket(data):
    flight_id = input("Enter Flight ID: ")
    flight = find_flight(data, flight_id)

    if not flight:
        print("Flight not found!\n")
        return

    name = input("Enter Passenger Name to cancel: ")

    if name in flight["booked"]:
        flight["booked"].remove(name)
        save_data(data)
        print("Ticket cancelled successfully!\n")
    else:
        print("Passenger not found!\n")


def view_passengers(data):
    flight_id = input("Enter Flight ID: ")
    flight = find_flight(data, flight_id)

    if not flight:
        print("Flight not found!\n")
        return

    if not flight["booked"]:
        print("No passengers yet.\n")
        return

    print("Passengers:")
    for p in flight["booked"]:
        print(f"- {p}")
    print()


# -----------------------------
# Main Menu
# -----------------------------

def main():
    while True:
        data = load_data()

        print("==== Flight Booking System ====")
        print("1. View Flights")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. View Passengers")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_flights(data)
        elif choice == "2":
            book_ticket(data)
        elif choice == "3":
            cancel_ticket(data)
        elif choice == "4":
            view_passengers(data)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.\n")


if __name__ == "__main__":
    main()
