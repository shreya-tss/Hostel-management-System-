import tkinter as tk
from studentlogin import student_login_window
from stafflogin import staff_login_window

def main_window():
    root = tk.Tk()
    root.title("Hostel Management System")
    root.geometry("400x300")
    root.config(bg="#f0f8ff")  # Light blue background color

    # Heading
    heading_label = tk.Label(root, text="Hostel Management System", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#4CAF50")
    heading_label.pack(pady=20)

    # Button Styles
    button_font = ('Arial', 14, 'bold')

    # Student Login Button
    student_button = tk.Button(root, text="Student", font=button_font, bg="#4CAF50", fg="white", width=15, height=2, command=student_login_window)
    student_button.pack(pady=10)

    # Staff Login Button
    staff_button = tk.Button(root, text="Staff", font=button_font, bg="#4CAF50", fg="white", width=15, height=2, command=staff_login_window)
    staff_button.pack(pady=10)

    # Run the main event loop
    root.mainloop()

if __name__ == "__main__":
    main_window()