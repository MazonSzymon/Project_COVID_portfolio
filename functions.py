# -*- coding: utf-8 -*-
"""functions

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aNAYOyInGd-6bqDDNJ9VV6cNwR1fH-7S

#  ***Analysis of investing at GPW in 2020*** 

---

#Downloading libraries and creating wig20 table
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as pdr 
# %load_ext google.colab.data_table

#Set up plot
from cycler import cycler
plt.style.use('ggplot')
plt.rc('axes', facecolor='white', edgecolor='black', grid = False, axisbelow = True)
plt.rc('grid',color='gray', linestyle='solid', linewidth=0.5)
plt.rc('patch', edgecolor='black')
plt.rc('legend', shadow=True, handlelength=1, fontsize=10, edgecolor = 'black', facecolor='white')

#Creat a DataFrame with names of WIG 20 one joint stock company
stocks_at_WIG20 = pd.DataFrame(np.array([
    ['WIG20' , 'wig20.pl'],
    ['Alior Bank' , 'alr.pl'],
    ['CCC' , 'ccc.pl'],
    ['CD Projekt' , 'cdr.pl'],
    ['Cyfrowy Polsat SA' , 'cps.pl'],
    ['Dino Polska' , 'dnp.pl'],
    ['Jastrzebska Spolka Weglowa' , 'jsw.pl'],
    ['KGHM Polska Mied' , 'kgh.pl'],
    ['LPP' , 'lpp.pl'],
    ['Grupa Lotos SA' , 'lts.pl'],
    ['mBank' , 'mbk.pl'],
    ['Orange Polska' , 'opl.pl'],
    ['Bank Polska Kasa Opieki' , 'peo.pl'],
    ['PGE Polska Grupa Energetyczna' , 'pge.pl'],
    ['Polskie Gronictwo Naftowe i Gazownictwo' , 'pgn.pl'],
    ['Powszechna Kasa Oszczednosci Bank Polski' , 'pko.pl'],
    ['Play Communications SA' , 'ply.pl'],
    ['Powszechny Zaklad Ubezpieczen' , 'pzu.pl'],
    ['Santander Bank Polska' , 'spl.pl'],
    ['Tauron Polska Energia' , 'tpe.pl']
    ]), columns = ['Full_name','Short_name'])

"""# Functions

> ## Downloading data
"""

def get_data(stock,start_date, end_date):
  stooq_data = pdr.get_data_stooq(stock['Short_name'], start = start_date, end = end_date).sort_index()
  stooq_data['Stock_name'] = stock['Full_name']
  df = stooq_data.copy()
  df.rename(columns = { stock['Short_name'] : 'stooq_data'},inplace = True)
  return df

""">## WIG20 Tabel

>> ### Creating WIG20 frame
"""

def WIG20_frame(start_date,end_date):
  WIG20 = pd.DataFrame()
  for i in range(len(stocks_at_WIG20)):
    tmp = get_data(stocks_at_WIG20.iloc[i],start_date,end_date)
    WIG20 = WIG20.append(tmp)
  return WIG20

""">> ### WIG20"""

start_date = dt.datetime(2020,1,1)
end_date = dt.date.today()
WIG20_tabel = WIG20_frame(start_date,end_date) #Run once time because its API

WIG20_by_stocks = WIG20_tabel.groupby('Stock_name') #This is our basic tabel to creating portfolios !!!!!!!!!!!!!!!!!

""">>### Basic information"""

def stock_info(stock):
  df = WIG20_by_stocks.get_group(stock)
  print("-"*50)
  print("5 First and 5 Last records")
  print("-"*50)
  print(df.head())
  print("-"*50)
  print(df.tail())
  print("-"*50)
  print("Basic information about data set")
  print("-"*50)
  print(df.info())
  print("-"*50)
  print("Basic statistic about data")
  print("-"*50)
  print(df.describe())
  print("-"*50+"\n")

""">>### Visualization of stock actions"""

def stock_visualization(stock):
  df = WIG20_by_stocks.get_group(stock)
  plt.figure(figsize=(28,8))
  #1 Visualization close value
  plt.subplot(1,2,1)
  plt.plot(df['Close'], color = 'blue')
  plt.title(stock + " close value")
  plt.grid()
  #2 Visulization volume value
  plt.subplot(1,2,2)
  plt.plot(df['Volume'], color = 'green')
  plt.title(stock + ' volume value')
  plt.grid()
  return plt.show()

""">> ### Relative change"""

def stock_rate(stock):
  df = WIG20_by_stocks.get_group(stock)
  plt.figure(figsize=(28,8))
  #1 Visualization Rate of Return
  plt.subplot(121)
  plt.plot(np.log(df['Close'].pct_change()+1), color = 'blue')
  plt.title(stock + " Rate of Return")
  plt.grid()
  #2 Histogram Rate of Return
  plt.subplot(122)
  plt.hist(np.log(df['Close'].pct_change()+1), color = 'gray', bins = 50)
  plt.title(stock + ' Rate of Return')
  plt.grid()
  return plt.show()

""">## Portfolio

>> ### Creat investment
"""

def creat_investment(stocks,investment):
  df = pd.DataFrame(columns=['Stock','Value'])
  df['Stock'] = stocks
  df['Value'] = investment
  df['Value'] = df['Value'].astype('float')
  df.sort_values('Stock', inplace = True)
  return df

""">> ### Preparing portfolio"""

def preparing_portfolio(total_investments,stocks):
  
  #Get data to stock
  def get_frame(stock):
    return WIG20_by_stocks.get_group(stock)
  
  stocks_data = map(get_frame,stocks)
  df = pd.concat(stocks_data, keys = stocks, names= ['Stock','Date'])
  df = df.reset_index().pivot(index='Date',columns = 'Stock', values = ['Close','Volume'])
  portfolio_change = (1 + df[['Close']].pct_change()).cumprod().fillna(1).round(2).rename(columns = {'Close' : 'ROI'})
  integrer_of_stocks = (total_investments/df['Close'].iloc[0]).astype(int).values
  investment_by_stocks = integrer_of_stocks  * df['Close'].iloc[0]
  rest_investment = total_investments - investment_by_stocks.values
  rest_investment
  investment_value = portfolio_change.multiply(investment_by_stocks.values).rename(columns = {'ROI' : 'Investments_value'}).round(2)
  investment_value['Sum_of_investments'] = investment_value.sum(axis=1).round(2)
  portfolio_value = pd.concat([df,portfolio_change,investment_value], axis = 1)
  portfolio_value['ROI_of_investments'] = (1 + portfolio_value[['Sum_of_investments']].pct_change()).cumprod().fillna(1).round(2)
  tmp = portfolio_value.columns.to_frame()['Stock'].values
  print("-"*50)
  print("We first want to inveset {first_invest_value} PLN".format( first_invest_value = total_investments.sum()))
  print("We get")
  for i in range(len(integrer_of_stocks)):
    print("{integrer} stocks {company} for {price} PLN total {total} PLN".format(
        integrer = integrer_of_stocks[i], company = portfolio_value[['Investments_value'][0]].columns[i], price = portfolio_value['Close'].iloc[0][i], total = portfolio_value['Investments_value'][tmp[i]][0]))
  print("and the rest from investment {rest} PLN".format(rest = rest_investment.sum().round(2)))
  return portfolio_value

def preparing_portfolio_by_date(total_investments,stocks,date):
  
  #Get data to stock
  def get_frame(stock):
    return WIG20_by_stocks.get_group(stock)
  
  stocks_data = map(get_frame,stocks)
  df = pd.concat(stocks_data, keys = stocks, names= ['Stock','Date'])
  df = df.reset_index(inplace = True)
  df = df[df['Date'] >= date]
  df = df.reset_index().pivot(index='Date',columns = 'Stock', values = ['Close','Volume'])
  portfolio_change = (1 + df[['Close']].pct_change()).cumprod().fillna(1).round(2).rename(columns = {'Close' : 'ROI'})
  integrer_of_stocks = (total_investments/df['Close'].iloc[0]).astype(int).values
  investment_by_stocks = integrer_of_stocks  * df['Close'].iloc[0]
  rest_investment = total_investments - investment_by_stocks.values
  rest_investment
  investment_value = portfolio_change.multiply(investment_by_stocks.values).rename(columns = {'ROI' : 'Investments_value'}).round(2)
  investment_value['Sum_of_investments'] = investment_value.sum(axis=1).round(2)
  portfolio_value = pd.concat([df,portfolio_change,investment_value], axis = 1)
  portfolio_value['ROI_of_investments'] = (1 + portfolio_value[['Sum_of_investments']].pct_change()).cumprod().fillna(1).round(2)
  tmp = portfolio_value.columns.to_frame()['Stock'].values
  print("-"*50)
  print("At {start_date} We first want to inveset {first_invest_value} PLN".format(start_date = date.date(), first_invest_value = total_investments.sum()))
  print("We get")
  for i in range(len(integrer_of_stocks)):
    print("{integrer} stocks {company} for {price} PLN total {total} PLN".format(
        integrer = integrer_of_stocks[i], company = portfolio_value[['Investments_value'][0]].columns[i], price = portfolio_value['Close'].iloc[0][i], total = portfolio_value['Investments_value'][tmp[i]][0]))
  print("and the rest from investment {rest} PLN".format(rest = rest_investment.sum().round(2)))
  return portfolio_value

""">> ### portfolio_summary"""

def portfolio_summary(portfolio):
  #Stocks list
  tmp = portfolio.columns.to_frame()['Stock'].values
  portfolio_list = ''
  for i in range(int(len(tmp)/4)):
    portfolio_list = portfolio_list + tmp[i]
    if i < len(tmp)/4 -2:
      portfolio_list = portfolio_list + ", "

  #Basic information about investment
  print("-"*50)
  print("At {start_date} We invested {initial_investment_value} PLN, spliced by company".format(
      start_date = portfolio.index[0].date() , initial_investment_value = portfolio['Sum_of_investments'][0]
  ))
  for i in range(int(len(tmp)/4)):
      print("{value} PLN at stocks {company}".format(value = portfolio['Investments_value'][tmp[i]][0], company = tmp[i]))
  
  #Information about our initial stock 
  print("-"*50)
  print("We have ")
  for i in range(int(len(tmp)/4)):
      print("{integrer} stocks {company}".format(integrer = int(portfolio['Investments_value'][tmp[i]][0]/portfolio['Close'][tmp[i]][i]), company = tmp[i]))
  print("-"*50)
  print("On {end_date} it is all worth {investment_value} PLN,spliced by company".format(
      end_date = portfolio.index[-1].date(), investment_value = portfolio['Sum_of_investments'][-1]
  ))
  for i in range(int(len(tmp)/4)):
      print("{value} PLN at stocks {company}".format(value = portfolio['Investments_value'][tmp[i]][-1], company = tmp[i]))
  
  print("-"*50)
  print("Rate of investment is {ROI} %, spliced by comapny".format(
      ROI = ((portfolio['Sum_of_investments'][-1]/portfolio['Sum_of_investments'][0] -1)*100).round(2)
  ))
  for i in range(int(len(tmp)/4)):
      print("{ROI} % at stocks {company}".format(ROI = ((portfolio['Investments_value'][tmp[i]][-1]/portfolio['Investments_value'][tmp[i]][0] -1)*100).round(2), company = tmp[i]))
  
  print("-"*50 + "\n")
  #Graphs
  plt.figure( figsize = (28, 8 ))
  #1
  plt.subplot(121)
  for i in range(int(len(tmp)/4)):
    plt.plot(portfolio[['Investments_value'][0]][portfolio[['Investments_value'][0]].columns[i]], label = portfolio[['Investments_value'][0]].columns[i])
  plt.grid()
  plt.legend()
  plt.title('Value of investments by stocks')
  #2
  plt.subplot(122)
  plt.plot(portfolio['Sum_of_investments'])
  plt.title('Value of investment')
  plt.grid()
  plt.show()

  return

""">> ### Portfolio compare"""

def portfolio_compare(portfolio, benchmark):
  #Stocks list
  tmp = portfolio.columns.to_frame()['Stock'].values
  portfolio_list = ''
  for i in range(int(len(tmp)/4)):
    portfolio_list = portfolio_list + tmp[i]
    if i < len(tmp)/4 -2:
      portfolio_list = portfolio_list + ", "
  
  tmp = benchmark.columns.to_frame()['Stock'].values
  benchmark_list = ''
  for i in range(int(len(tmp)/4)):
    benchmark_list = benchmark_list + tmp[i]
    if i < len(tmp)/5 -2:
      benchmark_list = benchmark_list + ", "
  

  #compare
  print("-"*50)
  print("At {start_date} We invested {initial_investment_value} PLN at {stocks}".format(
      start_date = portfolio.index[0].date() , initial_investment_value = portfolio['Sum_of_investments'][0], stocks = portfolio_list
  ))
  print("-"*50)
  print("On {end_date} is worth {investment_value} PLN, Rate of investment is {ROI} %".format(
      end_date = portfolio.index[-1].date(), investment_value = portfolio['Sum_of_investments'][-1],
      ROI = ((portfolio['Sum_of_investments'][-1]/portfolio['Sum_of_investments'][0] -1)*100).round(2)
  ))
  
     
  print("Ratio investment to benchmark is {change}%".format(
     change = ((portfolio['Sum_of_investments'][-1]/benchmark['Sum_of_investments'][-1] - 1)*100).round(2)))
  print("-"*50+ "\n")
  #graphs
  plt.figure(figsize=(15,10))
  plt.plot(portfolio['Sum_of_investments'], color = 'green', label = portfolio_list)
  plt.plot(benchmark['Sum_of_investments'], color = 'red',label = benchmark_list)
  plt.title("Value of investment " + portfolio_list, fontsize = 22, fontweight="bold")
  plt.grid()
  plt.legend()

  return

""">>###Change interval"""

def change_interval(portfolio):
  print("-"*50)
  print("Week's mean" + "\n")
  print(portfolio.resample('W').mean().tail())
  
  print("-"*50+"\n")
  print("Month's last value" + "\n")
  print(portfolio.resample('M').last().tail())
  print("-"*50)
  return

""">>### Visualization of stock actions at our portfolio"""

def portfolio_visualization(portfolio):
  tmp = portfolio.columns.to_frame()['Stock'].values
  plt.figure( figsize = (28, 8 ))
  #1
  plt.subplot(121)
  for i in range(int(len(tmp)/4)):
    plt.plot(portfolio[['Close'][0]][portfolio[['Close'][0]].columns[i]], label = portfolio[['Close'][0]].columns[i])
  plt.grid()
  plt.legend()
  plt.title('Value of  by stocks')
  #2
  plt.subplot(122)
  plt.plot(portfolio['Sum_of_investments'])
  plt.title('Value of investment')
  plt.grid()
  return plt.show()

""">>### Relative change our portfolio"""

def portfolio_rate(portfolio):
  tmp = portfolio.columns.to_frame()['Stock'].values

  # Graphs
  for i in range(int(len(tmp)/4)):
    if (i) > len(tmp)/2-1:
      break
    else:
      #1
      plt.figure(figsize=(28,8))
      for k in range(0,2):
        if (k+i*2) > int(len(tmp)/4)-1:
          break
        else:
          plt.plot(np.log(portfolio['Close'].pct_change()+1)[portfolio[['Close'][0]].columns[i*2 + k]], label = portfolio[['Close'][0]].columns[i*2+k])
          plt.grid()
          plt.legend()
          plt.title('ROI')
      plt.show()
      #2 
      plt.figure(figsize=(28,8))
      for k in range(0,2):
        if (k+i*2) > int(len(tmp)/4)-1:
          break
        else:
          plt.subplot(121 + k)
          plt.hist(np.log(portfolio['Close'].pct_change()+1)[portfolio[['Close'][0]].columns[i*2 + k]], label = portfolio[['Close'][0]].columns[i*2+k])
          plt.grid()
          plt.legend()
          plt.title('ROI')
      plt.show()


  return plt.show()


