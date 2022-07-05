import mysql.connector as connector;
from constant import userList;
import nsepython as nse
import pandas as pd



con = connector.connect(host='localhost',
        port='3306',
        user='root',
        password='mySql@123',
        database='project1');
    


#INSERTING INTO USER_INFO TABLE
query = "insert into user_info values(%s , %s , %s , %s)";
cur = con.cursor();
cur.executemany(query , userList);
con.commit();
print('User info inserted');

#------------------------------------------------------------------------------------------

nifty_stock_list = pd.read_csv('nifty50.csv')
print(nifty_stock_list)
nifty_stocks_list_modified =[]

for int in nifty_stock_list.index: #this is used to
        print(nifty_stock_list.iloc[int].iat[0])
        nifty_stocks_list_modified.append(nifty_stock_list.iloc[int].iat[0])


print(nifty_stocks_list_modified);

niftyStocks = nifty_stocks_list_modified;

i = 1;
for names in niftyStocks:
    cur.execute("insert into stock_info(srip_id , company_name) values({} , '{}')".format(i , names));
    con.commit();
    i += 1;

