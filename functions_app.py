# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 10:33:18 2025

@author: lddelnido
"""
import streamlit as st
import numpy as np
import pandas as pd
import time
import datetime
from astropy.time import Time
import sqlite3
import requests
import plotly.graph_objects as go


def read_db(num):
    table = ['polls_files','polls_files_new','polls_fcn_cpo']
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * from {table[num]} """)
    dff=pd.read_sql(f"""SELECT * from {table[num]} """, conn)  #DataFrame with all the prediction data from the database
    conn.close()
    return dff


def separate_dates(df):
    dates = df['pub_date'].values
    year = [s[:4] for s in dates]
    month = [m[5:7] for m in dates]
    day = [d[8:10] for d in dates]
    
    df.insert(0, column = 'year', value = year)
    df.insert(1, column = 'month', value = month)
    df.insert(2, column = 'day', value = day)
    return df

def create_df(val,df5,df_mjd):
    #Reading the data of the chosen prediction epoch
    conv1 = (df5[df5['type_EAM'] == 0])["values"].iloc[0]
    conv2 = (df5[df5['type_EAM'] == 1])["values"].iloc[0]
    conv_dates = ((df5[df5['type_EAM'] == 0])["pub_date"].values)[0]
    epochs = (df_mjd[df_mjd["pub_date"] == conv_dates])["values"].iloc[0]
    epochs = [int(float(item)) for item in epochs.split(',')] 
    conv1 =  [float(item) for item in conv1.split(',')] 
    conv2 =  [float(item) for item in conv2.split(',')]  
    dates_fmt = [(Time(item,format = 'mjd').to_value('datetime')).strftime("%Y-%m-%d %H:%M:%S") for item in epochs]
    if val in 'dt':
         txt = 's'
         fm = '% .9f'
    if val in {'dx','dy'}:
         txt = 'mas'
         fm = '% 5f'
    if val in {'xp','yp'}:
         txt = 'as'
         fm = '% .8f'
         
    df_final = pd.DataFrame({'Date [YY-MM-DD]':dates_fmt,'Epoch [MJD]':epochs, f'w/o EAM [{txt}]':conv1, f'w/ EAM [{txt}]':conv2}, index = (['Day'+str(v) for v in range(11)]))     
    return df_final, txt, fm

def create_download(df,selected,txt,fm,t):
    l = len(txt)
    if l<3:
        txt = txt+']'+(' '*(2-l))
    else:
        txt = txt+']'
    if t:
        np.savetxt('param.txt',df, fmt = ['% s','%5d',f'{fm}',f'{fm}',f'{fm}',f'{fm}'], delimiter='   \t', header = f'   Date [YY-MM-DD]  |  Epoch[MJD]  | w/o EAM [{txt}  | w/EAM  [{txt} |NEW w/o EAM [{txt}| NEW w/EAM  [{txt}')
    else:
        np.savetxt('param.txt',df, fmt = ['% s','%5d',f'{fm}',f'{fm}'], delimiter='   \t', header = f'  Date [YY-MM-DD]  |  Epoch[MJD]  |  w/o EAM [{txt}  |    w/EAM  [{txt}')
    f = open('param.txt','r') 
    lista =f.read()
    f.close()

    if selected == 'UT1-UTC':
         string = 'dut1'
    else:
         string = selected
         
    return string, lista


def history1(dff):
    df_aux_no = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','xp','yp','dt','dx','dy'])
    df_no = dff[dff['type_EAM'] == 0].sort_values('pub_date')

    df_aux_si = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','xp','yp','dt','dx','dy'])
    df_si = dff[dff['type_EAM'] == 1].sort_values('pub_date')
    
    for item in ['mj','xp','yp','dx','dy','dt']:
        d1 = df_no[df_no['param']==item]
        d2 = df_si[df_si['param']==item]
        
        df_aux_no[item] = d1['values'].values
        df_aux_si[item] = d2['values'].values
    
         
    #Change df format for a row per day:
    df_no_hist = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','xp','yp','dt','dx','dy'])
    df_si_hist = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','xp','yp','dt','dx','dy'])
    
    for i in range(len(df_aux_no)):
        sample_no = df_aux_no.iloc[i]
        aux_no = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','xp','yp','dt','dx','dy'])
        sample_si = df_aux_si.iloc[i]
        aux_si = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','xp','yp','dt','dx','dy'])
        for it in ['mj','xp','yp','dt','dx','dy']:
            aux_no[it] = list(map(float,sample_no[it].split(',')))
            aux_si[it] = list(map(float,sample_si[it].split(',')))
            # df_no_hist = pd.concat([df_no_hist,[np.nan]*7])
        df_no_hist = pd.concat([df_no_hist,aux_no])
        df_si_hist = pd.concat([df_si_hist,aux_si])
        
    df_no_hist.dop = df_no_hist.index
    df_si_hist.dop = df_si_hist.index
    
    dates_hist_fmt = [(Time(item,format = 'mjd').to_value('datetime')).strftime("%Y-%m-%d %H:%M:%S") for item in df_no_hist['mj'].values]
    df_no_hist.pub_date = dates_hist_fmt
    df_si_hist.pub_date = dates_hist_fmt
    
    ls = {'pub_date':'Date [YY-MM-DD]','mj':'Epoch[MJD]','dop':'Prediction day','xp':'xpol[as]','yp':'ypol[as]','dt':'dUT1[s]','dx':'dX[mas]','dy':'dY[mas]'}
    df_no_hist = df_no_hist.rename(ls, axis = 1)
    df_si_hist = df_si_hist.rename(ls, axis = 1)
  
    return df_no_hist, df_si_hist
        

def history2(dff):
    df_aux_no = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','dx','dy'])
    df_no = dff[dff['type_EAM'] == 0].sort_values('pub_date')

    df_aux_si = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','dx','dy'])
    df_si = dff[dff['type_EAM'] == 1].sort_values('pub_date')
    
    for item in ['mj','dx','dy']:
        d1 = df_no[df_no['param']==item]
        d2 = df_si[df_si['param']==item]
        
        df_aux_no[item] = d1['values'].values
        df_aux_si[item] = d2['values'].values
    
         
    #Change df format for a row per day:
    df_no_hist = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','dx','dy'])
    df_si_hist = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','dx','dy'])
    
    for i in range(len(df_aux_no)):
        sample_no = df_aux_no.iloc[i]
        aux_no = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','dx','dy'])
        sample_si = df_aux_si.iloc[i]
        aux_si = pd.DataFrame(data = [], columns = ['pub_date','mj','dop','dx','dy'])
        for it in ['mj','dx','dy']:
            aux_no[it] = list(map(float,sample_no[it].split(',')))
            aux_si[it] = list(map(float,sample_si[it].split(',')))
            # df_no_hist = pd.concat([df_no_hist,[np.nan]*7])
        df_no_hist = pd.concat([df_no_hist,aux_no])
        df_si_hist = pd.concat([df_si_hist,aux_si])
        
    df_no_hist.dop = df_no_hist.index
    df_si_hist.dop = df_si_hist.index
    
    dates_hist_fmt = [(Time(item,format = 'mjd').to_value('datetime')).strftime("%Y-%m-%d %H:%M:%S") for item in df_no_hist['mj'].values]
    df_no_hist.pub_date = dates_hist_fmt
    df_si_hist.pub_date = dates_hist_fmt
    
    ls = {'pub_date':'Date [YY-MM-DD]','mj':'Epoch[MJD]','dop':'Prediction day','dx':'dX_new[mas]','dy':'dY_new[mas]'}
    df_no_hist = df_no_hist.rename(ls, axis = 1)
    df_si_hist = df_si_hist.rename(ls, axis = 1)
    
    return df_no_hist, df_si_hist

def history(dff,dff2):
    df_no_hist, df_si_hist = history1(dff)
    a1,a2 = history2(dff2)
    
    dd = len(df_no_hist)-len(a1)
    aux = np.concatenate((np.array([' nan  ']*dd),np.array([f'{x: .5f}' for x in a1['dX_new[mas]'].values])))
    aux2 = np.concatenate((np.array([' nan  ']*dd),np.array([f'{x: .5f}' for x in a1['dY_new[mas]'].values])))
    df_no_hist.insert(8,'dX_new[mas]',aux)
    df_no_hist.insert(9,'dY_new[mas]',aux2)
    
    dd = len(df_si_hist)-len(a2)
    aux = np.concatenate((np.array([' nan  ']*dd),np.array([f'{x: .5f}' for x in a2['dX_new[mas]'].values])))
    aux2 = np.concatenate((np.array([' nan  ']*dd),np.array([f'{x: .5f}' for x in a2['dY_new[mas]'].values])))
    df_si_hist.insert(8,'dX_new[mas]',aux)
    df_si_hist.insert(9,'dY_new[mas]',aux2)
    
    return df_no_hist, df_si_hist
    

def df_filtered(dff_aux,df,val, years, months, days):
    dff2 = dff_aux[dff_aux['param'] == val]
    dff_mjd= dff_aux[dff_aux['param'] == 'mj']
    
    if (years in dff2['year'].values and months in dff2['month'].values and days in dff2['day'].values):
        dff3 = dff2[dff2['year']==years]
        dff4 = dff3[dff3['month']==months]
        dff5 = dff4[dff4['day']==days]
        
        df_new, txt_new, fm_new = create_df(val, dff5, dff_mjd)
        
        df = pd.concat([df,df_new[df_new.columns[-2:]]],axis = 1, ignore_index = False)
        df.columns = pd.Index(['Date [YY-MM-DD]', 'Epoch [MJD]', 'w/o EAM [mas]', 'w/ EAM [mas]','NEW w/o EAM [mas]', 'NEW w/ EAM [mas]'], dtype='object')
        t = True
    return df, t


def fcn_cpo(dff):
    df = pd.DataFrame(data = [], columns = ['dt','mj','ac','as','x0','y0','dx','dy'])
    for i in range(len(dff)):
        aa = dff.iloc[i]
        val = [float(x) for x in aa['values'].split(',')]
        df[aa.param] = val
        
        if aa.param == 'mj':
            inter = [(Time(x, format = 'mjd').to_value('datetime')).strftime("%Y-%m-%d %H:%M:%S") for x in val]
            df.dt = inter
    df = df.rename({'dt':'Date [YY-MM-DD]','mj':'Epoch [MJD]','ac':'Ac [muas]','as':'As [muas]','x0':'X0 [muas]','y0':'Y0 [muas]','dx':'dX [muas]','dy':'dY [muas]'},axis = 1) 
    fm = ['% s','%5d','% .4f','% .4f','% .4f','% .4f','% .4f','% .4f']    
    return df, fm
        
 
def read_iers():
    r = requests.get("https://datacenter.iers.org/data/latestVersion/EOP_20u23_C04_one_file_1962-now.txt")
    datos = r.text
    cont,j = 0,0
    while cont<6:
        if datos[j] =='\n':
            cont+=1
        j+=1
    datos=datos[j:]
    lista = datos.split("\n")
    aux = [lista[i].split() for i in range(len(lista)-1)]   #last value is an empty line
    dx = [1e6*float(aux[i][8]) for i in range(len(aux))]
    dy = [1e6*float(aux[i][9]) for i in range(len(aux))]
    
    return dx,dy


def interval_dates(df_fcn):
    inicio = df_fcn['Date [YY-MM-DD]'].values[-365*10]
    fin = df_fcn['Date [YY-MM-DD]'].values[-1]
    inicio = datetime.datetime.strptime(inicio, '%Y-%m-%d %H:%M:%S')
    fin = datetime.datetime.strptime(fin, '%Y-%m-%d %H:%M:%S')
    return inicio, fin


def fig_eops(df,txt,selected,lim):
    fig = go.Figure()
    for j in range(1,lim):
         fig.add_trace(go.Scatter(x = df['Epoch [MJD]'],y = df[df.columns[-j]],mode = 'lines+markers', marker = dict(size = 5), line = dict(width = 1.5),name = df.columns[-j]))
     
    fig.update_layout(title = f'{selected}',
                      title_font_color = '#fb9a5a',
                      title_font_size = 28,
                      title_font_weight = 20,
                      title_x = .5
                        )
    fig.update_layout(legend_title_text = 'Models',
                      legend_bordercolor = '#fb9a5a',
                      legend_borderwidth = 1.5,
                      legend_font_size = 14,
                      legend_title_font_size = 18
                      )
    fig.update_layout(plot_bgcolor = '#fff')
    fig.update_xaxes(title_text="Date",
                     tickfont_size = 14,
                     ticks = 'outside',
                     minor_ticks = 'outside',
                     minor_dtick = 1,
                     tickcolor = '#d1d1d1',
                     )
    
    fig.update_yaxes(title_text=f"[{txt}]",
                     tickfont_size = 14,
                     ticks = 'outside',
                     tickcolor = '#d1d1d1',
                     minor_ticks = 'outside',
                     gridcolor = '#d1d1d1',
                     minor_showgrid = True,
                     minor_griddash = 'dot'
                     )
    return fig


def fig_fcn(intervalo, df_fcn, dx_c04, dy_c04):
    a, b = intervalo[0].strftime('%Y-%m-%d %H:%M:%S'), intervalo[1].strftime('%Y-%m-%d %H:%M:%S')
    i = (df_fcn[df_fcn['Date [YY-MM-DD]'] == a].index)[0]
    f = (df_fcn[df_fcn['Date [YY-MM-DD]'] == b].index)[0]
    
    if f> len(df_fcn):
        xval = len(df_fcn)
    else: 
        xval = f
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df_fcn['Date [YY-MM-DD]'][i:xval], y = dx_c04[i:xval], mode = 'lines+markers',marker = dict(size = 2.5), line = dict(width = 1,dash = 'dot'),name = 'dX IERS 20u23 C04'))
    fig.add_trace(go.Scatter(x = df_fcn['Date [YY-MM-DD]'][i:xval], y = dy_c04[i:xval], mode = 'lines+markers',marker = dict(size = 2.5), line = dict(width = 1,dash = 'dot'),name = 'dY IERS 20u23 C04'))
    fig.add_trace(go.Scatter(x = df_fcn['Date [YY-MM-DD]'][i:f], y = df_fcn[df_fcn.columns[6]][i:f], mode = 'lines+markers',marker = dict(size = 3), line = dict(width = 1.2),name = 'FCN - dX'))
    fig.add_trace(go.Scatter(x = df_fcn['Date [YY-MM-DD]'][i:f], y = df_fcn[df_fcn.columns[7]][i:f], mode = 'lines+markers',marker = dict(size = 3), line = dict(width = 1.2),name = 'FCN - dY'))
    fig.update_layout(title = 'FCN-CPOs solutions',
                      title_font_color = '#fb9a5a',
                      title_font_size = 28,
                      title_font_weight = 20,
                      title_x = .5
                        )
    fig.update_layout(legend_title_text = 'Parameters',
                      legend_bordercolor = '#fb9a5a',
                      legend_borderwidth = 1.5,
                      legend_font_size = 14,
                      legend_title_font_size = 18
                      )
    fig.update_layout(plot_bgcolor = '#fff')
    fig.update_xaxes(title_text="Date",
                      tickfont_size = 14,
                      ticks = 'outside',
                      minor_ticks = 'outside',

                      tickcolor = '#d1d1d1',
                      )
    
    fig.update_yaxes(title_text="muas",
                      tickfont_size = 14,
                      ticks = 'outside',
                      tickcolor = '#d1d1d1',
                      minor_ticks = 'outside',
                      gridcolor = '#d1d1d1',
                      minor_showgrid = True,
                      minor_griddash = 'dot'
                      )
    return fig