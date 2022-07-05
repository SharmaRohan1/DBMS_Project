import mysql.connector as connector
from constant import userList;


con = connector.connect(host='localhost',
        port='3306',
        user='root',
        password='mySql@123',
        database='project1');
    

#CREATING TABLES
query1 = 'create table stock_info(srip_id int primary key , company_name varchar(20) , ltp double default 0.0 , change_abs double , change_per double , open double default 0.0 )';
cur = con.cursor();
cur.execute(query1);
print('stock info created');

query2 = 'create table user_info(email varchar(20) primary key , fname varchar(10) , lname varchar(10) , password varchar(20))';
cur = con.cursor();
cur.execute(query2);
print('User info created');

query3 = 'create table portfolio(email varchar(20),company_name varchar(20),Qty int,buy_price double,MTM double,primary key(email,company_name),foreign key(email) references user_info(email) ,foreign key(company_name) references stock_info(company_name) )';
cur.execute(query3);
print('Portfolio creation');






