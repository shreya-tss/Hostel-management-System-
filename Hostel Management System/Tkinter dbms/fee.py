import tkinter as tk
from tkinter import messagebox
import mysql.connector  # or your preferred database connector

# Database connection (Replace with your actual credentials)
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tomriddle@31',
    database='hostelm'
)
cursor = connection.cursor()

def calculate_hostel_fee():
    ssn = ssn_entry.get()
    room_no = roomno_entry.get()

    try:
        # Step 1: Get Room Number from Student Table
        get_room_query = "SELECT RoomNo FROM Student WHERE SSN = %s"
        cursor.execute(get_room_query, (ssn,))
        fetched_room_no = cursor.fetchone()
        
        # Debugging statement to print fetched room number
        print(f"Fetched Room Number: {fetched_room_no}")

        
        # Check if RoomNo is fetched and if it matches the entered room_no
        if fetched_room_no is None:
            messagebox.showerror("Error", "Invalid SSN or student not assigned to the specified room.")
            return
        
        fetched_room_no = fetched_room_no[0]

        if str(fetched_room_no) != str(room_no):
            messagebox.showerror("Error", "Room number does not match the SSN provided.")
            return
        
        # Step 2: Get Occupancy Type from Rooms Table
        get_occupancy_query = "SELECT Occupancy FROM Rooms WHERE RoomNo = %s"
        cursor.execute(get_occupancy_query, (room_no,))
        occupancy = cursor.fetchone()

        print(f"Fetched Occupancy: {occupancy}")

        if occupancy is None:
            messagebox.showerror("Error", "Room number not found in the Rooms table.")
            return

        occupancy_type = occupancy[0]
        
        # Step 3: Update R_Type in Fee Table
        update_rtype_query = "UPDATE Fee SET R_Type = %s WHERE SSN = %s"
        cursor.execute(update_rtype_query, (occupancy_type, ssn))
        connection.commit()

        # Step 4: Calculate Fee Based on R_Type
        if occupancy_type == 1:
            fee = 3000
        elif occupancy_type == 2:
            fee = 2000
        #elif occupancy_type == 'Triple':
        #    fee = 1500
        else:
            raise ValueError("Invalid room type in database.")

        # Display the calculated fee
        messagebox.showinfo("Hostel Fee", f"The hostel fee is: Rs{fee}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to open the fee payment window
def open_fee_payment_window():
    # Tkinter window setup
    fee_window = tk.Toplevel()
    fee_window.title("Hostel Fee Calculator")

    # SSN Input
    tk.Label(fee_window, text="Enter SSN:").grid(row=0, column=0, padx=10, pady=10)
    global ssn_entry  # Define ssn_entry and roomno_entry in the global scope for calculate_hostel_fee access
    ssn_entry = tk.Entry(fee_window)
    ssn_entry.grid(row=0, column=1, padx=10, pady=10)

    # Room Number Input
    tk.Label(fee_window, text="Enter Room Number:").grid(row=1, column=0, padx=10, pady=10)
    global roomno_entry
    roomno_entry = tk.Entry(fee_window)
    roomno_entry.grid(row=1, column=1, padx=10, pady=10)

    # Calculate Button
    calculate_button = tk.Button(fee_window, text="Calculate Fee", command=calculate_hostel_fee)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=20)
