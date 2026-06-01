from tkinter import ttk

from numpy import record
from database import connect_db
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- LOAD DATA ---------------- #

def load_data(search_text=""):

    connection = connect_db()
    cursor = connection.cursor()

    query = """
    SELECT
        students.student_id,
        students.name,
        students.class,
        attendance.attendance_date,
        attendance.status

    FROM attendance

    INNER JOIN students
    ON attendance.student_id = students.student_id
    ORDER BY attendance.attendance_date DESC,
    students.student_id ASC
    """

    if search_text != "":
        query += """ 
        WHERE students.name LIKE %s
        OR students.roll_no LIKE %s
        """
        cursor.execute(
            query,
            ('%' + search_text + '%', '%' + search_text + '%')
        )
    else:
        cursor.execute(query)

    records = cursor.fetchall()

    attendance_table.delete(
        *attendance_table.get_children()
    )

    for record in records:
        status = record[4]

        if status == "Present":
            status = "🟢 Present"
        else:
            status = "🔴 Absent"

        attendance_table.insert(
            "",
            "end",
            values=(
                record[0],
                record[1],
                record[2],
                record[3],
                status
            )
        )


    total_label.configure(
        text=f"Total Records: {len(records)}"
    )

    connection.close()


# ---------------- SEARCH ---------------- #

def search_data():

    load_data(
        search_entry.get()
    )

app = ctk.CTk()

app.title("Attendance Records")
app.geometry("1400x800")
app.minsize(1300, 750)

title = ctk.CTkLabel(
    app,
    text="📋 Attendance Records",
    font=("Segoe UI", 28, "bold")
)

title.pack(pady=20)

# ---------------- MAIN FRAME ---------------- #

main_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# ---------------- SEARCH FRAME ---------------- #

search_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

search_frame.pack(
    pady=15
)

search_entry = ctk.CTkEntry(
    search_frame,
    width=400,
    placeholder_text="Search Name or Roll Number..."
)

search_entry.grid(
    row=0,
    column=0,
    padx=10
)

search_btn = ctk.CTkButton(
    search_frame,
    text="Search",
    width=120,
    command=search_data
)

search_btn.grid(
    row=0,
    column=1,
    padx=5
)

show_all_btn = ctk.CTkButton(
    search_frame,
    text="Show All",
    width=120,
    command=load_data
)

show_all_btn.grid(
    row=0,
    column=2,
    padx=5
)

search_entry.bind(
    "<Return>",
    lambda event: search_data()
)

# ---------------- TOTAL RECORDS ---------------- #

total_label = ctk.CTkLabel(
    main_frame,
    text="Total Records: 0",
    font=("Arial", 13, "bold")
)

total_label.pack(pady=5)

# ---------------- TABLE FRAME ---------------- #

table_frame = ctk.CTkFrame(
    main_frame
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

# ---------------- SCROLLBARS ---------------- #

scroll_y = ttk.Scrollbar(
    table_frame,
    orient="vertical"
)

scroll_y.pack(
    side="right",
    fill="y"
)

scroll_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal"
)

scroll_x.pack(
    side="bottom",
    fill="x"
)

# ---------------- TREEVIEW STYLE ---------------- #

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#2b2b2b",
    foreground="white",
    fieldbackground="#2b2b2b",
    rowheight=30,
    font=("Arial", 11)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold")
)

# ---------------- TABLE ---------------- #

attendance_table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Name",
        "Class",
        "Date",
        "Status"
    ),
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(
    command=attendance_table.yview
)

scroll_x.config(
    command=attendance_table.xview
)

attendance_table.heading(
    "ID",
    text="Student ID"
)

attendance_table.heading(
    "Name",
    text="Student Name"
)

attendance_table.heading(
    "Class",
    text="Class"
)

attendance_table.heading(
    "Date",
    text="Attendance Date"
)

attendance_table.heading(
    "Status",
    text="Status"
)

attendance_table.column(
    "ID",
    width=100,
    anchor="center"
)

attendance_table.column(
    "Name",
    width=250
)

attendance_table.column(
    "Class",
    width=120,
    anchor="center"
)

attendance_table.column(
    "Date",
    width=150,
    anchor="center"
)

attendance_table.column(
    "Status",
    width=180,
    anchor="center"
)

attendance_table.pack(
    fill="both",
    expand=True
)
load_data()
app.mainloop()