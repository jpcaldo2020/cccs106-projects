import mysql.connector
from mysql.connector import Error

def connect_db():
    """
    Establishes connection to MySQL database
    Returns mysql.connector connection object
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword123",  # Replace with your MySQL root password
            database="fletapp"
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise