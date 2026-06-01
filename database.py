import mysql.connector
def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="YOUR_USERNAME(usually 'root')",
        password="YOUR_PASSWORD",
        database="attendance_system"
    )
    return connection