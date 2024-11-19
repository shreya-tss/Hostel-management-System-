import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tomriddle@31",
    database="hostelm"
)
cursor = connection.cursor()

def staff_reg_window():
    # Function to register staff
    def register_staff():
        staff_id = staff_id_entry.get()
        dob = dob_entry.get()
        gender = gender_combo.get()
        position = position_entry.get()
        shift_time = shift_time_entry.get()
        salary = salary_entry.get()
        password = password_entry.get()

        # Check if staff ID already exists
        cursor.execute("SELECT * FROM Staff WHERE StaffID = %s", (staff_id,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Error", "Staff ID already exists.")
        else:
            # Insert new staff data into the Staff table
            try:
                query = """INSERT INTO Staff (StaffID, DOB, Gender, Position, ShiftTime, Salary, Password)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (staff_id, dob, gender, position, shift_time, salary, password))
                connection.commit()
                messagebox.showinfo("Success", "Staff registered successfully!")

                # Clear the form fields after successful registration
                clear_form()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

    # Function to clear form fields
    def clear_form():
        staff_id_entry.delete(0, tk.END)
        dob_entry.set_date('')
        gender_combo.set('')
        position_entry.delete(0, tk.END)
        shift_time_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    def open_login_window():
        from stafflogin import staff_login_window
        staff_login_window()

    # Create the main window
    root = tk.Tk()
    root.title("Staff Registration Form")
    root.geometry("500x450")
    root.config(bg="#f0f8ff")  # Light blue background color

    # Fonts
    font_label = ('Arial', 12)
    font_entry = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # Center the widgets in the grid
    for i in range(8):
        root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Staff ID
    tk.Label(root, text="Staff ID:", font=font_label, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    staff_id_entry = tk.Entry(root, font=font_entry)
    staff_id_entry.grid(row=0, column=1, padx=10, pady=10)

    # Date of Birth (with calendar)
    tk.Label(root, text="Date of Birth:", font=font_label, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    dob_entry = DateEntry(root, date_pattern='yyyy-mm-dd', font=font_entry)
    dob_entry.grid(row=1, column=1, padx=10, pady=10)

    # Gender (drop-down)
    tk.Label(root, text="Gender:", font=font_label, bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    gender_combo = ttk.Combobox(root, values=["Male", "Female", "Other"], font=font_entry)
    gender_combo.grid(row=2, column=1, padx=10, pady=10)

    # Position
    tk.Label(root, text="Position:", font=font_label, bg="#f0f8ff").grid(row=3, column=0, padx=10, pady=10, sticky='e')
    position_entry = tk.Entry(root, font=font_entry)
    position_entry.grid(row=3, column=1, padx=10, pady=10)

    # Shift Time
    tk.Label(root, text="Shift Time:", font=font_label, bg="#f0f8ff").grid(row=4, column=0, padx=10, pady=10, sticky='e')
    shift_time_entry = tk.Entry(root, font=font_entry)
    shift_time_entry.grid(row=4, column=1, padx=10, pady=10)

    # Salary
    tk.Label(root, text="Salary:", font=font_label, bg="#f0f8ff").grid(row=5, column=0, padx=10, pady=10, sticky='e')
    salary_entry = tk.Entry(root, font=font_entry)
    salary_entry.grid(row=5, column=1, padx=10, pady=10)

    # Password
    tk.Label(root, text="Password:", font=font_label, bg="#f0f8ff").grid(row=6, column=0, padx=10, pady=10, sticky='e')
    password_entry = tk.Entry(root, font=font_entry, show="*")  # Mask password input
    password_entry.grid(row=6, column=1, padx=10, pady=10)

    # Register Button
    register_button = tk.Button(root, text="Register", command=register_staff, font=font_button, bg="#4CAF50", fg="white")
    register_button.grid(row=7, columnspan=2, pady=20)

    login_button = tk.Button(root, text="Login", command=open_login_window, font=font_button, bg="#2196F3", fg="white")
    login_button.grid(row=8, columnspan=2, pady=10)

    # Run the application
    root.mainloop()