import mysql.connector as connector;

con = connector.connect(host='localhost',
        port='3306',
        user='root',
        password='mySql@123',
        database='project1');
print('connection established');