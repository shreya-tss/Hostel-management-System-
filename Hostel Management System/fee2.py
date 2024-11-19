'''
import tkinter as tk
from tkinter import messagebox
import mysql.connector

def open_fee_window():
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # use the role with needed privileges
        password='tomriddle@31',
        database='hostelm'
    )
    cursor = connection.cursor()

    # Utility function to check if an SSN exists in the Student table
    def ssn_exists(ssn):
        cursor.execute("SELECT 1 FROM Student WHERE SSN = %s", (ssn,))
        return cursor.fetchone() is not None

    # Utility function to check if a RoomNo exists in the Rooms table
    def room_exists(room_no):
        cursor.execute("SELECT 1 FROM Rooms WHERE RoomNo = %s", (room_no,))
        return cursor.fetchone() is not None

    def add_fee():
        ssn = ssn_entry.get()
        room_no = roomno_entry.get()
        status = status_entry.get()
        r_type = rtype_entry.get()

        if ssn_exists(ssn) and room_exists(room_no):
            try:
                # Fetch the last PID from the Fee table
                cursor.execute("SELECT MAX(PID) FROM Fee")
                last_pid = cursor.fetchone()[0]  # Get the maximum PID (last inserted)
                new_pid = last_pid + 1 if last_pid is not None else 1  # Increment PID or start from 1 if no data exists

                # Insert the new fee record with the manually generated PID
                query = "INSERT INTO Fee (PID, SSN, Status, R_Type) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (new_pid, ssn, status, r_type))
                connection.commit()
                messagebox.showinfo("Success", "Fee added successfully.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN or room number.")


    # Function to view fee details (Read)
    def view_fee():
        ssn = ssn_entry.get()

        if ssn_exists(ssn):
            try:
                query = "SELECT PID, Status, R_Type FROM Fee WHERE SSN = %s"
                cursor.execute(query, (ssn,))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Fee Details", f"PID: {result[0]}\nStatus: {result[1]}\nRoom Type: {result[2]}")
                else:
                    messagebox.showerror("Error", "No fee record found for this SSN.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")

    # Function to update fee details (Update)
    def update_fee():
        ssn = ssn_entry.get()
        status = status_entry.get()
        r_type = rtype_entry.get()

        if ssn_exists(ssn):
            try:
                query = "UPDATE Fee SET Status = %s, R_Type = %s WHERE SSN = %s"
                cursor.execute(query, (status, r_type, ssn))
                connection.commit()
                messagebox.showinfo("Success", "Fee details updated successfully.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")

    # Function to delete fee details (Delete)
    def delete_fee():
        ssn = ssn_entry.get()

        if ssn_exists(ssn):
            try:
                query = "DELETE FROM Fee WHERE SSN = %s"
                cursor.execute(query, (ssn,))
                connection.commit()
                messagebox.showinfo("Success", "Fee record deleted successfully.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")

    # Function to calculate hostel fee using the stored procedure
    def calculate_hostel_fee():
        ssn = ssn_entry.get()
        if ssn_exists(ssn):
            try:
                fee_amount = cursor.callproc('CalculateHostelFee2', [ssn, 0])  # Output will be in fee_amount[1]
                fee = fee_amount[1]
                
                if fee:
                    messagebox.showinfo("Hostel Fee", f"The hostel fee is: ${fee}")
                else:
                    messagebox.showerror("Error", "Room type not found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")
        connection.commit()

    # Function to retrieve room fees by occupancy type using aggregate functions and joins
    def get_fee_summary():
        try:
            query = """
            SELECT R.Occupancy,
                AVG(CASE
                        WHEN F.R_Type = 1 THEN 3000
                        WHEN F.R_Type = 2 THEN 2000
                        WHEN F.R_Type = 3 THEN 1500
                        ELSE 0
                    END) AS Average_Fee,
                MIN(CASE
                        WHEN F.R_Type = 1 THEN 3000
                        WHEN F.R_Type = 2 THEN 2000
                        WHEN F.R_Type = 3 THEN 1500
                        ELSE 0
                    END) AS Min_Fee,
                MAX(CASE
                        WHEN F.R_Type = 1 THEN 3000
                        WHEN F.R_Type = 2 THEN 2000
                        WHEN F.R_Type = 3 THEN 1500
                        ELSE 0
                    END) AS Max_Fee
            FROM Rooms R
            JOIN Fee F ON R.Occupancy = F.R_Type  -- Join based on room occupancy type
            GROUP BY R.Occupancy;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            summary = "\n".join([f"{occupancy}: Avg Fee ${avg_fee}, Min Fee ${min_fee}, Max Fee ${max_fee}"
                                for occupancy, avg_fee, min_fee, max_fee in result])

            messagebox.showinfo("Fee Summary", summary)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



    # Tkinter GUI Setup
    root = tk.Tk()
    root.title("Hostel Management System")

    # SSN Input
    tk.Label(root, text="Enter SSN:").grid(row=0, column=0, padx=10, pady=10)
    ssn_entry = tk.Entry(root)
    ssn_entry.grid(row=0, column=1, padx=10, pady=10)

    # Name Input
    tk.Label(root, text="Enter Name:").grid(row=1, column=0, padx=10, pady=10)
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    # Room Number Input
    tk.Label(root, text="Enter Room Number:").grid(row=2, column=0, padx=10, pady=10)
    roomno_entry = tk.Entry(root)
    roomno_entry.grid(row=2, column=1, padx=10, pady=10)

    # Status Input
    tk.Label(root, text="Enter Status:").grid(row=3, column=0, padx=10, pady=10)
    status_entry = tk.Entry(root)
    status_entry.grid(row=3, column=1, padx=10, pady=10)

    # Room Type Input
    tk.Label(root, text="Enter Room Type:").grid(row=4, column=0, padx=10, pady=10)
    rtype_entry = tk.Entry(root)
    rtype_entry.grid(row=4, column=1, padx=10, pady=10)

    # CRUD Buttons for Fee
    tk.Button(root, text="Add Fee", command=add_fee).grid(row=5, column=0, pady=5)
    tk.Button(root, text="View Fee", command=view_fee).grid(row=5, column=1, pady=5)
    tk.Button(root, text="Update Fee", command=update_fee).grid(row=6, column=0, pady=5)
    tk.Button(root, text="Delete Fee", command=delete_fee).grid(row=6, column=1, pady=5)

    # Calculate Fee Button
    calculate_button = tk.Button(root, text="Calculate Fee", command=calculate_hostel_fee)
    calculate_button.grid(row=7, column=0, columnspan=2, pady=10)

    # Fee Summary Button
    summary_button = tk.Button(root, text="Get Fee Summary", command=get_fee_summary)
    summary_button.grid(row=8, column=0, columnspan=2, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

    # Close the connection when done
    cursor.close()
    connection.close()
'''
import tkinter as tk
from tkinter import messagebox
import mysql.connector

def open_fee_window():
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # use the role with needed privileges
        password='tomriddle@31',
        database='hostelm'
    )
    cursor = connection.cursor()

    # Utility function to check if an SSN exists in the Student table
    def ssn_exists(ssn):
        cursor.execute("SELECT 1 FROM Student WHERE SSN = %s", (ssn,))
        return cursor.fetchone() is not None

    # Utility function to check if a RoomNo exists in the Rooms table
    def room_exists(room_no):
        cursor.execute("SELECT 1 FROM Rooms WHERE RoomNo = %s", (room_no,))
        return cursor.fetchone() is not None

    def add_fee():
        ssn = ssn_entry.get()
        room_no = roomno_entry.get()
        status = status_entry.get()
        r_type = rtype_entry.get()

        if ssn_exists(ssn) and room_exists(room_no):
            try:
                # Fetch the last PID from the Fee table
                cursor.execute("SELECT MAX(PID) FROM Fee")
                last_pid = cursor.fetchone()[0]  # Get the maximum PID (last inserted)
                new_pid = last_pid + 1 if last_pid is not None else 1  # Increment PID or start from 1 if no data exists

                # Insert the new fee record with the manually generated PID
                query = "INSERT INTO Fee (PID, SSN, Status, R_Type) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (new_pid, ssn, status, r_type))
                connection.commit()
                messagebox.showinfo("Success", "Fee added successfully.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN or room number.")

    # Function to view fee details (Read)
    def view_fee():
        ssn = ssn_entry.get()

        if ssn_exists(ssn):
            try:
                query = "SELECT PID, Status, R_Type FROM Fee WHERE SSN = %s"
                cursor.execute(query, (ssn,))
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Fee Details", f"PID: {result[0]}\nStatus: {result[1]}\nRoom Type: {result[2]}")
                else:
                    messagebox.showerror("Error", "No fee record found for this SSN.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")

    # Function to update fee details (Update)
    def update_fee():
        ssn = ssn_entry.get()
        status = status_entry.get()
        r_type = rtype_entry.get()

        if ssn_exists(ssn):
            try:
                query = "UPDATE Fee SET Status = %s, R_Type = %s WHERE SSN = %s"
                cursor.execute(query, (status, r_type, ssn))
                connection.commit()
                messagebox.showinfo("Success", "Fee details updated successfully.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")

    # Function to delete fee details (Delete)
    def delete_fee():
        ssn = ssn_entry.get()

        if ssn_exists(ssn):
            try:
                query = "DELETE FROM Fee WHERE SSN = %s"
                cursor.execute(query, (ssn,))
                connection.commit()
                messagebox.showinfo("Success", "Fee record deleted successfully.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")

    # Function to calculate hostel fee using the stored procedure
    def calculate_hostel_fee():
        ssn = ssn_entry.get()
        if ssn_exists(ssn):
            try:
                fee_amount = cursor.callproc('CalculateHostelFee2', [ssn, 0])  # Output will be in fee_amount[1]
                fee = fee_amount[1]
                
                if fee:
                    messagebox.showinfo("Hostel Fee", f"The hostel fee is: ${fee}")
                else:
                    messagebox.showerror("Error", "Room type not found.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Invalid SSN.")
        connection.commit()

    # Function to retrieve room fees by occupancy type using aggregate functions and joins
    def get_fee_summary():
        try:
            query = """
            SELECT R.Occupancy,
                AVG(CASE
                        WHEN F.R_Type = 1 THEN 3000
                        WHEN F.R_Type = 2 THEN 2000
                        WHEN F.R_Type = 3 THEN 1500
                        ELSE 0
                    END) AS Average_Fee,
                MIN(CASE
                        WHEN F.R_Type = 1 THEN 3000
                        WHEN F.R_Type = 2 THEN 2000
                        WHEN F.R_Type = 3 THEN 1500
                        ELSE 0
                    END) AS Min_Fee,
                MAX(CASE
                        WHEN F.R_Type = 1 THEN 3000
                        WHEN F.R_Type = 2 THEN 2000
                        WHEN F.R_Type = 3 THEN 1500
                        ELSE 0
                    END) AS Max_Fee
            FROM Rooms R
            JOIN Fee F ON R.Occupancy = F.R_Type  -- Join based on room occupancy type
            GROUP BY R.Occupancy;
            """
            cursor.execute(query)
            result = cursor.fetchall()

            summary = "\n".join([f"{occupancy}: Avg Fee ${avg_fee}, Min Fee ${min_fee}, Max Fee ${max_fee}"
                                for occupancy, avg_fee, min_fee, max_fee in result])

            messagebox.showinfo("Fee Summary", summary)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Tkinter GUI Setup
    fee_window = tk.Tk()
    fee_window.title("Hostel Fee Management")
    fee_window.geometry("400x450")
    fee_window.config(bg="#f0f8ff")  # Light blue background color

    # Center the widgets in the grid
    for i in range(5):
        fee_window.grid_rowconfigure(i, weight=1)
    fee_window.grid_columnconfigure(0, weight=1)
    fee_window.grid_columnconfigure(1, weight=1)

    # Fonts
    font_label = ('Arial', 12)
    font_entry = ('Arial', 12)
    font_button = ('Arial', 12, 'bold')

    # SSN Input
    tk.Label(fee_window, text="Enter SSN:", font=font_label, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    ssn_entry = tk.Entry(fee_window, font=font_entry)
    ssn_entry.grid(row=0, column=1, padx=10, pady=10)

    # Room Number Input
    tk.Label(fee_window, text="Enter Room Number:", font=font_label, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    roomno_entry = tk.Entry(fee_window, font=font_entry)
    roomno_entry.grid(row=1, column=1, padx=10, pady=10)

    # Status Input
    tk.Label(fee_window, text="Enter Status:", font=font_label, bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=10, sticky='e')
    status_entry = tk.Entry(fee_window, font=font_entry)
    status_entry.grid(row=2, column=1, padx=10, pady=10)

    # Room Type Input
    tk.Label(fee_window, text="Enter Room Type:", font=font_label, bg="#f0f8ff").grid(row=3, column=0, padx=10, pady=10, sticky='e')
    rtype_entry = tk.Entry(fee_window, font=font_entry)
    rtype_entry.grid(row=3, column=1, padx=10, pady=10)

    # CRUD Buttons for Fee
    tk.Button(fee_window, text="Add Fee", command=add_fee, font=font_button, bg="#4CAF50", fg="white").grid(row=4, column=0, pady=10)
    tk.Button(fee_window, text="View Fee", command=view_fee, font=font_button, bg="#4CAF50", fg="white").grid(row=4, column=1, pady=10)
    tk.Button(fee_window, text="Update Fee", command=update_fee, font=font_button, bg="#4CAF50", fg="white").grid(row=5, column=0, pady=10)
    tk.Button(fee_window, text="Delete Fee", command=delete_fee, font=font_button, bg="#4CAF50", fg="white").grid(row=5, column=1, pady=10)

    # Calculate Hostel Fee Button
    tk.Button(fee_window, text="Calculate Hostel Fee", command=calculate_hostel_fee, font=font_button, bg="#4CAF50", fg="white").grid(row=6, column=0, pady=10)

    # Fee Summary Button
    tk.Button(fee_window, text="Fee Summary", command=get_fee_summary, font=font_button, bg="#4CAF50", fg="white").grid(row=6, column=1, pady=10)

    fee_window.mainloop()

