from getpass import getpass
from mysql.connector import *

try:
    connection = connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: ")
    )
    print(connection)
except Error as e:
    print(e)

cursor = connection.cursor()

#cursor.execute("CREATE DATABASE IF NOT EXISTS drawfit")


#cursor.execute("SHOW DATABASES LIKE 'drawfitgfjf'")

#print(cursor.fetchall())

#for row in cursor.fetchall():
 #   print(row)

#if not cursor.fetchall():
#    print("yeweees")



cursor.execute("USE drawfit")
cursor.execute("USE drawfit")


connection.cursor().execute("DESCRIBE games")

for row in cursor.fetchall():
    print(row)






connection.close()







