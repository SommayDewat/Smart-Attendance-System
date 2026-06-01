import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
import os

# ---------- APP SETTINGS ----------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------- LOGIN FUNCTION ----------

def login():

    username = username_entry.get()
    password = password_entry.get()

    connection = connect_db()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM teachers
    WHERE username=%s
    AND password=%s
    """

    cursor.execute(
        query,
        (username, password)
    )

    result = cursor.fetchone()

    connection.close()

    if result:

        messagebox.showinfo(
            "Success",
            "Login Successful"
        )

        app.destroy()

        os.system("python dashboard.py")

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )

# ---------- MAIN WINDOW ----------

app = ctk.CTk()

app.title("Smart Attendance System")
app.geometry("600x500")
app.resizable(False, False)

# ---------- TITLE ----------

title = ctk.CTkLabel(
    app,
    text="🎓 Smart Attendance System",
    font=("Segoe UI", 30, "bold")
)

title.pack(pady=40)

subtitle = ctk.CTkLabel(
    app,
    text="Manage Students & Attendance Efficiently",
    font=("Arial", 14)
)

subtitle.pack(pady=(0, 15))

# ---------- LOGIN FRAME ----------

frame = ctk.CTkFrame(
    app,
    width=450,
    height=350,
    corner_radius=15
)

frame.pack(pady=20)

# ---------- USERNAME ----------

username_label = ctk.CTkLabel(
    frame,
    text="Username"
)

username_label.pack(pady=(25,5))

username_entry = ctk.CTkEntry(
    frame,
    width=250,
    placeholder_text="Enter Username"
)

username_entry.pack()

# ---------- PASSWORD ----------

password_label = ctk.CTkLabel(
    frame,
    text="Password"
)

password_label.pack(pady=(20,5))

password_entry = ctk.CTkEntry(
    frame,
    width=250,
    show="*",
    placeholder_text="Enter Password"
)

password_entry.pack()

# ---------- BUTTON ----------

login_btn = ctk.CTkButton(
    frame,
    text="Login",
    width=200,
    command=login
)

login_btn.pack(pady=30)


# ---------- FOOTER ----------

footer = ctk.CTkLabel(
    app,
    text="Python + MySQL Attendance Management System",
    font=("Arial", 12)
)

footer.pack(pady=10)

# ---------- ENTER KEY LOGIN ----------

app.bind(
    "<Return>",
    lambda event: login_btn.invoke()
)
app.mainloop()