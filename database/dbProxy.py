from getpass import getpass
from mysql.connector import *

def start():
    try:
        conn = connect(
            host="localhost",
            user=input("> Enter username: "),
            password=getpass("> Enter password: ")
        )
    except Error as e:
        print("ERROR: Could not connect to localhost.")
        return None

    cursor = conn.cursor()

    cursor.execute("SHOW DATABASES LIKE 'drawfit'")

    if not cursor.fetchall():
        x = input("INFO: No databases with name 'drawfit'.\nWARNING: Create new empty database? [Y/n] ")
        if (x.lower() == 'y'):
            create(conn)
        else:
            print("INFO: Operation Aborted.")
            return None
    else:
        print("INFO: Found database with name 'drawfit' - connected.")
    
    cursor.execute("USE drawfit")

    return conn


def reset(conn):
    x = input("WARNING: Delete database? [Y/n] ")
    if (x.lower() == 'y'):
        conn.cursor().execute("DROP DATABASE IF EXISTS drawfit")
    else:
        print("INFO: Operation Aborted.")



def create(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS drawfit")
    cursor.execute("USE drawfit")
    executeScriptsFromFile(conn, "tables.sql")
    print("INFO: New database created.")
    






def executeScriptsFromFile(conn, filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                conn.cursor().execute(command)
        except IOError as msg:
            print ("Command skipped: ", msg)



conne = start()

conne.close()








