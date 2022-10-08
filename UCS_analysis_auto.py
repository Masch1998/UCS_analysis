#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 15:52:42 2022

@author: mariusschneider
"""

import numpy as np
import pandas as pd # Library for data table and statistics
import matplotlib.pyplot as plt # Library for plotting nice figures
import math
from scipy import stats
import os

folder='/Users/mariusschneider/Downloads/Results Uniaxial Compression Test (651-4125-00L 2022W)'
l=os.listdir(folder)

def README():
    print('This code allows you to analyse UCS data directly from the file folder')
    print('Workflow:')
    print('1. In the Excel file, add col l and d for length and diameter in mm for each file in the first row below the header.')    
    print('2. Enter the correct path to the files (folder var. in line 15)')
    print('3. Make sure that the file names, and change in file name are known.\nChange if necessary in line 35')
    print('\n')
    print('2 functions can be used for this analysis (overall, single_analysis)')
    print('\n')
    print('Overall:\nThis functions gives you the mean of UCS, UCS_50, (all) Youngs modulus and Poisson ratio.\nno further input needed and here is no return given from the function, but can be added.')
    print('You can enter the function by adding overall() to the console')
    print('\n')
    print('single_analysis: enter in console with single_analysis(folder,filename,plot=True). If plot is set to False, no plot will be drawn. ')
    print('Function has no return')
    
def maxi_MPa(df):
    ucs=np.max(df.MPa)# [MPa] = ([kN]/[mm^2])*1000
    ucs_c=np.max(df.MPa_cor) # [MPa] = ([kN]/[mm^2])*1000
    return ucs,ucs_c

def closest(lst, K):      
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def possion_ratio(df):
    l=closest(df.MPa,np.max(df.MPa)*0.3) # lower
    u=closest(df.MPa,np.max(df.MPa)*0.5) # upper    
    low=df.index[df.MPa==l][0]
    high=df.index[df.MPa==u][0]
    pr=(df.loc[low,'er']-df.loc[high,'er'])/(df.loc[high,'ea']-df.loc[low,'ea'])   
    return pr

def tangent_Y(df): #∆s/∆e_a
    # Defined for tangent at 50% of UCS 
    u=closest(df.MPa,np.max(df.MPa)*0.5)
    u=closest(df.MPa,np.max(df.MPa)*0.5)
    low=df.index[df.MPa==u][0]-1 # lower
    high=df.index[df.MPa==u][0]+1 # upper    
    E_t=(df.loc[low,'MPa']-df.loc[high,'MPa'])/(df.loc[low,'ea']-df.loc[high,'ea'])*1e-3
    return E_t,low,high


def av_Y(df): #∆s/∆e_a
    # Defined for tangent at 30% - 50% UCS   
    l=closest(df.MPa,np.max(df.MPa)*0.3) # lower
    u=closest(df.MPa,np.max(df.MPa)*0.5) # upper   
    low=df.index[df.MPa==l][0]
    high=df.index[df.MPa==u][0]    
    E_av=(df.loc[low,'MPa']-df.loc[high,'MPa'])/(df.loc[low,'ea']-df.loc[high,'ea'])*1e-3
    # print('E_av= ',round(E_av,1),'GPa')    
    return E_av,low,high

def s_Y(df): #∆s/∆e_a
    # Defined from original to peak (UCS)
    u=closest(df.MPa,np.max(df.MPa)) # upper    
    low=0
    high=df.index[df.MPa==u][0]    
    E_s=(df.loc[low,'MPa']-df.loc[high,'MPa'])/(df.loc[low,'ea']-df.loc[high,'ea'])*1e-3
    # print('E_s= ',round(E_s,1),'GPa')    
    return E_s,low,high
    
def overall(folder,l):

    all_UCS=[]
    all_UCS_50=[]
    all_E_T=[]
    all_E_av=[]
    all_E_s=[]
    all_v=[]

    x= '.DS_Store' in l 
    
    if x==True:
        i=l.index('.DS_Store')
        l.pop(i)

        
    
    
    
    for i in range(0,len(l)):
        file='{}/'+l[i]
        
        df=pd.read_excel(file.format(folder))  
        
        d=df.loc[0,'d']
        h=df.loc[0,'l']
        
        
        
        area=math.pi*(d**2)/4
        
        
        
        for i in range(0,len(df['Time(s)'])):
            df.loc[i,'MPa']=(df.loc[i,'Load(kN)']/area)*1000
            df.loc[i,'ea']=df.loc[i,'Long. strain(mm)']/h
            df.loc[i,'er']=-df.loc[i,'Transv. strain(mm)']/d
            df.loc[i,'MPa_cor']=df.MPa[i]/((50/d)**(0.18))
        
        UCS,UCS_c=maxi_MPa(df)
        v=possion_ratio(df)
        E_t,_,_=tangent_Y(df)
        E_av,_,_=av_Y(df)
        E_s,_,_=s_Y(df)
        
        all_UCS.append(UCS)
        all_UCS_50.append(UCS)
        all_E_T.append(E_t)
        all_E_av.append(E_av)
        all_E_s.append(E_s)
        all_v.append(v)
    
    
    m_UCS=round(np.mean(all_UCS),1)
    print('Mean UCS= ',m_UCS,'MPa')
    
    m_UCS_50=round(np.mean(all_UCS_50),1)
    print('Mean UCS (50mm)= ',m_UCS_50,'MPa')
    
    m_E_T=round(np.mean(all_E_T),1)
    print('Mean Tangent Youngs Modulus= ',m_E_T,'GPa')
    
    m_E_av=round(np.mean(all_E_av),1)
    print('Mean Average Youngs Modulus= ',m_E_av,'GPa')
    
    m_E_s=round(np.mean(all_E_s),1)
    print('Mean secant Youngs Modulus= ',m_E_s,'GPa')
    
    m_v=round(np.mean(all_v),3)
    print('Mean Poisson ratio= ',m_v)


def single_analysis(folder,filename='DS2',plot=True):
    filename=str(filename)
    plot=True
    file='{}/'+filename+'.xls'
    df=pd.read_excel(file.format(folder))
    
    d=df.loc[0,'d']
    h=df.loc[0,'l']
    
    
    
    area=math.pi*(d**2)/4
    
    
    
    for i in range(0,len(df['Time(s)'])):
        df.loc[i,'MPa']=(df.loc[i,'Load(kN)']/area)*1000
        df.loc[i,'ea']=df.loc[i,'Long. strain(mm)']/h
        df.loc[i,'er']=-df.loc[i,'Transv. strain(mm)']/d
        df.loc[i,'MPa_cor']=df.MPa[i]/((50/d)**(0.18))
    
    UCS,UCS_c=maxi_MPa(df)
    v=possion_ratio(df)
    E_t,low_t,high_t=tangent_Y(df)
    E_av,low_av,high_av=av_Y(df)
    E_s,low_s,high_s=s_Y(df)
    
    print('UCS= ',round(UCS,2),'MPa')
    
    print('UCS (50mm)= ',round(UCS_c,2),'MPa')
    
    print('Tangent Youngs Modulus= ',round(E_t,2),'GPa')
    
    print('Average Youngs Modulus= ',round(E_av,2),'GPa')
    
    print('Secant Youngs Modulus= ',round(E_s,2),'GPa')
    
    print('Poisson ratio= ',round(v,3))
    
    
    x_t=[df.loc[low_t,'ea'],df.loc[high_t,'ea']]
    y_t=[df.loc[low_t,'MPa'],df.loc[high_t,'MPa']]
    
    x_av=[df.loc[low_av,'ea'],df.loc[high_av,'ea']]
    y_av=[df.loc[low_av,'MPa'],df.loc[high_av,'MPa']]
    
    
    def regre(x,y,xuselim=10):
        res = stats.linregress(x, y)
        xuse=np.linspace(0,xuselim,2)
        y=res.intercept + res.slope*xuse
        return xuse, y
    
    
    for i in range(0,len(df['Time(s)'])):
        df.loc[i,'e_vol']=df.ea[i]+2*df.er[i]
        df.loc[i,'e_ev']=((1-2*v)/(E_av*1000)*df.MPa[i])
        df.loc[i,'e_cv']=df.e_vol[i]-df.e_ev[i]
    
    
    if plot==True:
        fig,ax=plt.subplots(1,3,figsize=(10,5))
        ax[0].plot(df['Time(s)'],df['MPa'])
        ax[0].hlines(np.max(df.MPa),0,df.loc[df.index[df.MPa==np.max(df.MPa)][0],'Time(s)'],
                     linestyle='--',
                     color='k',
                     linewidth=.75)
        ax[0].text(40,np.max(df.MPa)*1.01,'UCS='+str(round(np.max(df.MPa),2))+'MPa')
        ax[0].set_xlim(0,np.max(df['Time(s)'])*1.1)
        ax[0].set_ylim(0,np.max(df.MPa)*1.1)
        
        ax[1].plot(df['ea']*100,df['MPa'],color='k')
        ax[1].plot(df['er']*100,df['MPa'],color='k')
        ax[1].plot([df.loc[0,'ea']*100,df.loc[high_s,'ea']*100],[df.loc[0,'MPa'],df.loc[high_s,'MPa']],
                   linestyle='--',
                   color='r',
                   linewidth=.75,
                   label='$E_a$='+str(round(E_s,2))+'GPa')
        x,y=regre(x_t,y_t,np.max(df['ea']*0.75))
        ax[1].plot(x*100,y,color='darkgreen',
                  linewidth=.75,
                  linestyle='--',
                  label='$E_t$='+str(round(E_t,2))+'GPa')   
        x,y=regre(x_av,y_av,np.max(df['ea']*0.75))
        ax[1].plot(x*100,y,color='dodgerblue',
                  linewidth=.75,
                  linestyle='--',
                  label='$E_{av}$='+str(round(E_av,2))+'GPa')
        ax[1].legend(loc='upper center')
        ax[1].set_ylim(0,np.max(df['MPa']*1.2))
        
        
        ax[2].plot(df.e_vol*100,df.MPa)
        ax[2].plot(df.e_cv*100,df.MPa)
        ax[2].vlines(np.max(df.e_vol)*100,df.MPa[df.e_vol==np.max(df.e_vol)]*.75,df.MPa[df.e_vol==np.max(df.e_vol)]*1.25,
                     color='k',linestyle='--',linewidth=.5)
        ax[2].vlines(np.max(df.e_cv)*100,df.MPa[df.e_cv==np.max(df.e_cv)]*.25,df.MPa[df.e_cv==np.max(df.e_cv)]*1.25,
                     color='k',linestyle='--',linewidth=.5)
        
        s1=df.MPa[df.e_vol==np.max(df.e_vol)]
        s1=s1.iloc[0]
        s2=df.MPa[df.e_cv==np.max(df.e_cv)]
        s2=s2.iloc[0]
    
        
        ax[2].text(np.max(df.e_vol)*1.03*100,df.MPa[df.e_vol==np.max(df.e_vol)]*.75,'CI\n'+str(round(s1,2))+'MPa')
        ax[2].text(np.max(df.e_cv)*1.03*100,df.MPa[df.e_cv==np.max(df.e_cv)]*.25,'CD\n'+str(round(s2,2))+'MPa')
        ax[2].set_xlim(-.00001,np.max(df.e_vol)*150)
        
        
        ax[0].set_xlabel('Time[s]')
        ax[0].set_ylabel('Stress [MPa]') 
        ax[1].set_xlabel('Deformation [%]')
        ax[1].set_ylabel('Stress [MPa]') 
        ax[2].set_xlabel('Vol. strain [%]')
        ax[2].set_ylabel('Stress [MPa]')
        plt.tight_layout()
