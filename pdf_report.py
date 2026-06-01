import os
from tkinter import messagebox
from database import connect_db
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report():

    try:

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
        """

        cursor.execute(query)

        records = cursor.fetchall()

        connection.close()
        os.makedirs(
            "reports",
            exist_ok=True
        )
        pdf_file = "reports/attendance_report.pdf"

        doc = SimpleDocTemplate(pdf_file)

        styles = getSampleStyleSheet()

        elements = []

        title = Paragraph(
            "Attendance Report",
            styles["Title"]
        )

        elements.append(title)
        elements.append(Spacer(1, 12))

        data = [
            [
                "ID",
                "Name",
                "Class",
                "Date",
                "Status"
            ]
        ]

        for row in records:
            data.append(list(row))

        table = Table(data)

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ])
        )

        elements.append(table)

        doc.build(elements)

        messagebox.showinfo(
            "Success",
            f"PDF Report Saved:\n{pdf_file}"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )