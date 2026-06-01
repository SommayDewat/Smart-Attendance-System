import customtkinter as ctk
import os

from database import connect_db
from datetime import date

from export_report import export_attendance
from pdf_report import generate_pdf_report


# -------------------------------------------------
# APP SETTINGS
# -------------------------------------------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# -------------------------------------------------
# OPEN MODULES
# -------------------------------------------------

def open_students():
    os.system("python manage_students.py")


def open_attendance():
    os.system("python attendance.py")


def open_records():
    os.system("python view_attendance.py")


def open_percentage():
    os.system("python attendance_percentage.py")


# -------------------------------------------------
# DATABASE STATS
# -------------------------------------------------

def get_total_students():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM students"
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_present_today():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date=%s
        AND status='Present'
        """,
        (date.today(),)
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_absent_today():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date=%s
        AND status='Absent'
        """,
        (date.today(),)
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_attendance_rate():

    total_students = get_total_students()
    present_today = get_present_today()

    if total_students == 0:
        return 0

    return round(
        (present_today / total_students) * 100,
        2
    )


# -------------------------------------------------
# CARD COMPONENT
# -------------------------------------------------

def create_card(parent, title, value):

    card = ctk.CTkFrame(
        parent,
        width=250,
        height=140,
        corner_radius=15
    )

    card.pack(
        side="left",
        padx=10
    )

    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text=title,
        font=("Segoe UI", 18, "bold")
    ).pack(pady=(20, 10))

    ctk.CTkLabel(
        card,
        text=str(value),
        font=("Segoe UI", 30, "bold")
    ).pack()

    return card


# -------------------------------------------------
# LOGOUT
# -------------------------------------------------

def logout():
    app.destroy()


# -------------------------------------------------
# MAIN WINDOW
# -------------------------------------------------

app = ctk.CTk()

app.title("Smart Attendance System")
app.geometry("1300x750")


# -------------------------------------------------
# HEADER
# -------------------------------------------------

header = ctk.CTkLabel(
    app,
    text="📊 Smart Attendance Dashboard",
    font=("Segoe UI", 32, "bold")
)

header.pack(pady=20)


# -------------------------------------------------
# CARDS
# -------------------------------------------------

cards_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

cards_frame.pack(pady=20)

create_card(
    cards_frame,
    "Total Students",
    get_total_students()
)

create_card(
    cards_frame,
    "Present Today",
    get_present_today()
)

create_card(
    cards_frame,
    "Absent Today",
    get_absent_today()
)

create_card(
    cards_frame,
    "Attendance Rate",
    f"{get_attendance_rate()}%"
)


# -------------------------------------------------
# BUTTONS SECTION
# -------------------------------------------------

button_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)

button_frame.pack(
    pady=30,
    padx=20
)


ctk.CTkButton(
    button_frame,
    text="👨‍🎓 Manage Students",
    command=open_students,
    width=250,
    height=45
).grid(row=0, column=0, padx=15, pady=15)


ctk.CTkButton(
    button_frame,
    text="📅 Mark Attendance",
    command=open_attendance,
    width=250,
    height=45
).grid(row=0, column=1, padx=15, pady=15)


ctk.CTkButton(
    button_frame,
    text="📋 View Records",
    command=open_records,
    width=250,
    height=45
).grid(row=1, column=0, padx=15, pady=15)


ctk.CTkButton(
    button_frame,
    text="📊 Attendance Percentage",
    command=open_percentage,
    width=250,
    height=45
).grid(row=1, column=1, padx=15, pady=15)


ctk.CTkButton(
    button_frame,
    text="📥 Export Excel Report",
    command=export_attendance,
    width=250,
    height=45
).grid(row=2, column=0, padx=15, pady=15)


ctk.CTkButton(
    button_frame,
    text="📄 Export PDF Report",
    command=generate_pdf_report,
    width=250,
    height=45
).grid(row=2, column=1, padx=15, pady=15)


ctk.CTkButton(
    button_frame,
    text="🚪 Logout",
    command=logout,
    width=250,
    height=45
).grid(row=3, column=0, columnspan=2, pady=20)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

ctk.CTkLabel(
    app,
    text="Python + MySQL Attendance Management System",
    font=("Arial", 12)
).pack(pady=15)


# -------------------------------------------------
# RUN APP
# -------------------------------------------------

app.mainloop()
