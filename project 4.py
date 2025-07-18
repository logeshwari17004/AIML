import mysql.connector
import csv
import datetime
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS employee")
cursor.execute("USE employee")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary (
        empid INT,
        firstname VARCHAR(100),
        lastname VARCHAR(100),
        email VARCHAR(50),
        phone VARCHAR(15),
        hire_date DATE,
        job_id VARCHAR(15),
        salary INT
    )
""")
filename = "employees1.csv"

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header

    for row in csvreader:
        print(row)
        empid = int(row[0])
        firstname = row[1]
        lastname = row[2]
        email = row[3]
        phone = row[4]
        hire_date = datetime.datetime.strptime(row[5], '%d-%b-%y').date()
        job_id = row[6]
        salary = int(row[7])

        sql = """
            INSERT INTO salary (
                empid, firstname, lastname, email, phone, hire_date, job_id, salary
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (empid, firstname, lastname, email, phone, hire_date, job_id, salary)
        cursor.execute(sql, val)

mydb.commit()

cursor.close()
mydb.close()
mydb.commit()