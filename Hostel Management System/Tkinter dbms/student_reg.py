'''
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import mysql.connector
from studentlogin import student_login_window

# Function to clear the form fields
 


# Function to register the student

def register_student():
    ssn = ssn_entry.get()
    name = name_entry.get()
    dob = dob_entry.get()
    year_of_study = year_of_study_entry.get()
    course = course_entry.get()
    gender = gender_combo.get()
    contact = contact_entry.get()
    room_no = room_no_entry.get()
    room_type = room_type_combo.get()
    meal_plan = meal_plan_combo.get()
    password = password_entry.get()


    # Determine meal plan description
    if meal_plan in ["Breakfast/Lunch", "Lunch/Dinner", "Breakfast/Dinner"]:
        meal_plan_desc = "Meal Plan 1"
    elif meal_plan == "All 3":
        meal_plan_desc = "Meal Plan 2"

    # Save data into the database
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if your database server is different
            user='root',  # Change to your database username
            password='tomriddle@31',  # Change to your database password
            database='hostelm'  # Change to your database name
        )
        cursor = connection.cursor()
        query = """INSERT INTO Student (SSN, Name, DOB, Year_of_Study, Course, Gender, Contact, RoomNo, Password, meal_plan, R_Type)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (ssn, name, dob, year_of_study, course, gender, contact, room_no, password, meal_plan_desc, room_type))
        connection.commit()
        messagebox.showinfo("Success", "Student registered successfully!")

        

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def open_login_window():
    student_login_window()  

# Create main window
root = tk.Tk()
root.title("Student Registration Form")

# SSN
tk.Label(root, text="SSN:").grid(row=0, column=0, padx=10, pady=10)
ssn_entry = tk.Entry(root)
ssn_entry.grid(row=0, column=1)

# Name
tk.Label(root, text="Name:").grid(row=1, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

# Date of Birth
tk.Label(root, text="Date of Birth:").grid(row=2, column=0, padx=10, pady=10)
dob_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
dob_entry.grid(row=2, column=1)

# Year of Study
tk.Label(root, text="Year of Study:").grid(row=3, column=0, padx=10, pady=10)
year_of_study_entry = tk.Entry(root)
year_of_study_entry.grid(row=3, column=1)

# Course
tk.Label(root, text="Course:").grid(row=4, column=0, padx=10, pady=10)
course_entry = tk.Entry(root)
course_entry.grid(row=4, column=1)

# Gender
tk.Label(root, text="Gender:").grid(row=5, column=0, padx=10, pady=10)
gender_combo = ttk.Combobox(root, values=["Male", "Female", "Other"])
gender_combo.grid(row=5, column=1)

# Contact Number
tk.Label(root, text="Contact Number:").grid(row=6, column=0, padx=10, pady=10)
contact_entry = tk.Entry(root)
contact_entry.grid(row=6, column=1)

# Room Number
tk.Label(root, text="Room Number:").grid(row=7, column=0, padx=10, pady=10)
room_no_entry = tk.Entry(root)
room_no_entry.grid(row=7, column=1)

# Room Type
tk.Label(root, text="Room Type:").grid(row=8, column=0, padx=10, pady=10)
room_type_combo = ttk.Combobox(root, values=["Single Occupancy", "Double Occupancy"])
room_type_combo.grid(row=8, column=1)

# Meal Plan
tk.Label(root, text="Meal Plan:").grid(row=9, column=0, padx=10, pady=10)
meal_plan_combo = ttk.Combobox(root, values=["Breakfast/Lunch", "Lunch/Dinner", "Breakfast/Dinner", "All 3"])
meal_plan_combo.grid(row=9, column=1)

# Password
tk.Label(root, text="Password:").grid(row=10, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")  # Masking password input
password_entry.grid(row=10, column=1)

# Register Button
register_button = tk.Button(root, text="Register", command=register_student)
register_button.grid(row=11, columnspan=2, pady=20)

# Button to open the login window
login_button = tk.Button(root, text="Login", command=open_login_window)
login_button.grid(row=12, columnspan=2, pady=10)

# Run the application
root.mainloop()
'''
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import mysql.connector
#from studentlogin import student_login_window

# Function to clear the form fields
# Uncomment if needed
'''
def clear_form():
    ssn_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    dob_entry.set_date('')  # Clears the DateEntry
    year_of_study_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    gender_combo.set('')  # Resets Combobox
    contact_entry.delete(0, tk.END)
    room_no_entry.delete(0, tk.END)
    room_type_combo.set('')  # Resets Combobox
    meal_plan_combo.set('')  # Resets Combobox
    password_entry.delete(0, tk.END)
'''


def student_register_window():
    # Function to register the student
    def register_student():
        ssn = ssn_entry.get()
        name = name_entry.get()
        dob = dob_entry.get()
        year_of_study = year_of_study_entry.get()
        course = course_entry.get()
        gender = gender_combo.get()
        contact = contact_entry.get()
        #room_no = room_no_entry.get()
        room_type = room_type_combo.get()
        meal_plan = meal_plan_combo.get()
        password = password_entry.get()

        # Determine meal plan description
        if meal_plan in ["Breakfast/Lunch", "Lunch/Dinner", "Breakfast/Dinner"]:
            meal_plan_desc = "Meal Plan 1"
        elif meal_plan == "All 3":
            meal_plan_desc = "Meal Plan 2"

        # Save data into the database
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Change if your database server is different
                user='root',  # Change to your database username
                password='tomriddle@31',  # Change to your database password
                database='hostelm'  # Change to your database name
            )
            cursor = connection.cursor()
            query = """INSERT INTO Student (SSN, Name, DOB, Year_of_Study, Course, Gender, Contact, RoomNo, Password, meal_plan, R_Type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (ssn, name, dob, year_of_study, course, gender, contact, '0', password, meal_plan_desc, room_type))
            connection.commit()
            messagebox.showinfo("Success", "Student registered successfully!")

            # Clear the form fields after successful registration
            # clear_form()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_login_window():
        from studentlogin import student_login_window
        student_login_window()  

    # Create main window
    root = tk.Tk()
    root.title("Student Registration Form")
    root.geometry("600x600")  # Set an initial size for the window
    root.config(bg="#f0f8ff")  # Light blue background color

    # Center the widgets in the grid
    for i in range(12):
        root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Fonts
    font_label = ('Arial', 12)
    font_entry = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # SSN
    tk.Label(root, text="SSN:", font=font_label, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    ssn_entry = tk.Entry(root, font=font_entry)
    ssn_entry.grid(row=0, column=1, padx=10, pady=10)

    # Name
    tk.Label(root, text="Name:", font=font_label, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    name_entry = tk.Entry(root, font=font_entry)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    # Date of Birth
    tk.Label(root, text="Date of Birth:", font=font_label, bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    dob_entry = DateEntry(root, date_pattern='yyyy-mm-dd', font=font_entry)
    dob_entry.grid(row=2, column=1, padx=10, pady=10)

    # Year of Study
    tk.Label(root, text="Year of Study:", font=font_label, bg="#f0f8ff").grid(row=3, column=0, padx=10, pady=10, sticky='e')
    year_of_study_entry = tk.Entry(root, font=font_entry)
    year_of_study_entry.grid(row=3, column=1, padx=10, pady=10)

    # Course
    tk.Label(root, text="Course:", font=font_label, bg="#f0f8ff").grid(row=4, column=0, padx=10, pady=10, sticky='e')
    course_entry = tk.Entry(root, font=font_entry)
    course_entry.grid(row=4, column=1, padx=10, pady=10)

    # Gender
    tk.Label(root, text="Gender:", font=font_label, bg="#f0f8ff").grid(row=5, column=0, padx=10, pady=10, sticky='e')
    gender_combo = ttk.Combobox(root, values=["Male", "Female", "Other"], font=font_entry)
    gender_combo.grid(row=5, column=1, padx=10, pady=10)

    # Contact Number
    tk.Label(root, text="Contact Number:", font=font_label, bg="#f0f8ff").grid(row=6, column=0, padx=10, pady=10, sticky='e')
    contact_entry = tk.Entry(root, font=font_entry)
    contact_entry.grid(row=6, column=1, padx=10, pady=10)

    # Room Number
    #tk.Label(root, text="Room Number:", font=font_label, bg="#f0f8ff").grid(row=7, column=0, padx=10, pady=10, sticky='e')
    #room_no_entry = tk.Entry(root, font=font_entry)
    #room_no_entry.grid(row=7, column=1, padx=10, pady=10)

    # Room Type
    tk.Label(root, text="Room Type:", font=font_label, bg="#f0f8ff").grid(row=8, column=0, padx=10, pady=10, sticky='e')
    room_type_combo = ttk.Combobox(root, values=["Single Occupancy", "Double Occupancy"], font=font_entry)
    room_type_combo.grid(row=8, column=1, padx=10, pady=10)

    # Meal Plan
    tk.Label(root, text="Meal Plan:", font=font_label, bg="#f0f8ff").grid(row=9, column=0, padx=10, pady=10, sticky='e')
    meal_plan_combo = ttk.Combobox(root, values=["Breakfast/Lunch", "Lunch/Dinner", "Breakfast/Dinner", "All 3"], font=font_entry)
    meal_plan_combo.grid(row=9, column=1, padx=10, pady=10)

    # Password
    tk.Label(root, text="Password:", font=font_label, bg="#f0f8ff").grid(row=10, column=0, padx=10, pady=10, sticky='e')
    password_entry = tk.Entry(root, font=font_entry, show="*")  # Masking password input
    password_entry.grid(row=10, column=1, padx=10, pady=10)

    # Register Button
    register_button = tk.Button(root, text="Register", command=register_student, font=font_button, bg="#4CAF50", fg="white")
    register_button.grid(row=11, columnspan=2, pady=20)

    # Button to open the login window
    login_button = tk.Button(root, text="Login", command=open_login_window, font=font_button, bg="#2196F3", fg="white")
    login_button.grid(row=12, columnspan=2, pady=10)

    # Run the application
    root.mainloop()