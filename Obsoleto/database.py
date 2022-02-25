from getpass import getpass
from mysql.connector import *

try:
    connection = connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="drawfit"
    )
    print(connection)
except Error as e:
    print(e)

cursor = connection.cursor()


# cursor.execute("CREATE DATABASE drawfit")







