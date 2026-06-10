#%% Librerias y paquetes 
import numpy as np
from uncertainties import ufloat, unumpy
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import os
import chardet
import re
from datetime import datetime
pendiente_HvsI = 3716.3 # 1/m
ordenada_HvsI = 1297.0 # A/m
# from clase_resultados import ResultadosESAR
#%% Lector Templog
def lector_templog(path):
    '''
    Busca archivo *templog.csv en directorio especificado.
    muestras = False plotea solo T(dt).
    muestras = True plotea T(dt) con las muestras superpuestas
    Retorna arrys timestamp,temperatura
    '''
    data = pd.read_csv(path,sep=';',header=5,
                            names=('Timestamp','T_CH1','T_CH2'),usecols=(0,1,2),
                            decimal=',',engine='python')
    temp_CH1  = pd.Series(data['T_CH1']).to_numpy(dtype=float)
    temp_CH2  = pd.Series(data['T_CH2']).to_numpy(dtype=float)
    timestamp = np.array([datetime.strptime(date,'%Y/%m/%d %H:%M:%S') for date in data['Timestamp']])

    time = np.array([(t-timestamp[0]).total_seconds() for t in timestamp])
    return timestamp,time,temp_CH1, temp_CH2



#%% 1- 500uL EG 55 FF 45 LN2 RF300-152
print('-'*50,'\nEG 55 FF 45 LN2 RF300-152','\n')
temps_500_CPA_EG55FF45_1 = glob("1_LN2_to_RF/*.csv",recursive=True)
temps_500_CPA_EG55FF45_1.sort()
i=1
for p in temps_500_CPA_EG55FF45_1:
    print('  -',i,p)
    i+=1
    
fig1,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('1.1 - EG 55% FF 45% - LN2 --> RF',loc='left')
ax2.set_title('1.2 - EG 55% FF 45% - LN2 --> RT',loc='left')


for p in temps_500_CPA_EG55FF45_1[:-1]:
    _,time,temp_CH1, _ = lector_templog(p)
    ax1.plot(time,temp_CH1,label=os.path.basename(p).split('.')[0])

_,time_RT,temp_CH1_RT, _ = lector_templog(temps_500_CPA_EG55FF45_1[-1])
ax1.plot(time_RT,temp_CH1_RT,'C3--',label=os.path.basename(temps_500_CPA_EG55FF45_1[-1]).split('.')[0])
    

for p in temps_500_CPA_EG55FF45_1[-1:]:
    _,time,temp_CH1, _ = lector_templog(p)
    ax2.plot(time,temp_CH1,'C3--',label=os.path.basename(p).split('.')[0])
    ax2.plot(time[125:150],temp_CH1[125:150],'o',c='tab:purple',alpha=0.5,zorder=-1)
    ax2.plot(time[300:340],temp_CH1[300:340],'o',c='tab:purple',alpha=0.5,zorder=-1)
ax2.set_xlim(60,400)
ax1.set_xlim(0,160)
ax2.set_xlabel('t (s)')
ax1.legend(title='f = 300 kHz   Idc = 152 dA',
           loc='lower right',
           shadow=True,frameon=True)
ax2.legend(loc='lower right',
           shadow=True,frameon=True)

for a in (ax1,ax2):
    # a.set_xlim(0,)
    # a.axhline(-120,color='k',ls='--',lw=0.5)
    a.grid()
    a.set_ylabel('T (°C)')

#%% 2 - 500 uL 
print('-'*50,'\nEG 55 FF 45 LN2 RF300- Idc= [150, 125, 100, 075, 050] dA','\n')

temps_500_EG55_FF45_2 = glob("2_EG55_FF45_LN2_to_RF_150_125_100_075_050/*.csv",recursive=True)
temps_500_EG55_FF45_2.sort()
for p in temps_500_EG55_FF45_2:
    print('  -',os.path.basename(p))
Idc_values = [15.0, 12.5, 10.0, 7.5, 5.0,0]
H0=[(h*pendiente_HvsI+ordenada_HvsI)/1000 for h in Idc_values]  

fig2,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('2.1 - EG 55% FF 45% - LN2 --> RF - Idc = [150, 125, 100] dA',loc='left')
ax2.set_title('2.2 - EG 55% FF 45% - LN2 --> RF - Idc = [75, 50, 00] dA',loc='left')

for i,p in enumerate(temps_500_EG55_FF45_2[:3]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')

for i,p in enumerate(temps_500_EG55_FF45_2[3:]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')

for a in (ax1,ax2):
    a.set_xlim(0,175)
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlim(80,350)

ax2.set_xlabel('t (s)')

#%%3  
print('-'*50,'\nEG 53 FF 47 LN2 RF300- Idc= [150, 125, 100, 075, 050] dA','\n')

temps_500_EG53_FF47 = glob("3_EG53_FF47_LN2_to_RF_150_125_100_075_050/*.csv",recursive=True)
temps_500_EG53_FF47.sort()
for p in temps_500_EG53_FF47:
    print('  -',os.path.basename(p))
Idc_values = [15.0, 12.5, 10.0, 7.5, 5.0,0]
H0=[(h*pendiente_HvsI+ordenada_HvsI)/1000 for h in Idc_values]  

fig3,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('3.1 - EG 53% FF 47% - LN2 --> RF - Idc = [150, 125, 100] dA',loc='left')
ax2.set_title('3.2 - EG 53% FF 47% - LN2 --> RF - Idc = [75, 50, 00] dA',loc='left')

for i,p in enumerate(temps_500_EG53_FF47[:3]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')

for i,p in enumerate(temps_500_EG53_FF47[3:]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')

for a in (ax1,ax2):
    a.set_xlim(0,175)
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlim(80,350)
ax2.set_xlabel('t (s)')

#%%4  
print('-'*50,'\nEG 51 FF 49 LN2 RF300- Idc= [150, 125, 100, 075, 050] dA','\n')
temps_500_EG51_FF49 = glob("4_EG51_FF49_LN2_to_RF_150_125_100_075_050/*.csv",recursive=True)
temps_500_EG51_FF49.sort()
for p in temps_500_EG51_FF49:
    print('  -',os.path.basename(p))
Idc_values = [15.0, 12.5, 10.0, 7.5, 5.0,0]
H0=[(h*pendiente_HvsI+ordenada_HvsI)/1000 for h in Idc_values]  

fig4,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('4.1 - EG 51% FF 49% - LN2 --> RF - Idc = [150, 125, 100] dA',loc='left')
ax2.set_title('4.2 - EG 51% FF 49% - LN2 --> RF - Idc = [75, 50, 00] dA',loc='left')

for i,p in enumerate(temps_500_EG51_FF49[:3]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')

for i,p in enumerate(temps_500_EG51_FF49[3:]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')
ax1.set_xlim(0,160)
ax2.set_xlim(00,350)

for a in (ax1,ax2):
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlabel('t (s)')

#%% Salvo figuras
figs=[fig1,fig2,fig3,fig4]
names=['EG55FF45_LN2_RF','EG55FF45_LN2_RF_Idc','EG53FF47_LN2_RF_Idc','EG51FF49_LN2_RF_Idc']
for i,fig in enumerate(figs):
    fig.savefig(f'{names[i]}.png',dpi=300)

#%%
