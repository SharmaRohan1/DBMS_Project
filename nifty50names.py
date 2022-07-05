import nsepython as nse
import pandas as pd

nifty_stock_list = pd.read_csv('nifty50.csv')
print(nifty_stock_list)
nifty_stocks_list_modified =[]

for int in nifty_stock_list.index: #this is used to
        print(nifty_stock_list.iloc[int].iat[0])
        nifty_stocks_list_modified.append(nifty_stock_list.iloc[int].iat[0])


print(nifty_stocks_list_modified);

niftyStocks = nifty_stocks_list_modified;

