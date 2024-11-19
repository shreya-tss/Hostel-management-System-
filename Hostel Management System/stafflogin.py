# Staff login function
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
def staff_login():
    staff_id = staff_id_entry.get()
    password = staff_password_entry.get()

    # Query to check login details
    cursor.execute("SELECT * FROM Staff WHERE StaffID = %s AND Password = %s", (staff_id, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Success", "Staff login successful!")
    else:
        messagebox.showerror("Login Failed", "Invalid Staff ID or Password")

# Creating the Tkinter window for Staff login
staff_window = tk.Tk()
staff_window.title("Staff Login")

# Staff ID and Password labels and entry fields
tk.Label(staff_window, text="Staff ID").grid(row=0, column=0)
staff_id_entry = tk.Entry(staff_window)
staff_id_entry.grid(row=0, column=1)

tk.Label(staff_window, text="Password").grid(row=1, column=0)
staff_password_entry = tk.Entry(staff_window, show="*")
staff_password_entry.grid(row=1, column=1)

# Login button
login_button = tk.Button(staff_window, text="Login", command=staff_login)
login_button.grid(row=2, column=1)

staff_window.mainloop()

import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tomriddle@31",
    database="hostelm"
)
cursor = connection.cursor()

# Function to create and open the staff login window
def staff_login_window():
    staff_window = tk.Tk()
    staff_window.title("Staff Login")
    staff_window.geometry("400x250")
    staff_window.config(bg="#f0f8ff")  # Light blue background color

    # Center the widgets in the grid
    for i in range(3):
        staff_window.grid_rowconfigure(i, weight=1)
    staff_window.grid_columnconfigure(0, weight=1)
    staff_window.grid_columnconfigure(1, weight=1)

    # Fonts
    font_label = ('Arial', 12)
    font_entry = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # Staff ID and Password labels and entry fields
    tk.Label(staff_window, text="Staff ID:", font=font_label, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    staff_id_entry = tk.Entry(staff_window, font=font_entry)
    staff_id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(staff_window, text="Password:", font=font_label, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    staff_password_entry = tk.Entry(staff_window, font=font_entry, show="*")  # Masking password input
    staff_password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Staff login function
    def staff_login():
        staff_id = staff_id_entry.get()
        password = staff_password_entry.get()

        # Query to check login details
        cursor.execute("SELECT * FROM Staff WHERE StaffID = %s AND Password = %s", (staff_id, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", "Staff login successful!")
            #staff_window.destroy()  # Close the login window on successful login
        else:
            messagebox.showerror("Login Failed", "Invalid Staff ID or Password")

    # Login button
    login_button = tk.Button(staff_window, text="Login", command=staff_login, font=font_button, bg="#4CAF50", fg="white")
    login_button.grid(row=2, columnspan=2, pady=20)

    staff_window.mainloop()

# Call the staff login window function to run the application
#staff_login_window()
'''
import tkinter as tk
from tkinter import messagebox, ttk, Scrollbar
import mysql.connector
from allocate2 import show_room_allocation_window

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="tomriddle@31",
    database="hostelm"
)
cursor = connection.cursor()

# Function to create and open the staff login window
def staff_login_window():
    staff_window = tk.Tk()
    staff_window.title("Staff Login")
    staff_window.geometry("400x250")
    staff_window.config(bg="#f0f8ff")  # Light blue background color

    # Center the widgets in the grid
    for i in range(3):
        staff_window.grid_rowconfigure(i, weight=1)
    staff_window.grid_columnconfigure(0, weight=1)
    staff_window.grid_columnconfigure(1, weight=1)

    # Fonts
    font_label = ('Arial', 12)
    font_entry = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # Staff ID and Password labels and entry fields
    tk.Label(staff_window, text="Staff ID:", font=font_label, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    staff_id_entry = tk.Entry(staff_window, font=font_entry)
    staff_id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(staff_window, text="Password:", font=font_label, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    staff_password_entry = tk.Entry(staff_window, font=font_entry, show="*")  # Masking password input
    staff_password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Staff login function
    def staff_login():
        staff_id = staff_id_entry.get()
        password = staff_password_entry.get()

        # Query to check login details
        cursor.execute("SELECT * FROM Staff WHERE StaffID = %s AND Password = %s", (staff_id, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Success", "Staff login successful!")
            staff_window.destroy()  # Close the login window on successful login
            #room_allocation_sys()  # Redirect to room allocation system
            show_room_allocation_window(connection, cursor)
        else:
            messagebox.showerror("Login Failed", "Invalid Staff ID or Password")

    # Login button
    login_button = tk.Button(staff_window, text="Login", command=staff_login, font=font_button, bg="#4CAF50", fg="white")
    login_button.grid(row=2, columnspan=2, pady=20)

    register_button = tk.Button(staff_window, text="Register", command=open_reg_window, font=font_button, bg="##2196F3", fg="white")
    register_button.grid(row=4, columnspan=2, pady=20)

    staff_window.mainloop()

def open_reg_window():
    from staff_reg import staff_reg_window
    staff_reg_window()

# Room Allocation System Code
def room_allocation_system():
    root = tk.Tk()
    root.title("Room Allocation System")
    root.geometry("800x600")
    root.configure(bg="#2C3E50")

    # Room checkboxes storage
    room_checkboxes = {}

    # Fetch and display rooms function
    def fetch_rooms():
        cursor.execute("SELECT RoomNo, Floor, Occupancy, Status FROM Rooms")
        rooms = cursor.fetchall()

        for room in rooms:
            room_no, floor, room_type, status = room
            color = "white" if status == "Available" else "#3498DB"

            if floor == 1 and room_type == 1:
                add_room_checkbutton(room_no, floor1_single_frame, color)
            elif floor == 1 and room_type == 2:
                add_room_checkbutton(room_no, floor1_double_frame, color)
            elif floor == 2 and room_type == 1:
                add_room_checkbutton(room_no, floor2_single_frame, color)
            elif floor == 2 and room_type == 2:
                add_room_checkbutton(room_no, floor2_double_frame, color)

    def add_room_checkbutton(room_no, parent_frame, bg_color):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(parent_frame, text=f"Room {room_no}", variable=var, bg=bg_color, width=15, anchor="w")
        checkbox.pack(anchor="w", pady=2)
        room_checkboxes[room_no] = var

    def allocate_room():
        ssn = ssn_entry.get()
        selected_rooms = [room_no for room_no, var in room_checkboxes.items() if var.get() == 1]

        if not selected_rooms:
            messagebox.showerror("Error", "Please select at least one room.")
            return

        try:
            cursor.execute("SELECT * FROM Student WHERE SSN = %s", (ssn,))
            student = cursor.fetchone()
            if student is None:
                messagebox.showerror("Error", "Student doesn't exist.")
                return

            room_no = selected_rooms[0]
            cursor.execute("UPDATE Student SET RoomNo = %s WHERE SSN = %s", (room_no, ssn))
            cursor.execute("UPDATE Rooms SET Status = 'Occupied' WHERE RoomNo = %s", (room_no,))
            connection.commit()

            messagebox.showinfo("Success", f"Room {room_no} allocated to student {ssn}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Title
    title_label = tk.Label(root, text="Room Allocation System", font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="white")
    title_label.pack(pady=10)

    # SSN Input Frame
    input_frame = tk.Frame(root, bg="#34495E", padx=10, pady=10)
    input_frame.pack(pady=10)
    tk.Label(input_frame, text="Enter SSN:", font=("Arial", 12), bg="#34495E", fg="white").grid(row=0, column=0, padx=10)
    ssn_entry = ttk.Entry(input_frame, width=30)
    ssn_entry.grid(row=0, column=1, padx=10)

    # Room Selection Frames
    selection_frame = tk.Frame(root, bg="#2C3E50")
    selection_frame.pack(pady=20)

    # Scrollable Frame Setup
    def create_scrollable_frame(parent):
        canvas = tk.Canvas(parent, bg="#2C3E50", highlightthickness=0)
        scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2C3E50")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    # Floor 1 - Single and Double Room Columns
    floor1_frame = tk.LabelFrame(selection_frame, text="Floor 1", font=("Arial", 14), bg="#2C3E50", fg="white")
    floor1_frame.grid(row=0, column=0, padx=10)
    floor1_single_frame = create_scrollable_frame(floor1_frame)
    floor1_double_frame = create_scrollable_frame(floor1_frame)

    tk.Label(floor1_single_frame, text="Single Rooms", bg="#2C3E50", fg="white").pack()
    tk.Label(floor1_double_frame, text="Double Rooms", bg="#2C3E50", fg="white").pack()

    # Floor 2 - Single and Double Room Columns
    floor2_frame = tk.LabelFrame(selection_frame, text="Floor 2", font=("Arial", 14), bg="#2C3E50", fg="white")
    floor2_frame.grid(row=0, column=1, padx=10)
    floor2_single_frame = create_scrollable_frame(floor2_frame)
    floor2_double_frame = create_scrollable_frame(floor2_frame)

    tk.Label(floor2_single_frame, text="Single Rooms", bg="#2C3E50", fg="white").pack()
    tk.Label(floor2_double_frame, text="Double Rooms", bg="#2C3E50", fg="white").pack()

    # Allocate Button
    allocate_button = ttk.Button(root, text="Allocate Room", command=allocate_room)
    allocate_button.pack(pady=10)

    # Fetch and Display Rooms
    fetch_rooms()

    # Run the Tkinter event loop for room allocation system
    root.mainloop()


# Launch the staff login window initially
#staff_login_window()

# Close the connection when done
#cursor.close()
#connection.close()
