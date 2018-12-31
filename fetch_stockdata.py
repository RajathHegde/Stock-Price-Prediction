# quandl for financial data
import quandl
# pandas for data manipulation
import pandas as pd
# Get your key from quandl by signing up.
quandl.ApiConfig.api_key = 'YOUR KEY'


# Retrieve ADANIPORTS data from Quandl between 2017-2-1 and 2018-12-30.
adani=  quandl.get("NSE/ADANIPORTS", start_date="2017-2-1", end_date="2018-12-30")
adani.reset_index(level=0, inplace = True)
# Taking only Date and Open from the data. 
adani = adani[["Date","Open"]]
adani=adani.rename(columns = {'Open':'ADANIPORTS'})

# 'ind_nifty50list.csv' is a file containg the symbols of the stocks used.
nifty50=pd.read_csv('ind_nifty50list.csv')
# Getting only the symbols
symb=nifty50['Symbol']
# Adding 'NSE/' to symbols in 'ind_nifty50list.csv' usually gives you the quandl symbol of the stock.But you it will not work for BAJAJ-AUTO and M&M. 
nifty50.iloc[3, nifty50.columns.get_loc('Symbol')] = 'BAJAJ_AUTO'
nifty50.iloc[31, nifty50.columns.get_loc('Symbol')] = 'MM'

# Removing Adaniports symbol from nifty50
nifty50 = nifty50.iloc[1:]

# Getting opening price of all the nifty50 shares.
for i in nifty50['Symbol'].unique():
    table =  quandl.get('NSE'+'/'+i, start_date="2017-2-1", end_date="2018-12-30")
    table.reset_index(level=0, inplace = True)
    table=table[["Date","Open"]]
    table=table.rename(columns = {'Open':i})
    X = adani.merge(table, how='inner', on='Date')
    adani = X
# Creating a csv file containing historical data of the 50 compaines.  
X.to_csv('nifty50.csv')