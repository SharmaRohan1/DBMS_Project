import nsepython as nse
import pandas as pd
from datetime import date
import time
from timeit import default_timer as timer
import mysql.connector as connector;

today = date.today()

nifty_stock_list = pd.read_csv('nifty50.csv')
print(nifty_stock_list)
nifty_stocks_list_modified =[]
i=1

for int in nifty_stock_list.index: #this is used to
        print(nifty_stock_list.iloc[int].iat[0])
        nifty_stocks_list_modified.append(nifty_stock_list.iloc[int].iat[0])


print(nifty_stocks_list_modified);

con = connector.connect(host='localhost',
        port='3306',
        user='root',
        password='mySql@123',
        database='project1');

cur = con.cursor(buffered = True);
    

default = timer()
while True:
    j=1
    start_time = timer()

    nifty_stocks_ltp = []
    nifty_stocks_open = []


    for name in nifty_stocks_list_modified:
        try:
            nifty_stocks_ltp.append(nse.nse_eq(name)['priceInfo']['close'])
            nifty_stocks_open.append(nse.nse_eq(name)['priceInfo']['open'])
        except:
            nifty_stocks_ltp.append(nse.nse_eq(name)['priceInfo']['close'])
            nifty_stocks_open.append(nse.nse_eq(name)['priceInfo']['open'])

    print(nifty_stocks_ltp)
    print(nifty_stocks_open)
    print((timer() - default) % 120)

    i = 1;
    for ltp in nifty_stocks_ltp:
        query = "update stock_info set ltp = {} where srip_id = {}".format(ltp , i);
        cur.execute(query);
        i += 1;
        con.commit();
        # print(ltp);

    i = 1;
    for open in nifty_stocks_open:
        query = "update stock_info set open = {} where srip_id = {}".format(open , i);
        cur.execute(query);
        i += 1;
        con.commit();
        # print(open);

    for i in range(1,51):
        absolute = nifty_stocks_ltp[i - 1] - nifty_stocks_open[i - 1];
        absolute_percent = ((nifty_stocks_ltp[i - 1] - nifty_stocks_open[i - 1]) / nifty_stocks_open[i - 1]) * 100;
        query = "update stock_info set change_abs = {} where srip_id = {}".format(absolute ,i);
        cur.execute(query);

        query1 = "update stock_info set change_per = {} where srip_id = {}".format(absolute_percent ,i);
        cur.execute(query1);
        con.commit();


    time.sleep((120 - (timer() - default)) % 120);
    
