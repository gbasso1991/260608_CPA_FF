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

for i,p in enumerate(temps_500_EG53_FF47_2[:3]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')

for i,p in enumerate(temps_500_EG53_FF47_2[3:]):
    _,time,temp_CH1, _ = lector_templog(p)
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')

for a in (ax1,ax2):
    a.set_xlim(0,175)
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlim(80,350)

ax2.set_xlabel('t (s)')






#%% 4 -  500uL_CPA_FF_LN2
print('-'*50,'\n500 uL CPA FF - Enfriamiento en LN2 - Calentamiento en RF','\n')
temps_500_CPA_FF_LN2 = glob("data/*500uL_CPA_FF_LN2*",recursive=True)
temps_500_CPA_FF_LN2.sort()
for p in temps_500_CPA_FF_LN2:
    print('  -',i,p)
    i+=1

fig4,ax4 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_500_CPA_FF_LN2:
    _,time,temp_CH1, _ = lector_templog(p)
    ax4.plot(time,temp_CH1,label=os.path.basename(p).split('.')[0])
ax4.set_title('4 - CPA FF - LN2 --> RF')
ax4.set_xlim(0,)
ax4.grid()
ax4.legend()
ax4.set_ylabel('T (°C)')
ax4.set_xlabel('t (s)')
    
#%% 5- 1000 uL EG60 agua 40 LN2
print('-'*50,'\n1000 uL 60% Etilenglicol 40% agua - Enfriamiento en LN2 - Calentamiento en BT','\n')
temps_1000_EG60_agua40_LN2 = glob("data/*1000uL_EG60_agua40_LN2*",recursive=True)
temps_1000_EG60_agua40_LN2.sort()
for p in temps_1000_EG60_agua40_LN2:
    print('  -',i,p)
    i+=1

fig5,ax5 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_1000_EG60_agua40_LN2:
    _,time,temp_CH1, _ = lector_templog(p)
    ax5.plot(time,temp_CH1,label=os.path.basename(p).split('.')[0])
ax5.set_title('5 - 60% Etilenglicol 40% agua - LN2 --> BT')
ax5.set_xlim(0,)
ax5.grid()
ax5.legend()    
ax5.set_ylabel('T (°C)')
ax5.set_xlabel('t (s)')

#%% 6- 500 uL EG60 FF40 LN2
print('-'*50,'\n500 uL 60% Etilenglicol 40% FF - Enfriamiento en LN2 - Calentamiento en RF','\n')
temps_500_EG60_FF40_LN2 = glob("data/*500uL_EG60_FF40_LN2*",recursive=True)
temps_500_EG60_FF40_LN2.sort()
for p in temps_500_EG60_FF40_LN2:
    print('  -',i,p)
    i+=1
fig6,ax6 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_500_EG60_FF40_LN2:
    _,time,temp_CH1, _ = lector_templog(p)
    ax6.plot(time,temp_CH1,'-',label=os.path.basename(p).split('.')[0])
ax6.set_title('6 - 60% Etilenglicol 40% FF - LN2 --> RF')
ax6.set_xlim(0,)
ax6.grid()
ax6.legend()
ax6.set_ylabel('T (°C)')
ax6.set_xlabel('t (s)')
#%% 7 - 500 uL 500uL_EG55_FF45 LN2
print('-'*50,'\n500 uL 55% Etilenglicol 45% FF - Enfriamiento en LN2 - Calentamiento en RF','\n')    
temps_500_EG55_FF45_LN2 = glob("data/*500uL_EG55_FF45_LN2*",recursive=True)
temps_500_EG55_FF45_LN2.sort()
for p in temps_500_EG55_FF45_LN2:
    print('  -',i,p)
    i+=1
fig7,ax7 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_500_EG55_FF45_LN2:
    _,time,temp_CH1, _ = lector_templog(p)
    ax7.plot(time,temp_CH1,'-',label=os.path.basename(p).split('.')[0])
ax7.set_title('7 - 55% Etilenglicol 45% FF - LN2 --> RF')
ax7.set_xlim(0,)
ax7.grid()
ax7.legend()
ax7.set_ylabel('T (°C)')
ax7.set_xlabel('t (s)')    
    
#%% 8 - 500uL_EG50_FF50_LN2
print('-'*50,'\n500 uL 50% Etilenglicol 50% FF - Enfriamiento en LN2 - Calentamiento en RF','\n')    
temps_500_EG50_FF50_LN2 = glob("data/*500uL_EG50_FF50_LN2*",recursive=True)
temps_500_EG50_FF50_LN2.sort()
for p in temps_500_EG50_FF50_LN2:
    print('  -',i,p)
    i+=1
fig8,ax8 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_500_EG50_FF50_LN2:
    _,time,temp_CH1, _ = lector_templog(p)
    ax8.plot(time,temp_CH1,'-',label=os.path.basename(p).split('.')[0])
ax8.set_title('8 - 50% Etilenglicol 50% FF - LN2 --> RF')
ax8.set_xlim(0,)
ax8.grid()
ax8.legend()
ax8.set_ylabel('T (°C)')
ax8.set_xlabel('t (s)')
#%% 9 - 500uL_EG47_FF53_LN2
print('-'*50,'\n500 uL 47% Etilenglicol 53% FF - Enfriamiento en LN2 - Calentamiento en RF','\n')    
temps_500_EG47_FF53_LN2 = glob("data/*500uL_EG47_FF53_LN2*",recursive=True)
temps_500_EG47_FF53_LN2.sort()
for p in temps_500_EG47_FF53_LN2:
    print('  -',i,p)
    i+=1
fig9,ax9 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_500_EG47_FF53_LN2:
    _,time,temp_CH1, _ = lector_templog(p)
    ax9.plot(time,temp_CH1,'-',label=os.path.basename(p).split('.')[0])
ax9.set_title('9 - 47% Etilenglicol 53% FF - LN2 --> RF')
ax9.set_xlim(0,)
ax9.grid()
ax9.legend()
ax9.set_ylabel('T (°C)')
ax9.set_xlabel('t (s)')

#%% 10- 500ul_EG47_FF53_LN2_BT
print('-'*50,'\n500 uL 47% Etilenglicol 53% FF - Enfriamiento en LN2 - Calentamiento en BT','\n')    
temps_500_EG47_FF53_LN2_BT = glob("data/*500ul_EG47_FF53_LN2_BT*",recursive=True)
temps_500_EG47_FF53_LN2_BT.sort()
for p in temps_500_EG47_FF53_LN2_BT:
    print('  -',i,p)
    i+=1
fig10,ax10 = plt.subplots(figsize=(9,4.5),constrained_layout=True)
for p in temps_500_EG47_FF53_LN2_BT:
    _,time,temp_CH1, _ = lector_templog(p)
    ax10.plot(time,temp_CH1,'-',label=os.path.basename(p).split('.')[0])
ax10.set_title('10 - 47% Etilenglicol 53% FF - LN2 --> BT')
ax10.set_xlim(0,)
ax10.grid()
ax10.legend()
ax10.set_ylabel('T (°C)')
ax10.set_xlabel('t (s)')        


# %% Salvo todas las figuras
figs=[fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10]
for i,fig in enumerate(figs):
    fig.savefig(f'figura_{i+1}.png',dpi=300)
#%%




#%%