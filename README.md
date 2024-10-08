# cars
python cars use delete function and edit function
import os

# Function to create a new folder or select an existing folder for car brand
def select_or_create_folder():
    while True:
        print("\n--- Select or Create Car Brand Folder ---")
        print("1. Create a new folder")
        print("2. Use an existing folder")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Create a new folder
            while True:
                folder_name = input("Enter a NEW folder name to store car information: ")
                if os.path.exists(folder_name):
                    print("Invalid input: Folder already exists. Please choose a different name.")
                else:
                    os.makedirs(folder_name)
                    print(f"Folder '{folder_name}' created.")
                    return folder_name
        
        elif choice == '2':
            # Use an existing folder
            folders = [f for f in os.listdir() if os.path.isdir(f)]
            if not folders:
                print("No existing folders available. Please create a new folder.")
                continue

            print("\nAvailable Car Brand Folders:")
            for i, folder in enumerate(folders, start=1):
                print(f"{i}. {folder}")
            
            try:
                folder_choice = int(input("Enter the number of the folder you want to use: ")) - 1
                if 0 <= folder_choice < len(folders):
                    return folders[folder_choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Function to check that a car ID is unique and then save it
def check_and_save_car_id():
    while True:
        print("\n--- Enter Car ID ---")
        car_id = input("Enter the Car ID (unique): ")
        with open("CarsID.txt", "a+") as f:
            f.seek(0)
            existing_ids = f.read().splitlines()
            if car_id in existing_ids:
                print("Invalid input: This Car ID already exists. Please use a unique ID.")
            else:
                f.write(car_id + "\n")
                return car_id

# Function to save car information in a specified folder
def save_car_info(folder_name, car_id, car_info):
    file_path = os.path.join(folder_name, f"{car_id}.txt")
    with open(file_path, "w") as car_file:
        car_file.write(car_info)
    print(f"\nCar information saved in '{file_path}'\n")

# Function to view existing folders and car files within them
def view_cars():
    print("\n--- View Existing Car Brands ---")
    folders = [f for f in os.listdir() if os.path.isdir(f)]
    if not folders:
        print("No car brands available.")
        return
    
    print("\nAvailable Car Brands:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    
    try:
        folder_choice = int(input("\nEnter the number of the brand you want to view: ")) - 1
        if 0 <= folder_choice < len(folders):
            selected_folder = folders[folder_choice]
            files = [f for f in os.listdir(selected_folder) if f.endswith('.txt')]
            if not files:
                print(f"\nNo cars available in the '{selected_folder}' brand.")
                return
            
            print(f"\nAvailable Cars in '{selected_folder}':")
            for i, file in enumerate(files, start=1):
                print(f"{i}. {file}")
            
            file_choice = int(input("\nEnter the number of the car you want to view: ")) - 1
            if 0 <= file_choice < len(files):
                selected_file = files[file_choice]
                with open(os.path.join(selected_folder, selected_file), "r") as f:
                    print("\n--- Car Information ---")
                    print(f.read())
                return selected_folder, selected_file  # Return folder and file for editing/deleting
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Function to delete a car record
def delete_car(folder_name, car_file):
    os.remove(os.path.join(folder_name, car_file))
    print(f"Car file '{car_file}' has been deleted.\n")

# Function to edit a car record
def edit_car(folder_name, car_file):
    file_path = os.path.join(folder_name, car_file)
    with open(file_path, "r") as f:
        existing_info = f.read()
    
    print("\n--- Edit Car Details ---")
    print("Current Information:")
    print(existing_info)
    
    car_model = input("Enter the Car Model: ")
    car_year = input("Enter the Year of Manufacture: ")
    car_price = input("Enter the Price of the Car: ")

    car_id = car_file.split('.')[0]  # Get the Car ID from the filename
    car_info = f"Car ID: {car_id}\nCar Model: {car_model}\nYear of Manufacture: {car_year}\nPrice: {car_price}\n"
    
    with open(file_path, "w") as f:
        f.write(car_info)
    
    print(f"Car information for '{car_file}' has been updated.\n")

# Main function to show the menu
def main():
    print("Welcome to the Car Dealer App")
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Add a new car")
        print("2. View existing cars")
        print("3. Delete a car")
        print("4. Edit a car")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Select or create a folder and save new car info
            folder_name = select_or_create_folder()
            car_id = check_and_save_car_id()
            
            print("\n--- Enter Car Details ---")
            car_model = input("Enter the Car Model: ")
            car_year = input("Enter the Year of Manufacture: ")
            car_price = input("Enter the Price of the Car: ")

            car_info = f"Car ID: {car_id}\nCar Model: {car_model}\nYear of Manufacture: {car_year}\nPrice: {car_price}\n"
            save_car_info(folder_name, car_id, car_info)
        
        elif choice == '2':
            folder_name, car_file = view_cars()
            if car_file:
                # Prompt to delete or edit the car after viewing
                print("Options:")
                print("1. Delete this car")
                print("2. Edit this car")
                action_choice = input("Choose an action: ")
                if action_choice == '1':
                    delete_car(folder_name, car_file)
                elif action_choice == '2':
                    edit_car(folder_name, car_file)
                else:
                    print("Invalid choice.")
        
        elif choice == '3':
            folder_name, car_file = view_cars()
            if car_file:
                delete_car(folder_name, car_file)
        
        elif choice == '4':
            folder_name, car_file = view_cars()
            if car_file:
                edit_car(folder_name, car_file)
        
        elif choice == '5':
            print("\nExiting the application. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number from the menu options.")

if __name__ == "__main__":
    main()
