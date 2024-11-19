import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection setup
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

# Room allocation function, callable from other parts of the app
def show_room_allocation_window(connection, cursor):
    room_var = tk.StringVar(value="")

    def allocate_room():
        ssn = ssn_entry.get()
        selected_room = room_var.get()
        print("Selected room:", selected_room)  # Debug line to check selected room value

        if not ssn:
            messagebox.showerror("Error", "Please enter SSN.")
            return

        # Check if the SSN exists in the Student table
        cursor.execute("SELECT RoomNo FROM Student WHERE SSN = %s", (ssn,))
        student = cursor.fetchone()
        if not student:
            messagebox.showerror("Error", "Invalid SSN.")
            return

        current_room = student[0]  # The currently assigned room (if any)

        if selected_room:
            try:
                # If the student already has an assigned room, set it to 'Available'
                if current_room:
                    cursor.execute("UPDATE Rooms SET Status = 'Available' WHERE RoomNo = %s", (current_room,))

                # Update Student table with the selected room
                cursor.execute("UPDATE Student SET RoomNo = %s WHERE SSN = %s", (selected_room, ssn))
                # Update Rooms table to set the new room as 'Occupied'
                cursor.execute("UPDATE Rooms SET Status = 'Occupied' WHERE RoomNo = %s", (selected_room,))
                connection.commit()

                messagebox.showinfo("Success", f"SSN {ssn} allocated Room No. {selected_room}.")
                room_var.set("")  # Reset room_var to avoid stale data
                load_rooms()  # Refresh the rooms list to update availability
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
                connection.rollback()
        else:
            messagebox.showerror("Error", "Please select an available room to allocate.")

    def load_rooms():
        cursor.execute("SELECT Floor, RoomNo, Status FROM Rooms ORDER BY Floor, RoomNo")
        rooms = cursor.fetchall()

        # Clear previous checkboxes
        for widget in checkboxes_frame.winfo_children():
            widget.destroy()

        current_floor = None
        for floor, room_no, status in rooms:
            if floor != current_floor:
                tk.Label(checkboxes_frame, text=f"Floor {floor}", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(anchor='w', pady=(10, 5))
                current_floor = floor

            color = "grey" if status == "Available" else "blue"
            checkbox = tk.Checkbutton(
                checkboxes_frame, text=room_no, variable=room_var, onvalue=room_no, offvalue="",
                font=("Arial", 14, "bold"),  # Larger font size and bold
                bg="#f0f8ff", fg="black" if status == "Available" else "white",
                selectcolor=color, state="normal" if status == "Available" else "disabled",
                padx=10, pady=5  # Extra padding for a larger appearance
            )
            checkbox.pack(anchor='w', padx=10, pady=4)

    # Tkinter GUI setup
    room_window = tk.Toplevel()
    room_window.title("Room Allocation")
    room_window.geometry("400x600")
    room_window.configure(bg="#f0f8ff")

    # SSN Entry
    tk.Label(room_window, text="Enter Student SSN:", bg="#f0f8ff", font=("Arial", 12)).pack(pady=5)
    ssn_entry = tk.Entry(room_window, font=("Arial", 12))
    ssn_entry.pack(pady=5)

    # Scrollable Frame for Room Checkboxes
    frame_canvas = tk.Frame(room_window, bg="#f0f8ff")
    frame_canvas.pack(fill='both', expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame_canvas, bg="#f0f8ff")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside Canvas for checkboxes
    checkboxes_frame = tk.Frame(canvas, bg="#f0f8ff")
    canvas.create_window((0, 0), window=checkboxes_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    checkboxes_frame.bind("<Configure>", on_frame_configure)

    # Allocate Button
    allocate_button = tk.Button(room_window, text="Allocate", command=allocate_room, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
    allocate_button.pack(pady=10)

    # Load rooms initially
    load_rooms()


# Tkinter root setup

