# These packages are necessary later on. Load all the packages in one place for consistency
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#The path of the directory where all AMF data are
#path_dir = Path.cwd()/'data'/'AMF-clean'
path_dir = Path.cwd()/'data'/'2'

name_of_site = 'US-MMS_clean.csv.gz'
path_data = path_dir/name_of_site
path_data.resolve()

df_data = pd.read_csv(path_data, index_col='time',parse_dates=['time'])

all_sites_info =  pd.read_csv('data/site_info.csv')
site_info=all_sites_info[all_sites_info['Site Id'] == name_of_site.split('_clean')[0]]

first_5_rows = df_data.head(5)
describe = df_data.describe()

df_data.loc[:,['SWIN','LWIN','SWOUT','LWOUT']].plot(figsize=(15,4))
df_data.loc[:,['LE','H']].plot(figsize=(15,4))
df_data.loc[:,['TA']].plot(figsize=(15,4))
df_data.loc[:,['P']].plot(figsize=(15,4))
df_data.loc[:,['WS']].plot(figsize=(15,4))
df_data.loc[:,['RH']].plot(figsize=(15,4))
df_data.loc[:,['PA']].plot(figsize=(15,4))

date = '2001 10 21'
df_data.loc[:,['SWIN','LWIN','SWOUT','LWOUT']].dropna().loc[date].plot()

NetSW = df_data.loc[date,'SWIN']-df_data.loc[date,'SWOUT']
NetLW = df_data.loc[date,'LWIN']-df_data.loc[date,'LWOUT']
Netrad_calc=NetSW+NetLW
df_data.loc[date,'NETRAD'].plot(color='r',label='NETRAD from data')
Netrad_calc.plot(color='b',marker='o',label='NETRAD calculated')
plt.legend()

df_data.loc[:,['NETRAD','H','LE']].dropna().loc[date].plot()

ser_alb=df_data['SWOUT']/df_data['SWIN']
ser_alb[ser_alb.between(0,1)&(df_data['SWIN']>5)].loc[date].plot(marker='o')