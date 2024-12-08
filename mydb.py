import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    name ="fpmsdb" # your database name here
)

# Create a cursor object to interact with the database
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE IF NOT EXISTS FPMSdb")
print('Good to Go!')