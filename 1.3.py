import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import datetime

group_number=2
path_dir = Path.cwd()/'data'/f'{group_number}'
# examine available files in your folder
list(path_dir.glob('*gz'))

name_of_site='US-MMS'

# load dataset
site_file=name_of_site+'_clean.csv.gz'
path_data = path_dir/site_file
df_data = pd.read_csv(path_data, index_col='time',parse_dates=['time'])

#save this as something df_data.head()

fontsize=15
df_data.loc[:,['SWIN','LWIN','SWOUT','LWOUT']].plot(figsize=(12,4),fontsize=fontsize)
plt.ylabel('Flux (W m$^{-2}$)',fontsize=fontsize)
plt.xlabel('Time',fontsize=fontsize)

def DOY_to_datetime(row):
    year=int(row['modis_date'][1:5])
    DOY=int(row['modis_date'][5:])
    return datetime.datetime(year, 1, 1) + datetime.timedelta(DOY - 1)

df_LAI=pd.read_csv('data/MODIS_LAI_AmeriFlux/statistics_Lai_500m-'+name_of_site+'.csv')
df_LAI.columns=['product']+[i.split(' ')[1] for i in df_LAI.columns if i!='product']
df_LAI=df_LAI.filter(['modis_date','value_mean'])

df_LAI.set_index(df_LAI.apply(DOY_to_datetime,axis=1),inplace=True)
df_LAI.drop('modis_date',axis=1,inplace=True)

#save this as something df_LAI.head()

fontsize=15
df_LAI.plot(legend=False,figsize=(12,4),fontsize=fontsize)
plt.ylabel('LAI',fontsize=fontsize)
plt.xlabel('Time',fontsize=fontsize)

start_period='2006-01-01'
end_period='2007-01-01'

df_data_period=df_data.loc[start_period:end_period]
df_LAI_period=df_LAI.loc[start_period:end_period]

ser_alb=df_data_period['SWOUT']/df_data_period['SWIN']
ser_alb=ser_alb[ser_alb.index.time==datetime.time(12, 0)]
ser_alb_clean=ser_alb[ser_alb.between(0,1)&(df_data_period['SWIN']>5)]

plt.rcParams.update({'font.size': 15})
plt.figure(figsize=(12,4))
plt.scatter(ser_alb_clean.index,ser_alb_clean)
plt.ylabel('Albedo')
plt.xlabel('Time')

plt.rcParams.update({'font.size': 15})
fig,axs=plt.subplots(2,1,figsize=(12,8))
fig.subplots_adjust(hspace=0)
ax1=axs[0]
ax2=axs[1]

ax1.scatter(ser_alb_clean.index,ser_alb_clean)
ax1.set_ylabel('Albedo')
#ax1.set_xlim([ser_alb_clean[1],ser_alb_clean[-1]])
ax1.set_xticks([])
ax1.set_title(name_of_site)

ax2.plot(df_LAI_period.index,df_LAI_period)
ax2.set_ylabel('LAI')
ax2.set_xlabel('Time')
#ax2.set_xlim([df_LAI_period[1],df_LAI_period[-1]])



