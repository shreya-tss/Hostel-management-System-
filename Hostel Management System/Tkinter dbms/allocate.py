import tkinter as tk
from tkinter import messagebox, ttk, Scrollbar
import mysql.connector

# Database connection (Modify with your credentials)
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tomriddle@31',
    database='hostelm'
)
cursor = connection.cursor()

def fetch_rooms():
    """Fetch room status from the database and update the UI."""
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
    """Add a checkbox for each room to the corresponding frame."""
    var = tk.IntVar()  # Store checkbox state
    checkbox = tk.Checkbutton(
        parent_frame, text=f"Room {room_no}", variable=var,
        bg=bg_color, width=15, anchor="w"
    )
    checkbox.pack(anchor="w", pady=2)
    room_checkboxes[room_no] = var

def allocate_room():
    """Allocate selected room to the student."""
    ssn = ssn_entry.get()
    selected_rooms = [room_no for room_no, var in room_checkboxes.items() if var.get() == 1]

    if not selected_rooms:
        messagebox.showerror("Error", "Please select at least one room.")
        return

    try:
        # Check if student exists
        cursor.execute("SELECT * FROM Student WHERE SSN = %s", (ssn,))
        student = cursor.fetchone()
        if student is None:
            messagebox.showerror("Error", "Student doesn't exist.")
            return

        # Check room availability
        room_no = selected_rooms[0]
        cursor.execute("SELECT Status FROM Rooms WHERE RoomNo = %s", (room_no,))
        room_status = cursor.fetchone()

        if room_status and room_status[0] == 'Occupied':
            messagebox.showerror("Error", f"Room {room_no} is already occupied.")
            return

        # Update the Student table with the room allocation
        cursor.execute("UPDATE Student SET RoomNo = %s WHERE SSN = %s", (room_no, ssn))

        # Update the Rooms table to mark the room as "Occupied"
        cursor.execute("UPDATE Rooms SET Status = 'Occupied' WHERE RoomNo = %s", (room_no,))


        connection.commit()

        messagebox.showinfo("Success", f"Room {room_no} allocated to student {ssn}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Room Allocation System")
root.geometry("800x600")
root.configure(bg="#2C3E50")

room_checkboxes = {}  # Store checkbox states

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

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

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

# Run the Tkinter event loop
root.mainloop()

# Close the connection when done
cursor.close()
connection.close()