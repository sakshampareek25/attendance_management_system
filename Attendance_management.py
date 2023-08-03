USER_DATABASE_FILE = "user_credentials.txt"
ATTENDANCE_RECORDS_FILE = "attendance_records.txt"
MONTHLY_REPORT_FILE = "monthly_attendance_report.txt"

user_database = {"saksham":"pareek"}
student_database = {}
daily_attendance_records = {}
weekly_attendance_records = {}
monthly_attendance_records = {}

# loading the attendance records, user credentails first when main func starts and then saving the attendance records as daily attendance report when attendance is marked, and  saving the user credentails 

def save_attendance_records():
    with open(ATTENDANCE_RECORDS_FILE, "w") as file:
        for date, records in daily_attendance_records.items():
            for student_id, name in records.items():
                file.write(f"{date},{student_id},{name}\n")
def load_attendance_records():
    try:
        with open(ATTENDANCE_RECORDS_FILE, "r") as file:
            for line in file:
                date, student_id, name = line.strip().split(",")
                if date not in daily_attendance_records:
                    daily_attendance_records[date] = {}
                daily_attendance_records[date][student_id] = name
    except FileNotFoundError:
        # The file doesn't exist yet, create it when the first attendance is marked.
        pass

# Function to read the user credentials from the file into the user_database dictionary
def load_user_credentials():
    try:
        with open(USER_DATABASE_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                user_database[username] = password
    except FileNotFoundError:
        # The file doesn't exist yet, create it when the first admin registers.
        pass

# Function to save the user credentials from the user_database dictionary to the file
def save_user_credentials():
    with open(USER_DATABASE_FILE, "w") as file:
        for username, password in user_database.items():
            file.write(f"{username},{password}\n")


# User Authentication
def register_user(username, password):
    if username in user_database:
        return "Username already exists."
    user_database[username] = password
    return "Registration successful."

def login_user(username, password):
    if username not in user_database or user_database[username] != password:
        return "Invalid username or password. you are not authenticate person:"
    return "Login successful."

# Student Information Management
def add_student(student_id, name):
    if student_id in student_database:
        return "Student ID already exists."
    student_database[student_id] = name
    return "Student added successfully."

def view_students():
    return student_database

def update_student(student_id, new_name):
    if student_id not in student_database:
        return "Student ID not found."
    student_database[student_id] = new_name
    return "Student information updated successfully."

def delete_student(student_id):
    if student_id not in student_database:
        return "Student ID not found."
    del student_database[student_id]
    return "Student deleted successfully."

# Marking Attendance
def mark_attendance(date, student_ids_present):
    attendance_record = {}
    for student_id in student_ids_present:
        if student_id in student_database:
            attendance_record[student_id] = student_database[student_id]
    daily_attendance_records[date] = attendance_record
    save_attendance_records()  # Save the attendance records immediately after marking attendance
    return attendance_record

# generating and saving the monthly reports in text file

def generate_monthly_report():
    for date, records in daily_attendance_records.items():
        year, month, day = map(int, date.split("-"))
        key = f"{year}-{month}"
        if key not in monthly_attendance_records:
            monthly_attendance_records[key] = {}
        for student_id, name in records.items():
            monthly_attendance_records[key][student_id] = name

def save_monthly_report():
    with open(MONTHLY_REPORT_FILE, "w") as file:
        for key, records in monthly_attendance_records.items():
            file.write(f"Month: {key}\n")
            for student_id, name in records.items():
                file.write(f"{student_id},{name}\n")

def main():
    load_user_credentials()
    load_attendance_records()
    print("Welcome to the Attendance Management System")
    while True:
        print("\nOptions:")
        print("1. Login\n2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            message = login_user(username, password)
            print(message)

            if message == "Login successful.":
                if username == "saksham":  # Check if the user is the admin
                    while True:
                        print("\nOptions:")
                        print("1. Register User\n2. Add Student\n3. View Students\n4. Update Student\n5. Delete Student\n6. Mark Attendance\n7. Generate Monthly Report\n8. Logout")
                        user_choice = input("Enter your choice: ")

                        if user_choice == "1":
                            new_username = input("Enter a username: ")
                            new_password = input("Enter a password: ")
                            message = register_user(new_username, new_password)
                            print(message)

                        elif user_choice == "2":
                            student_id = input("Enter the Student ID: ")
                            name = input("Enter the Student's Name: ")
                            message = add_student(student_id, name)
                            print(message)

                        elif user_choice == "3":
                            students = view_students()
                            print("Students in the database:")
                            for student_id, name in students.items():
                                print(f"Student ID: {student_id}, Name: {name}")

                        elif user_choice == "4":
                            student_id = input("Enter the Student ID to update: ")
                            new_name = input("Enter the new Name: ")
                            message = update_student(student_id, new_name)
                            print(message)

                        elif user_choice == "5":
                            student_id = input("Enter the Student ID to delete: ")
                            message = delete_student(student_id)
                            print(message)

                        elif user_choice == "6":
                            date = input("Enter the date (YYYY-MM-DD): ")
                            student_ids_present = input("Enter Student IDs present: ").split(",")
                            attendance_record = mark_attendance(date, student_ids_present)
                            print("Attendance marked for:")
                            for student_id, name in attendance_record.items():
                                print(f"Student ID: {student_id}, Name: {name}")

                        elif user_choice == "7":
                            generate_monthly_report()
                            save_monthly_report()
                            print("Monthly report generated successfully.")

                        elif user_choice == "8":
                            print("Logged out successfully.")
                            break

                        else:
                            print("Invalid choice. Please try again.")

                else:
                    while True:
                        print("\nOptions:")
                        print("1. Add Student\n2. View Students\n3. Logout")
                        user_choice = input("Enter your choice: ")

                        if user_choice == "1":
                            student_id = input("Enter the Student ID: ")
                            name = input("Enter the Student's Name: ")
                            message = add_student(student_id, name)
                            print(message)
                        elif user_choice == "2":
                            students = view_students()
                            print("Students in the database:")
                            for student_id, name in students.items():
                                print(f"Student ID: {student_id}, Name: {name}")

                        elif user_choice == "3":
                            print("Logged out successfully.")
                            break

                        else:
                            print("Invalid choice. Please try again.")

        elif choice == "2":
            print("Exiting the Attendance Management System.")
            save_user_credentials()
            save_attendance_records()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
