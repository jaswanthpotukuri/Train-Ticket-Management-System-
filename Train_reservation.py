import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk
import random

# Establish MySQL database connection
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='asdfghjkl',
        database='project'
    )
    if conn.is_connected():
        print("Connected to MySQL database")
except Error as e:
    print("Error while connecting to MySQL", e)

cursor = conn.cursor()

# Tkinter main window setup
root = tk.Tk()
root.title("Train Reservation System")
root.geometry("1000x600")
root.configure(bg="#2C3E50")  # Dark teal background

# Title Frame
title_frame = tk.Frame(root, bg="#2C3E50", pady=20)
title_frame.pack(fill="x", pady=10)

title_label = tk.Label(
    title_frame,
    text="Train Reservation System",
    font=("Helvetica", 28, "bold"),
    fg="#ECF0F1",  # Light text for contrast
    bg="#2C3E50"
)
title_label.pack(pady=10)

# Helper function to display a message box
def show_message(title, message):
    messagebox.showinfo(title, message)

# Function to add a passenger with simple design
def add_passenger():
    add_passenger_window = tk.Toplevel(root)
    add_passenger_window.title("Add Passenger")
    add_passenger_window.geometry("500x600")
    add_passenger_window.configure(bg="#34495E")  # Dark gray background

    # Header for Add Passenger
    tk.Label(add_passenger_window, text="Add Passenger", font=("Helvetica", 20, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=20)

    entry_frame = tk.Frame(add_passenger_window, bg="#34495E")
    entry_frame.pack(pady=20)

    labels = ["Name:", "Age:", "Gender:", "Phone:", "Email:", "Departure:", "Destination:"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(entry_frame, text=label, font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").grid(row=i, column=0, padx=20, pady=10)
        entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=25, relief="solid", bd=1)
        entry.grid(row=i, column=1, pady=10)
        entries.append(entry)

    gender_entry = ttk.Combobox(entry_frame, values=['Male', 'Female', 'Other'], font=("Helvetica", 12), width=22)
    gender_entry.grid(row=2, column=1, pady=10)
    entries[2] = gender_entry  # Replace gender entry with combobox

    # Save button with simple styling
    def save_passenger():
        name = entries[0].get()
        age = entries[1].get()
        gender = entries[2].get()
        phone = entries[3].get()
        email = entries[4].get()
        departure = entries[5].get()
        destination = entries[6].get()
        id = random.randint(1000, 9999)

        if name and age and gender:
            cursor.execute("INSERT INTO passenger (passenger_id, name, age, gender, phone, email, departure, destination) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (id, name, age, gender, phone, email, departure, destination))
            conn.commit()
            show_message("Success", "Passenger added successfully!")
            add_passenger_window.destroy()
        else:
            show_message("Error", "Please fill in all required fields.")

    save_button = tk.Button(add_passenger_window, text="Save", command=save_passenger, bg="#1ABC9C", fg="white", font=("Helvetica", 12), relief="solid", width=20, height=2)
    save_button.pack(pady=20)

# Function to view all passengers with clean table design
def view_passengers():
    view_window = tk.Toplevel(root)
    view_window.title("View Passengers")
    view_window.geometry("900x500")
    view_window.configure(bg="#34495E")

    # Title for Passenger List
    tk.Label(view_window, text="Passenger List", font=("Helvetica", 20, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=20)

    # Treeview with scrollbars
    tree_frame = tk.Frame(view_window, bg="#34495E")
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    vert_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
    vert_scroll.pack(side="right", fill="y")

    horz_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")
    horz_scroll.pack(side="bottom", fill="x")

    tree = ttk.Treeview(
        tree_frame, 
        columns=("ID", "Name", "Age", "Gender", "Phone", "Email", "Departure", "Destination"),
        show='headings',
        yscrollcommand=vert_scroll.set, 
        xscrollcommand=horz_scroll.set
    )
    vert_scroll.config(command=tree.yview)
    horz_scroll.config(command=tree.xview)

    # Column formatting with simple, clean design
    for col in tree["columns"]:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=120, anchor='center', stretch=True)

    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT * FROM passenger")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Function to generate ticket with clean, simple design
def view_ticket():
    ticket_window = tk.Toplevel(root)
    ticket_window.title("Generate Ticket")
    ticket_window.geometry("500x400")
    ticket_window.configure(bg="#34495E")

    # Header for Generate Ticket
    tk.Label(ticket_window, text="Generate Ticket", font=("Helvetica", 20, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=20)

    ticket_frame = tk.Frame(ticket_window, bg="#34495E")
    ticket_frame.pack(padx=20, pady=20)

    tk.Label(ticket_frame, text="Passenger ID:", font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1").grid(row=0, column=0, padx=20, pady=10)
    passenger_id_entry = tk.Entry(ticket_frame, font=("Helvetica", 12), width=25, relief="solid", bd=1)
    passenger_id_entry.grid(row=0, column=1, pady=10)

    # Train names for ticket generation
    train_names = ["Shatabdi Express", "Rajdhani Express", "Duronto Express", "Garib Rath", "Vande Bharat Express"]

    def generate_ticket():
        passenger_id = passenger_id_entry.get()
        if passenger_id.isdigit():
            cursor.execute("SELECT * FROM passenger WHERE passenger_id = %s", (passenger_id,))
            passenger = cursor.fetchone()
            if passenger:
                name = passenger[1]
                train_name = random.choice(train_names)
                fare = random.randint(500, 5000)

                ticket_info = (
                    f"Passenger Name: {name}\n"
                    f"Train: {train_name}\n"
                    f"Fare: ₹{fare}\n"
                    f"Age: {passenger[2]}\n"
                    f"Gender: {passenger[3]}\n"
                    f"Departure: {passenger[6]}\n"
                    f"Destination: {passenger[7]}"
                )

                ticket_label = tk.Label(ticket_frame, text=ticket_info, font=("Helvetica", 12), bg="#34495E", fg="#ECF0F1", justify="left")
                ticket_label.grid(row=1, column=0, columnspan=2, pady=10)
            else:
                show_message("Error", "Passenger not found.")
        else:
            show_message("Error", "Please enter a valid Passenger ID.")

    tk.Button(ticket_window, text="Generate Ticket", command=generate_ticket, bg="#1ABC9C", fg="white", font=("Helvetica", 12), relief="solid", width=20, height=2).pack(pady=20)

# Menu with simple, clean buttons
menu_frame = tk.Frame(root, bg="#2C3E50", pady=20)
menu_frame.pack(pady=30)

tk.Button(menu_frame, text="Add Passenger", command=add_passenger, bg="#1ABC9C", fg="white", font=("Helvetica", 14, "bold"), relief="solid", width=20, height=2).grid(row=0, column=0, padx=20, pady=10)
tk.Button(menu_frame, text="View Passengers", command=view_passengers, bg="#1ABC9C", fg="white", font=("Helvetica", 14, "bold"), relief="solid", width=20, height=2).grid(row=0, column=1, padx=20, pady=10)
tk.Button(menu_frame, text="Generate Ticket", command=view_ticket, bg="#1ABC9C", fg="white", font=("Helvetica", 14, "bold"), relief="solid", width=20, height=2).grid(row=1, column=0, padx=20, pady=10)

root.mainloop()

# Closing the MySQL connection after the application ends
cursor.close()
conn.close()
