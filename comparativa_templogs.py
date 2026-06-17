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
#% Gradiente
t,t_min=[],[]
T,T_min=[],[]
Indx_min,dT=[],[]

for p in temps_500_CPA_EG55FF45_1:
    _,time,temp_CH1,_ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])

col=['C0','C1','C2']
fig13,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[:3],T[:3],dT[:3])):
    l1=axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2=axs[i].twinx()
    ax2.set_ylabel('T (K)')
    ax2.set_yscale('log')
    l2=ax2.plot(x[Indx_min[i]:],y[Indx_min[i]:]+273,c=col[i],label='T')

    handles=l1+l2
    labels=[h.get_label() for h in handles]

    axs[i].legend(handles,labels,frameon=True,shadow=True,title=os.path.basename(temps_500_CPA_EG55FF45_1[i]).split('.')[0],loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(np.concatenate(t_min[:3]))-1,)
    a.grid()

axs[2].set_xlabel('t (s)')
fig13.suptitle('1.3 - EG 55% FF 45% - LN2 --> RF')

fig14,ax=plt.subplots(figsize=(10,4),constrained_layout=True)

l1=ax.plot(t[-1][Indx_min[-1]:],dT[-1][Indx_min[-1]:],'.-',label='dT/dt')
ax2=ax.twinx()
ax2.set_yscale('log')
ax2.set_ylabel('T (K)')
l2=ax2.plot(t[-1][Indx_min[-1]:],T[-1][Indx_min[-1]:]+273,'C3',label='T')
ax2.set_ylim(98,273)

handles=l1+l2
labels=[h.get_label() for h in handles]

ax.legend(handles,labels,frameon=True,shadow=True,title=os.path.basename(temps_500_CPA_EG55FF45_1[-1]).split('.')[0],loc='lower right',ncol=2)

ax.set_ylabel('dT/dt (°C/s)')
ax.set_xlim(t_min[-1][0]-5,400)
ax.grid()
ax.set_xlabel('t (s)')
fig14.suptitle('1.4 - EG 55% FF 45% - LN2 --> RT')

fig13.savefig('gradiente_temperatura_RF.png',dpi=300)
fig14.savefig('gradiente_temperatura_RT.png',dpi=300)
#%% 2 - 500 uL EG 55 FF 45 LN2 RF300
print('-'*50,'\nEG 55 FF 45 LN2 RF300- Idc= [150, 125, 100, 075, 050] dA','\n')

temps_500_EG55_FF45_2 = glob("2_EG55_FF45_LN2_to_RF_150_125_100_075_050/*.csv",recursive=True)
temps_500_EG55_FF45_2.sort()
for p in temps_500_EG55_FF45_2:
    print('  -',os.path.basename(p))
print('\n')

Idc_values = [15.0, 12.5, 10.0, 7.5, 5.0,0]
H0=[(h*pendiente_HvsI+ordenada_HvsI)/1000 for h in Idc_values]  
t,t_min=[],[]
T,T_min=[],[]
Indx_min,dT=[],[]

fig2,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('2.1 - EG 55% FF 45% - LN2 --> RF - Idc = [150, 125, 100] dA',loc='left')
ax2.set_title('2.2 - EG 55% FF 45% - LN2 --> RF - Idc = [75, 50, 00] dA',loc='left')

for i,p in enumerate(temps_500_EG55_FF45_2[:3]):
    _,time,temp_CH1, _ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])
    print(f'Temp minima = {temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} C ({temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]+273:.1f} K) alcanzada en {time[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} s')
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')
    ax1.plot(time,(np.gradient(temp_CH1,time)))

for i,p in enumerate(temps_500_EG55_FF45_2[3:]):
    _,time,temp_CH1, _ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])
    print(f'Temp minima = {temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} C ({temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]+273:.1f} K) alcanzada en {time[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} s')
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')
    ax2.plot(time,(np.gradient(temp_CH1,time)))

for a in (ax1,ax2):
    a.set_xlim(0,175)
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlim(60,350)
ax2.set_xlabel('t (s)')

#% Gradiente 
col=['C0','C1','C2']
fig23,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[:3],T[:3],dT[:3])):
    l1 = axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2 = axs[i].twinx()
    ax2.set_yscale('log')
    ax2.set_ylabel('T (K)')
    Tplot = y[Indx_min[i]:] + 273
    l2 = ax2.plot(x[Indx_min[i]:],y[Indx_min[i]:]+273,c=col[i],label='T')
    ax2.set_yticks([Tplot.min(),Tplot.max()])
    ax2.set_yticklabels([f'{Tplot.min():.0f}',f'{Tplot.max():.0f}'])
    ax2.minorticks_off()
    
    handles = l1 + l2
    labels = [h.get_label() for h in handles]

    axs[i].legend(handles, labels, frameon=True, shadow=True,title=f'H$_0$ = {H0[i]:.1f} kA/m',loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(t_min[:3])[0]-1,)
    a.grid()
axs[2].set_xlabel('t (s)')
fig23.suptitle('2.3 - EG 55% FF 45% - LN2 --> RF - Idc = [150, 125, 100] dA')

fig24,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[3:],T[3:],dT[3:])):
    l1 = axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2 = axs[i].twinx()
    ax2.set_yscale('log')
    ax2.set_ylabel('T (K)')
    Tplot = y[Indx_min[i]:] + 273
    l2 = ax2.plot(x[Indx_min[i]:],y[Indx_min[i]:]+273,c=col[i],label='T')
    ax2.set_yticks([Tplot.min(),273])
    ax2.set_yticklabels([f'{Tplot.min():.0f}','273'])
    ax2.minorticks_off()    
    ax2.set_ylim(98,273)

    handles = l1 + l2
    labels = [h.get_label() for h in handles]

    axs[i].legend(handles, labels, frameon=True, shadow=True,title=f'H$_0$ = {H0[i]:.1f} kA/m',loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(np.concatenate(t_min)[3:])-5,300)
    # a.set_ylim(bottom=0)
    a.grid()
axs[2].set_xlabel('t (s)')
fig24.suptitle('2.4 - EG 55% FF 45% - LN2 --> RF - Idc = [075, 050, 100] dA')

#salvo figuras
fig23.savefig('gradiente_temperatura_150_125_100.png',dpi=300)
fig24.savefig('gradiente_temperatura_075_050_000.png',dpi=300)

#%%3 
print('-'*50,'\nEG 53 FF 47 LN2 RF300- Idc= [150, 125, 100, 075, 050] dA','\n')

temps_500_EG53_FF47 = glob("3_EG53_FF47_LN2_to_RF_150_125_100_075_050/*.csv",recursive=True)
temps_500_EG53_FF47.sort()
for p in temps_500_EG53_FF47:
    print('  -',os.path.basename(p))
Idc_values = [15.0, 12.5, 10.0, 7.5, 5.0,0]
H0=[(h*pendiente_HvsI+ordenada_HvsI)/1000 for h in Idc_values]  
t,t_min=[],[]
T,T_min=[],[]
Indx_min,dT=[],[]

fig3,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('3.1 - EG 53% FF 47% - LN2 --> RF - Idc = [150, 125, 100] dA',loc='left')
ax2.set_title('3.2 - EG 53% FF 47% - LN2 --> RF - Idc = [75, 50, 00] dA',loc='left')

for i,p in enumerate(temps_500_EG53_FF47[:3]):
    _,time,temp_CH1, _ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])
    print(f'Temp minima = {temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} C ({temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]+273:.1f} K) alcanzada en {time[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} s')
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')
    ax1.plot(time,(np.gradient(temp_CH1,time)))

for i,p in enumerate(temps_500_EG53_FF47[3:]):
    _,time,temp_CH1, _ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])
    print(f'Temp minima = {temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} C ({temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]+273:.1f} K) alcanzada en {time[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} s')
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')
    ax2.plot(time,(np.gradient(temp_CH1,time)))

for a in (ax1,ax2):
    a.set_xlim(0,175)
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlim(60,350)
ax2.set_xlabel('t (s)')

# Gradiente
col=['C0','C1','C2']
fig33,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[:3],T[:3],dT[:3])):
    l1 = axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2 = axs[i].twinx()
    ax2.set_yscale('log')
    ax2.set_ylabel('T (K)')
    Tplot = y[Indx_min[i]:] + 273
    l2 = ax2.plot(x[Indx_min[i]:],Tplot,c=col[i],label='T')
    ax2.set_yticks([Tplot.min(),Tplot.max()])
    ax2.set_yticklabels([f'{Tplot.min():.0f}',f'{Tplot.max():.0f}'])
    ax2.minorticks_off()

    handles = l1 + l2
    labels = [h.get_label() for h in handles]

    axs[i].legend(handles, labels, frameon=True, shadow=True,title=f'H$_0$ = {H0[i]:.1f} kA/m',loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(t_min[:3])[0]-1,)
    a.grid()
    a.set_ylim(-1,2.5)
axs[2].set_xlabel('t (s)')
fig33.suptitle('3.3 - EG 53% FF 47% - LN2 --> RF - Idc = [150, 125, 100] dA')

fig34,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[3:],T[3:],dT[3:])):
    l1 = axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2 = axs[i].twinx()
    ax2.set_yscale('log')
    ax2.set_ylabel('T (K)')
    Tplot = y[Indx_min[i]:] + 273
    l2 = ax2.plot(x[Indx_min[i]:],Tplot,c=col[i],label='T')
    ax2.set_yticks([Tplot.min(),273])
    ax2.set_yticklabels([f'{Tplot.min():.0f}','273'])
    ax2.minorticks_off()
    ax2.set_ylim(98,273)

    handles = l1 + l2
    labels = [h.get_label() for h in handles]

    axs[i].legend(handles, labels, frameon=True, shadow=True,title=f'H$_0$ = {H0[i]:.1f} kA/m',loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(np.concatenate(t_min)[3:])-2,250)
    a.set_yticks([-1,-0.5,0,0.5,1,1.5,2,2.5])
    # a.set_yticklabels(['-1','-0.5','0','0.5','1','1.5','2','2.5'])    
    a.set_ylim(-1,2.5)
    
    a.grid()
axs[2].set_xlabel('t (s)')
fig34.suptitle('3.4 - EG 53% FF 47% - LN2 --> RF - Idc = [075, 050, 100] dA')

#salvo figuras
fig33.savefig('gradiente_temperatura_EG53FF47_150_125_100.png',dpi=300)
fig34.savefig('gradiente_temperatura_EG53FF47_075_050_000.png',dpi=300)
#%%4  
print('-'*50,'\nEG 51 FF 49 LN2 RF300- Idc= [150, 125, 100, 075, 050] dA','\n')
temps_500_EG51_FF49 = glob("4_EG51_FF49_LN2_to_RF_150_125_100_075_050/*.csv",recursive=True)
temps_500_EG51_FF49.sort()
for p in temps_500_EG51_FF49:
    print('  -',os.path.basename(p))
Idc_values = [15.0, 12.5, 10.0, 7.5, 5.0,0]
H0=[(h*pendiente_HvsI+ordenada_HvsI)/1000 for h in Idc_values]
t,t_min=[],[]
T,T_min=[],[]
Indx_min,dT=[],[]

fig4,(ax1,ax2) = plt.subplots(2,1,figsize=(9,9),constrained_layout=True)
ax1.set_title('4.1 - EG 51% FF 49% - LN2 --> RF - Idc = [150, 125, 100] dA',loc='left')
ax2.set_title('4.2 - EG 51% FF 49% - LN2 --> RF - Idc = [75, 50, 00] dA',loc='left')

for i,p in enumerate(temps_500_EG51_FF49[:3]):
    _,time,temp_CH1,_ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])
    print(f'Temp minima = {temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} C ({temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]+273:.1f} K) alcanzada en {time[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} s')
    ax1.plot(time,temp_CH1,label=f'{H0[i]:.1f} kA/m')
    ax1.plot(time,(np.gradient(temp_CH1,time)))

for i,p in enumerate(temps_500_EG51_FF49[3:]):
    _,time,temp_CH1,_ = lector_templog(p)
    t.append(time)
    T.append(temp_CH1)
    dT.append(np.gradient(temp_CH1,time))
    indx_min=np.nonzero(temp_CH1==min(temp_CH1))[0]
    t_min.append(time[indx_min])
    T_min.append(temp_CH1[indx_min])
    Indx_min.append(indx_min[0])
    print(f'Temp minima = {temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} C ({temp_CH1[np.nonzero(temp_CH1==min(temp_CH1))][0]+273:.1f} K) alcanzada en {time[np.nonzero(temp_CH1==min(temp_CH1))][0]:.1f} s')
    ax2.plot(time,temp_CH1,label=f'{H0[i+3]:.1f} kA/m' if i!=2 else '0 kA/m')
    ax2.plot(time,(np.gradient(temp_CH1,time)))

ax1.set_xlim(0,160)
ax2.set_xlim(0,350)

for a in (ax1,ax2):
    a.grid()
    a.legend(title='f = 300 kHz',loc='lower right',shadow=True,frameon=True)
    a.set_ylabel('T (°C)')
ax2.set_xlabel('t (s)')

#%% Gradiente
col=['C0','C1','C2']
fig43,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[:3],T[:3],dT[:3])):
    l1 = axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2 = axs[i].twinx()
    ax2.set_yscale('log')
    ax2.set_ylabel('T (K)')
    Tplot = y[Indx_min[i]:] + 273
    l2 = ax2.plot(x[Indx_min[i]:],Tplot,c=col[i],label='T')
    ax2.set_yticks([Tplot.min(),Tplot.max()])
    ax2.set_yticklabels([f'{Tplot.min():.0f}',f'{Tplot.max():.0f}'])
    ax2.minorticks_off()

    handles = l1 + l2
    labels = [h.get_label() for h in handles]

    axs[i].legend(handles, labels, frameon=True, shadow=True,title=f'H$_0$ = {H0[i]:.1f} kA/m',loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(t_min[:3])[0]-1,)
    a.grid()
    #a.set_ylim(-1,2.5)

axs[2].set_xlabel('t (s)')
fig43.suptitle('4.3 - EG 51% FF 49% - LN2 --> RF - Idc = [150, 125, 100] dA')

fig44,axs=plt.subplots(3,1,figsize=(10,5.5),constrained_layout=True,sharex=True)

for i,(x,y,z) in enumerate(zip(t[3:],T[3:],dT[3:])):
    l1 = axs[i].plot(x[Indx_min[i]:],z[Indx_min[i]:],'.-',c=col[i],label='dT/dt')
    ax2 = axs[i].twinx()
    ax2.set_yscale('log')
    ax2.set_ylabel('T (K)')
    Tplot = y[Indx_min[i]:] + 273
    l2 = ax2.plot(x[Indx_min[i]:],Tplot,c=col[i],label='T')
    ax2.set_yticks([Tplot.min(),273])
    ax2.set_yticklabels([f'{Tplot.min():.0f}','273'])
    ax2.minorticks_off()
    ax2.set_ylim(98,273)

    handles = l1 + l2
    labels = [h.get_label() for h in handles]

    axs[i].legend(handles, labels, frameon=True, shadow=True,title=f'H$_0$ = {H0[i]:.1f} kA/m',loc='lower right',ncol=2)

for a in axs:
    a.set_ylabel('dT/dt (°C/s)')
    a.set_xlim(min(np.concatenate(t_min)[3:-1]),250)
    a.set_yticks([-1,-0.5,0,0.5,1,1.5,2,2.5])
    #a.set_ylim(-1,2.5)
    a.grid()

axs[2].set_xlabel('t (s)')
fig44.suptitle('4.4 - EG 51% FF 49% - LN2 --> RF - Idc = [075, 050, 100] dA')

fig43.savefig('gradiente_temperatura_EG51FF49_150_125_100.png',dpi=300)
fig44.savefig('gradiente_temperatura_EG51FF49_075_050_000.png',dpi=300)
#%% Salvo figuras
figs=[fig1,fig2,fig3,fig4]
names=['EG55FF45_LN2_RF','EG55FF45_LN2_RF_Idc','EG53FF47_LN2_RF_Idc','EG51FF49_LN2_RF_Idc']
for i,fig in enumerate(figs):
    fig.savefig(f'{names[i]}.png',dpi=300)

#%% Veo derivadas

 