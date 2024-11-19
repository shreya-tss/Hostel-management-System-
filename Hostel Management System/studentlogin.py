'''
import mysql.connector
import tkinter as tk
from tkinter import messagebox

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tomriddle@31",
    database="hostelm"
)
cursor = connection.cursor()

# Student login function
def student_login():
    ssn = student_ssn_entry.get()
    password = student_password_entry.get()

    # Query to check login details
    cursor.execute("SELECT * FROM Student WHERE SSN = %s AND Password = %s", (ssn, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Success", "Student login successful!")
    else:
        messagebox.showerror("Login Failed", "Invalid SSN or Password")

# Creating the Tkinter window
student_window = tk.Tk()
student_window.title("Student Login")

# SSN and Password labels and entry fields
tk.Label(student_window, text="SSN").grid(row=0, column=0)
student_ssn_entry = tk.Entry(student_window)
student_ssn_entry.grid(row=0, column=1)

tk.Label(student_window, text="Password").grid(row=1, column=0)
student_password_entry = tk.Entry(student_window, show="*")
student_password_entry.grid(row=1, column=1)

# Login button
login_button = tk.Button(student_window, text="Login", command=student_login)
login_button.grid(row=2, column=1)

student_window.mainloop()
'''
import tkinter as tk
from tkinter import messagebox, Toplevel
import mysql.connector
from fee2 import open_fee_window
from mainreq import open_maintenance_request_form
#from student_reg import student_register_window

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tomriddle@31",
    database="hostelm"
)
cursor = connection.cursor()

# Function to open the Maintenance Request window

# Function to create the dashboard window
def open_dashboard():
    dashboard = Toplevel()
    dashboard.title("Dashboard")
    dashboard.geometry("400x300")
    dashboard.config(bg="#f0f8ff")

    # Fonts
    font_button = ('Arial', 12, 'bold')

    tk.Label(dashboard, text="Welcome to the Dashboard", font=('Arial', 16, 'bold'), bg="#f0f8ff").pack(pady=20)

    # Fee Payments button
    fee_button = tk.Button(dashboard, text="Fee Payments", command=open_fee_window, font=font_button, bg="#4CAF50", fg="white")
    fee_button.pack(pady=10)

    # Maintenance Request button
    maintenance_button = tk.Button(dashboard, text="Maintenance Request Form", command=open_maintenance_request_form, font=font_button, bg="#4CAF50", fg="white")
    maintenance_button.pack(pady=10)

def open_register_window():
    from student_reg import student_register_window  # Move import here to avoid circular dependency
    student_register_window()

# Function to create and open the login window
def student_login_window():
    student_window = tk.Tk()
    student_window.title("Student Login")
    student_window.geometry("400x250")
    student_window.config(bg="#f0f8ff")  # Light blue background color

    # Center the widgets in the grid
    for i in range(3):
        student_window.grid_rowconfigure(i, weight=1)
    student_window.grid_columnconfigure(0, weight=1)
    student_window.grid_columnconfigure(1, weight=1)

    # Fonts
    font_label = ('Arial', 12)
    font_entry = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # SSN and Password labels and entry fields
    tk.Label(student_window, text="SSN:", font=font_label, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    student_ssn_entry = tk.Entry(student_window, font=font_entry)
    student_ssn_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(student_window, text="Password:", font=font_label, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    student_password_entry = tk.Entry(student_window, font=font_entry, show="*")  # Masking password input
    student_password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Student login function
    def student_login():
        ssn = student_ssn_entry.get()
        password = student_password_entry.get()

        # Query to check login details
        cursor.execute("SELECT * FROM Student WHERE SSN = %s AND Password = %s", (ssn, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", "Student login successful!")
            student_window.destroy()  # Close the login window on successful login
            open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid SSN or Password")

    # Login button
    login_button = tk.Button(student_window, text="Login", command=student_login, font=font_button, bg="#4CAF50", fg="white")
    login_button.grid(row=2, columnspan=2, pady=20)

    register_button = tk.Button(student_window, text="Register", command=open_register_window, font=font_button, bg="#4CAF50", fg="white")
    register_button.grid(row=4, columnspan=2, pady=20)

    student_window.mainloop()


