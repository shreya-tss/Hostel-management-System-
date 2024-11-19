import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector  # Ensure this package is installed

# Establish Database Connection
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='tomriddle@31',
        database='hostelm'
    )
    cursor = connection.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

def maintenance_request():
    ssn = ssn_entry.get()
    issue = issue_entry.get()

    if not ssn or not issue:
        messagebox.showerror("Error", "Both SSN and Issue Description are required.")
        return

    try:
        # Verify if the student exists
        cursor.execute("SELECT * FROM Student WHERE SSN = %s", (ssn,))
        student = cursor.fetchone()

        if student is None:
            messagebox.showerror("Error", "Student with this SSN does not exist.")
            return
        
        cursor.execute("SELECT MAX(ReqID) FROM MaintenanceReq")
        max_req_id = cursor.fetchone()[0]
        next_req_id = max_req_id + 1 if max_req_id is not None else 1  # Start from 1 if no data exists

        # Generate the next request number
        cursor.execute("SELECT COUNT(*) FROM MaintenanceReq")
        next_req_no = cursor.fetchone()[0] + 1

        # Insert the new maintenance request
        insert_query = """
            INSERT INTO MaintenanceReq (ReqID, ReqNo, Issue, Status, Date_of_R)
            VALUES (%s, %s, %s, 'Pending', %s)
        """
        request_date = datetime.now().strftime('%Y-%m-%d')

        cursor.execute(insert_query, (next_req_id, next_req_no, issue, request_date))
        connection.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"Request {next_req_no} lodged successfully.")
        else:
            messagebox.showerror("Error", "Failed to lodge the request.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to open the maintenance request form
def open_maintenance_request_form():
    # Tkinter window setup
    request_window = tk.Toplevel()
    request_window.title("Maintenance Request Form")
    request_window.geometry("400x300")  # Set a fixed size for the window
    request_window.configure(bg="#f0f8ff")  # Soft background color

    # Title Label
    title_label = tk.Label(request_window, text="Maintenance Request Form", font=("Arial", 16, "bold"), bg="#f0f8ff")
    title_label.pack(pady=10)

    # Frame for Input Fields
    input_frame = tk.Frame(request_window, bg="#f0f8ff")
    input_frame.pack(pady=10)

    # SSN Input
    global ssn_entry, issue_entry  # Define these in the global scope for access in `maintenance_request`
    tk.Label(input_frame, text="SSN:", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    ssn_entry = tk.Entry(input_frame, font=("Arial", 12))
    ssn_entry.grid(row=0, column=1, padx=10, pady=5)

    # Issue Description Input
    tk.Label(input_frame, text="Issue Description:", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    issue_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
    issue_entry.grid(row=1, column=1, padx=10, pady=5)

    # Submit Button
    submit_button = tk.Button(request_window, text="Submit Request", command=maintenance_request, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    submit_button.pack(pady=20)

# Ensure to close the database connection when done (optional, or use try-finally)
# cursor.close()
# connection.close()
