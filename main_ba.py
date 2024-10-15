# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:38:02 2024

@author: lddelnido
"""
import numpy as np
import pandas as pd
import time
import math
from funciones_ba import * 
import plotly.graph_objects as go

f1 = datetime.datetime.today()
today = greg_to_mjd(f1) 

f = open('archivos/pred_bulla/xp_pred.txt','r') 

texto_xp = f.readlines()

f.close()
mjd,xp,yp,dy,lod,dut = read_iers()
try:
    epoch,xmass,ymass,zmass = read_aam()

    
    mjd2, xp2, yp2, dut1, xp_comp, yp_comp = get_data(today)
    dx_comp, dy_comp = comp(today)
    #if True:
    if int(texto_xp[-1][2:7]) != today:  
        ### INPUT DATA
        
        dx3, dy3, fechas_finals = finals_all(mjd[0],today)
        j2000 = [fechas_finals[i]-51544.5 for i in range(len(fechas_finals))]
        xfcn, yfcn,fechas = coord_fcn(dx3,dy3,j2000)
        
        mjd2, xp2, yp2, dut1 = reduc(mjd2, xp2, yp2, dut1, today)
    
        ind = mjd2.index(float(mjd[-1]))+1
        
        mjd = mjd+mjd2[ind:]
        ind2 = fechas_finals.index(mjd[0])
        ind3 = fechas_finals.index(mjd[-1])+1
        
        xp = xp+xp2[ind:]
        yp = yp+yp2[ind:]
        dut = dut+dut1[ind:]
        dx = dx3[ind2:ind3]
        dy = dy3[ind2:ind3]
        
        i = fechas.index(mjd[0])
        f = fechas.index(mjd[-1])+1
        
        xfcn = xfcn[i:f]
        yfcn = yfcn[i:f]
        
        xmass, ymass, zmass = equal(mjd,epoch,xmass, ymass, zmass)
        
    
        ### XPOL prediction
        
        a,b,c,d,e = pred_xp(xp,xmass,mjd)
        
        aux = int(mjd[-1])
        xpaux = [list(range(aux+1,aux+11)), a,b,c,d,e]
        xpaux = np.transpose(np.array(xpaux))
        xp_pred = pd.DataFrame(xpaux, columns = ['Epoch','KRR(xp, AAM xmass)','SSA 4PC + KRR','SSA 6PC + KRR','SSA 4PC + GPR','SSA 6PC + GPR'])
        
        lista = np.array(add_date(aux+1,f1,today))
        l2 = ['yy/mm/dd']
        fus = [str(lista[k,0])+'/'+str(lista[k,1])+'/'+str(lista[k,2]) for k in range(len(lista))]
        xp_pred.insert(loc = 0, column = l2[0], value = fus)
        
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR(xp, AAM xmass) [as], SSA 4PC + KRR [as], SSA 6PC + KRR [as], SSA 4PC + GPR [as], SSA 6PC + GPR [as]'
        np.savetxt('archivos/pred_bulla/xp_pred.txt', xp_pred, fmt = ['%s','%d','%f','%f','%1.5f','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today)+' mjd (last updated)')
        
        f = open('archivos/pred_bulla/xp_pred.txt','r')
        texto_xp = f.read()
        f.close()
        
        ### YPOL prediction
        b,c,d,e = pred_yp(yp,dy,ymass,mjd)
        
        aux = int(mjd[-1])
        ypaux = [list(range(aux+1,aux+11)),e,b,c,d]
        ypaux = np.transpose(np.array(ypaux))
        yp_pred = pd.DataFrame(ypaux, columns = ['Epoch', 'KRR (yp, AAM ymass)','SSA 2PC + KRR','SSA 4PC + KRR','SSA 6PC + KRR'])
    
        yp_pred.insert(loc = 0, column = l2[0], value = fus)
        
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR (yp, dy)[as], KRR (yp, AAM ymass)[as], SSA 2PC + KRR [as], SSA 4PC + KRR [as], SSA 6PC + KRR [as]'
        np.savetxt('archivos/pred_bulla/yp_pred.txt', yp_pred, fmt = ['%s','%d','%1.5f','%1.5f','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today)+' mjd (last updated)')
        
        g = open('archivos/pred_bulla/yp_pred.txt','r')
        texto_yp = g.read()
        g.close()
        
        
        ### dX prediction
        a,b = pred_dx(dx,xfcn,xp)
        
        aux = int(mjd[-1])
        dxaux = [list(range(aux+1,aux+11)),a,b]
        dxaux = np.transpose(np.array(dxaux))
        dx_pred = pd.DataFrame(dxaux,columns = ['Epoch','KRR (dx, xfcn)', 'KRR (dx, xfcn, xp)'])
        
        dx_pred.insert(loc = 0, column = l2[0], value = fus)
            
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR (dx, xfcn) [as], KRR (dx, xfcn, xp) [as]'
        np.savetxt('archivos/pred_bulla/dx_pred.txt', dx_pred, fmt = ['%s','%d','%1.5f','%1.5f'], delimiter='   ',header=h, footer = str(today)+' mjd (last updated)')
        
        g = open('archivos/pred_bulla/dx_pred.txt','r')
        texto_dx = g.read()
        g.close()
        
        ### dY prediction
        a,b = pred_dy(dy,yfcn,yp)
        
        aux = int(mjd[-1])
        dyaux = [list(range(aux+1,aux+11)),a,b]
        dyaux = np.transpose(np.array(dyaux))
        dy_pred = pd.DataFrame(dyaux,columns = ['Epoch','KRR (dy, yfcn)', 'KRR (dy, yfcn, yp)'])
        
        dy_pred.insert(loc = 0, column = l2[0], value = fus)
            
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR (dy, yfcn) [as], KRR (dy, yfcn, yp) [as]'
        np.savetxt('archivos/pred_bulla/dy_pred.txt', dy_pred, fmt = ['%s','%d','%1.5f','%1.5f'], delimiter='   ',header=h, footer = str(today)+' mjd (last updated)')
        
        g = open('archivos/pred_bulla/dy_pred.txt','r')
        texto_dy = g.read()
        g.close()
        
        # ### LOD prediction
        # a,b = pred_lod(lod,zmass,mjd)
        
        # for k in range(10):
        #     a[k] = a[k]*1e03
        #     b[k] = b[k]*1e03
    
        
        # aux = int(mjd[-1])
        # lodaux = [list(range(aux+1,aux+11)), a,b]
        # lodaux = np.transpose(np.array(lodaux))
        # lod_pred = pd.DataFrame(lodaux, columns = ['Epoch','KRR (LOD)', 'KRR (LOD, AAM zmass)'])
        # lod_pred = lod_pred.astype({'Epoch': int})
        
        # for j in range(3):
        #     lod_pred.insert(loc = j, column = l2[j], value = lista[:,j])
            
        # h = 'Columns: Date (y, m, d), Epoch [MJD], KRR (LOD) [ms], KRR (LOD, AAM zmass)[ms]'
        # np.savetxt('archivos/pred_bulla/lod_pred.txt', lod_pred, fmt = ['%d','%d','%d','%d','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today)+' mjd (last updated)')
        
        # g = open('archivos/pred_bulla/lod_pred.txt','r')
        # texto_lod = g.read()
        # g.close()
        
        ### UT1-UTC prediction
        # a,b,c = pred_dut1(dut,lod,zmass,mjd)
        
        # aux = int(mjd[-1])
        # dut1 = [list(range(aux,aux+10)), a,b,c]
        # dut1 = np.transpose(np.array(dut1))
        # dut1_pred = pd.DataFrame(dut1, columns = ['Epoch','KRR (UT1-UTC)','KRR (UT1-UTC, LOD)','KRR (UT1-UTC, LOD, zmass)'])
        # dut1_pred = dut1_pred.astype({'Epoch': int})
        
        # for j in range(3):
        #     dut1_pred.insert(loc = j, column = l2[j], value = lista[:,j])
            
        # h = 'Columns: Date (y, m, d), Epoch [MJD], KRR (UT1-UTC) [s]'#', KRR (UT1-UTC, LOD) [s], KRR (UT1-UTC, LOD, zmass) [s]'
        # np.savetxt('archivos/pred_bulla/dut1_pred.txt', dut1_pred, fmt = ['%d','%d','%d','%d','%1.5f','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today)+' mjd (last updated)')
        
        # g = open('archivos/pred_bulla/dut1_pred.txt','r')
        # texto_dut1 = g.read()
        # g.close()
        
    else:
        f = open('archivos/pred_bulla/xp_pred.txt','r')
        texto_xp = f.readlines()
        f.close()
        
        aux = [texto_xp[i].split() for i in range(1,len(texto_xp)-1)]   #last value is an empty line
        day = [aux[i][0] for i in range(len(aux))]
        epoch2 = [int(aux[i][1]) for i in range(len(aux))]
        a = [float(aux[i][2]) for i in range(len(aux))]
        b = [float(aux[i][3]) for i in range(len(aux))]
        c = [float(aux[i][4]) for i in range(len(aux))]
        d = [float(aux[i][5]) for i in range(len(aux))]
        e = [float(aux[i][6]) for i in range(len(aux))]
        
        xpaux = [day,epoch2, a,b,c,d,e]
        xpaux = np.transpose(np.array(xpaux, dtype = object))
        xp_pred = pd.DataFrame(xpaux, columns = ['Date (yy/mm/dd)','Epoch','KRR','SSA 4PC + KRR','SSA 6PC + KRR','SSA 4PC + GRR','SSA 6PC + GRR'])
    
        
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR(xp, AAM xmass) [as], SSA 4PC + KRR [as], SSA 6PC + KRR [as], SSA 4PC + GPR [as], SSA 6PC + GPR [as]'
        try:
            np.savetxt('archivos/pred_bulla/xp_pred.txt', xp_pred, fmt = ['%s','%d','%1.5f','%1.5f','%1.5f','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today))
        except TypeError as err:
            print(err.args)
        
        
        g = open('archivos/pred_bulla/yp_pred.txt','r')
        texto_yp = g.readlines()
        g.close()
        aux = [texto_yp[i].split() for i in range(1,len(texto_yp)-1)]   #last value is an empty line
        day = [aux[i][0] for i in range(len(aux))]
        epoch2 = [int(aux[i][1]) for i in range(len(aux))]
        a = [float(aux[i][2]) for i in range(len(aux))]
        b = [float(aux[i][3]) for i in range(len(aux))]
        c = [float(aux[i][4]) for i in range(len(aux))]
        d = [float(aux[i][5]) for i in range(len(aux))]
        #e = [float(aux[i][6]) for i in range(len(aux))]
        
        #yp = [day,epoch2, a,b,c,d,e]
        ypaux = [day,epoch2, a,b,c,d]
        ypaux = np.transpose(np.array(ypaux, dtype = object))
        yp_pred = pd.DataFrame(ypaux, columns = ['Date (yy/mm/dd)','Epoch', 'KRR (yp, AAM ymass)','SSA 2PC + KRR','SSA 4PC + KRR','SSA 6PC + KRR'])
        
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD],  KRR (yp, AAM ymass)[as], SSA 2PC + KRR [as], SSA 4PC + KRR [as], SSA 6PC + KRR [as]'
        np.savetxt('archivos/pred_bulla/yp_pred.txt', yp_pred, fmt = ['%s','%d','%1.5f','%1.5f','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today))
        g = open('archivos/pred_bulla/yp_pred.txt','r')
        texto_yp = g.read()
        g.close()
        
        g = open('archivos/pred_bulla/dx_pred.txt','r')
        texto_dx = g.readlines()
        g.close()
        aux = [texto_dx[i].split() for i in range(1,len(texto_dx)-1)]   #last value is an empty line
        d = [aux[i][0] for i in range(len(aux))]
        epoch2 = [int(aux[i][1]) for i in range(len(aux))]
        a = [float(aux[i][2]) for i in range(len(aux))]
        b = [float(aux[i][3]) for i in range(len(aux))]
        
        dxaux = [d,epoch2, a,b]
        dxaux = np.transpose(np.array(dxaux, dtype = object))
        dx_pred = pd.DataFrame(dxaux, columns = ['Date (yy/mm/dd)','Epoch','KRR (dx, xfcn)', 'KRR (dx, xfcn, xp)'])
    
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR (dx, xfcn)[as], KRR (dx, xfcn, xp)[as]'
        np.savetxt('archivos/pred_bulla/dx_pred.txt', dx_pred, fmt = ['%s','%d','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today))
        g = open('archivos/pred_bulla/dx_pred.txt','r')
        texto_dx = g.read()
        
    
        g = open('archivos/pred_bulla/dy_pred.txt','r')
        texto_dy = g.readlines()
        g.close()
        aux = [texto_dy[i].split() for i in range(1,len(texto_dy)-1)]   #last value is an empty line
        d = [aux[i][0] for i in range(len(aux))]
        epoch2 = [int(aux[i][1]) for i in range(len(aux))]
        a = [float(aux[i][2]) for i in range(len(aux))]
        b = [float(aux[i][3]) for i in range(len(aux))]
        
        dyaux = [d,epoch2, a,b]
        dyaux = np.transpose(np.array(dyaux, dtype = object))
        dy_pred = pd.DataFrame(dyaux, columns = ['Date (yy/mm/dd)','Epoch','KRR (dy, yfcn)', 'KRR (dy, yfcn, yp)'])
        
        h = 'Columns: Date (yy/mm/dd), Epoch [MJD], KRR (dy, yfcn)[as], KRR (dy, yfcn, yp)[as]'
        np.savetxt('archivos/pred_bulla/dx_pred.txt', dy_pred, fmt = ['%s','%d','%1.5f','%1.5f'], delimiter='   ', header=h, footer = str(today))
        g = open('archivos/pred_bulla/dy_pred.txt','r')
        texto_dy = g.read()
        
        # g = open('archivos/pred_bulla/lod_pred.txt','r')
        # texto_lod = g.readlines()
        # g.close()
        # aux = [texto_lod[i].split() for i in range(1,len(texto_lod)-1)]   #last value is an empty line
        # y = [float(aux[i][0]) for i in range(len(aux))]
        # m = [float(aux[i][1]) for i in range(len(aux))]
        # d = [float(aux[i][2]) for i in range(len(aux))]
        # epoch2 = [float(aux[i][3]) for i in range(len(aux))]
        # a = [float(aux[i][4]) for i in range(len(aux))]
        # b = [float(aux[i][5]) for i in range(len(aux))]
        
        # lodaux = [y,m,d,epoch2, a,b]
        # lodaux = np.transpose(np.array(lodaux))
        # lod_pred = pd.DataFrame(lodaux, columns = ['Year','Month','Day','Epoch','KRR (LOD)', 'KRR (LOD, AAM zmass)'])
        # lod_pred = lod_pred.astype({'Epoch': int})
        
        # h = 'Columns: Date (y, m, d), Epoch [MJD], KRR (LOD)[ms], KRR (LOD, AAM zmass)[ms]'
        # np.savetxt('archivos/pred_bulla/lod_pred.txt', lod_pred, fmt = ['%d','%d','%d','%d','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today))
        # g = open('archivos/pred_bulla/lod_pred.txt','r')
        # texto_lod = g.read()
        # g.close()
        
        # g = open('archivos/pred_bulla/dut1_pred.txt','r')
        # texto_dut1= g.readlines()
        # g.close()
        # aux = [texto_dut1[i].split() for i in range(1,len(texto_dut1)-1)]   #last value is an empty line
        # y = [float(aux[i][0]) for i in range(len(aux))]
        # m = [float(aux[i][1]) for i in range(len(aux))]
        # d = [float(aux[i][2]) for i in range(len(aux))]
        # epoch2 = [float(aux[i][3]) for i in range(len(aux))]
        # a = [float(aux[i][4]) for i in range(len(aux))]
        # b = [float(aux[i][5]) for i in range(len(aux))]
        # c = [float(aux[i][6]) for i in range(len(aux))]
        
        # dut1= [y,m,d,epoch2, a, b, c]
        # dut1 = np.transpose(np.array(dut1))
        # dut1_pred = pd.DataFrame(dut1, columns = ['Year','Month','Day','Epoch','KRR (UT1-UTC)','KRR (UT1-UTC, LOD)','KRR (UT1-UTC, LOD, zmass)'])
        # dut1_pred = dut1_pred.astype({'Epoch': int})
        
        # h = 'Columns: Date (y, m, d), Epoch [MJD], KRR (UT1-UTC) [s],KRR (UT1-UTC, LOD) [s],KRR (UT1-UTC, LOD, zmass) [s]'
        # np.savetxt('archivos/pred_bulla/dut1_pred.txt', dut1_pred, fmt = ['%d','%d','%d','%d','%1.5f','%1.5f','%1.5f'], delimiter='   ',header=h,footer = str(today))
        # g = open('archivos/pred_bulla/dut1_pred.txt','r')
        # texto_dut1= g.read()
        # g.close()
        
    ################ día 1 ##############
    f = open('archivos/predtotal2/xp_pred2.txt')
    texto_xp2 = f.read()
    f.close()
    
    f = open('archivos/predtotal2/yp_pred2.txt')
    texto_yp2 = f.read()
    f.close()
    
    f = open('archivos/predtotal2/dx_pred2.txt')
    texto_dx2 = f.read()
    f.close()
    
    f = open('archivos/predtotal2/dy_pred2.txt')
    texto_dy2 = f.read()
    f.close()
    
    f = open('archivos/predtotal2/lod_pred2.txt')
    texto_lod2 = f.read()
    f.close()
    
    f = open('archivos/predtotal2/dut1_pred2.txt')
    texto_dut12 = f.read()
    f.close()
    
    
    
    xp_pred['Bulletin A IERS'] = xp_comp
    fig_xp = go.Figure()
    for j in range(2,len(xp_pred.columns)):
       fig_xp.add_trace(go.Scatter(
           x = xp_pred['Epoch'],y = xp_pred[xp_pred.columns[j]],
           mode = 'lines+markers', name = xp_pred.columns[j]))
       
    fig_xp.update_layout(legend_title_text = "Models")
    fig_xp.update_xaxes(title_text="MJD", tickvals = xp_pred['Epoch'], ticktext =[str(a) for a in xp_pred['Epoch']]) 
    fig_xp.update_yaxes(title_text="as")
    
    yp_pred['Bulletin A IERS'] = yp_comp
    fig_yp = go.Figure()
    for j in range(2,len(yp_pred.columns)):
       fig_yp.add_trace(go.Scatter(
           x = yp_pred['Epoch'],y = yp_pred[yp_pred.columns[j]],
           mode = 'lines+markers', name = yp_pred.columns[j]))
       
    fig_yp.update_layout(legend_title_text = "Models")
    fig_yp.update_xaxes(title_text="MJD", tickvals = yp_pred['Epoch'], ticktext =[str(a) for a in yp_pred['Epoch']]) 
    fig_yp.update_yaxes(title_text="as")
    
    dx_pred['Finals.data IERS'] = dx_comp
    fig_dx = go.Figure()
    for j in range(2,len(dx_pred.columns)):
       fig_dx.add_trace(go.Scatter(
           x = dx_pred['Epoch'],y = dx_pred[dx_pred.columns[j]],
           mode = 'lines+markers', name = dx_pred.columns[j]))
       
    fig_dx.update_layout(legend_title_text = "Models")
    fig_dx.update_xaxes(title_text="MJD", tickvals = dx_pred['Epoch'], ticktext =[str(a) for a in dx_pred['Epoch']]) 
    fig_dx.update_yaxes(title_text="as")
    
    dy_pred['Finals.data IERS'] = dy_comp
    fig_dy = go.Figure()
    for j in range(2,len(dy_pred.columns)):
       fig_dy.add_trace(go.Scatter(
           x = dy_pred['Epoch'],y = dy_pred[dy_pred.columns[j]],
           mode = 'lines+markers', name = dy_pred.columns[j]))
       
    fig_dy.update_layout(legend_title_text = "Models")
    fig_dy.update_xaxes(title_text="MJD", tickvals = dy_pred['Epoch'], ticktext =[str(a) for a in dy_pred['Epoch']]) 
    fig_dy.update_yaxes(title_text="as")
    
    
    f = open('archivos/predtotal2/iers2.txt')
    texto_iers = f.readlines()
    f.close()
    aux = [texto_iers[i].split() for i in range(len(texto_iers))]
    taux = []
    for k in range(1,7):
        if k == 3 or k == 5 or k == 6:
            taux.append([float(aux[i][k])*1e03 for i in range(len(aux))])
        else:
            taux.append([float(aux[i][k]) for i in range(len(aux))])
            
            
    iers2 = pd.DataFrame(data = {'xp':taux[0], 'yp':taux[1], 'LOD':taux[2], 'dut1':taux[3], 'dx':taux[4], 'dy':taux[5]})
    
    
    f = open('archivos/predtotal2/xp_pred2.txt')
    texto_xp3 = f.readlines()
    f.close()
    aux = [texto_xp3[i].split() for i in range(1,len(texto_xp3))]
    t = []
    for k in range(9):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    xp_pred2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(xp, AAM xmass) ':t[4], 'SSA 4PC + KRR ':t[5], 'SSA 6PC + KRR ':t[6], 'SSA 4PC + GPR ':t[7], 'SSA 6PC + GPR ':t[8], 'IERS 14 C04':taux[0]})
    xp_err = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(xp, AAM xmass) [1] ':1e03*abs(np.array(t[4])-np.array(taux[0])), 'SSA 4PC + KRR [2] ':1e03*abs(np.array(t[5])-np.array(taux[0])), 'SSA 6PC + KRR [3]':1e03*abs(np.array(t[6])-np.array(taux[0])), 'SSA 4PC + GPR [4]':1e03*abs(np.array(t[7])-np.array(taux[0])), 'SSA 6PC + GPR [5]':1e03*abs(np.array(t[8])-np.array(taux[0]))}) 
    media = [np.round(np.mean(xp_err[xp_err.columns[j]]),3)  for j in range(4,9)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'MAE [mas]: [1]: {media[0]}, [2]: {media[1]}, [3]: {media[2]}, [4]: {media[3]}, [5]: {media[4]}',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    
    
    fig_xp2 = go.Figure()
    for j in range(4,len(xp_pred2.columns)):
       fig_xp2.add_trace(go.Scatter(
           x = xp_pred2['Epoch [MJD]'],y = xp_pred2[xp_pred2.columns[j]],
           mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75),name = xp_pred2.columns[j]))
       
    fig_xp2.update_layout(legend_title_text = "Models")
    fig_xp2.update_xaxes(title_text="MJD")
    fig_xp2.update_yaxes(title_text="as")
    
    fig_xp3 = go.Figure()
    for j in range(4,len(xp_err.columns)):
       fig_xp3.add_trace(go.Scatter(
           x = xp_err['Epoch [MJD]'],y = xp_err[xp_err.columns[j]],
           # mode = 'lines', line = dict(width = .5),name = xp_err.columns[j]))
           mode = 'markers', marker = dict(size = 2.5),name = xp_err.columns[j]))
       
    fig_xp3.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_xp3.update_xaxes(title_text="MJD")
    fig_xp3.update_yaxes(title_text="mas")
    fig_xp3.update_layout(annotations = annot)
    
    f = open('archivos/predtotal2/yp_pred2.txt')
    texto_yp3 = f.readlines()
    f.close()
    aux = [texto_yp3[i].split() for i in range(1,len(texto_yp3))]
    t = []
    for k in range(9):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    yp_pred2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (yp,dy) ':t[4], 'KRR (yp, AAM ymass)':t[5], 'SSA 2PC + KRR ':t[6], 'SSA 4PC + KRR ':t[7], 'SSA 6PC + KRR ':t[8], 'IERS 14 C04':taux[1]})
    yp_err = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (yp,dy) [1]':1e03*abs(np.array(t[4])-np.array(taux[1])), 'KRR (yp, AAM ymass) [2]':1e03*abs(np.array(t[5])-np.array(taux[1])), 'SSA 2PC + KRR [3]':1e03*abs(np.array(t[6])-np.array(taux[1])), 'SSA 4PC + KRR [4]':1e03*abs(np.array(t[7])-np.array(taux[1])), 'SSA 6PC + KRR [5]':1e03*abs(np.array(t[8])-np.array(taux[1]))})
    media = [np.round(np.mean(yp_err[yp_err.columns[j]]),3)  for j in range(4,9)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'MAE [mas]: [1]: {media[0]}, [2]: {media[1]}, [3]: {media[2]}, [4]: {media[3]}, [5]: {media[4]}',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    
    fig_yp2 = go.Figure()
    for j in range(4,len(yp_pred2.columns)):
       fig_yp2.add_trace(go.Scatter(
           x = yp_pred2['Epoch [MJD]'],y = yp_pred2[yp_pred2.columns[j]],
           mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75), name = yp_pred2.columns[j]))
       
    fig_yp2.update_layout(legend_title_text = "Models")
    fig_yp2.update_xaxes(title_text="MJD")
    fig_yp2.update_yaxes(title_text="as")
    
    fig_yp3 = go.Figure()
    for j in range(4,len(yp_err.columns)):
       fig_yp3.add_trace(go.Scatter(
           x = yp_err['Epoch [MJD]'],y = yp_err[yp_err.columns[j]],
           mode = 'markers', marker = dict(size = 2.5),name = yp_err.columns[j]))
       
    fig_yp3.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_yp3.update_xaxes(title_text="MJD")
    fig_yp3.update_yaxes(title_text="mas")
    fig_yp3.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal2/dx_pred2.txt')
    texto_dx3 = f.readlines()
    f.close()
    aux = [texto_dx3[i].split() for i in range(1,len(texto_dx3))]
    t = []
    for k in range(6):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
      
    lim = np.array(taux[4][:len(t[0])])
    dx_pred2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dx, xfcn) ':t[4], 'KRR(dx, xfcn, xp) ':t[5], 'IERS 14 C04':lim})
    dx_err = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dx, xfcn) ':abs(np.array(t[4])-lim), 'KRR(dx, xfcn, xp) ':abs(np.array(t[5])-lim)})
    media = [np.round(np.mean(dx_err[dx_err.columns[j]]),3)  for j in range(4,6)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'KRR(dx, xfcn) MAE {media[0]} mas,  KRR(dx, xfcn, xp) MAE {media[1]} mas',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    fig_dx2 = go.Figure()
    for j in range(4,len(dx_pred2.columns)):
       fig_dx2.add_trace(go.Scatter(
           x = dx_pred2['Epoch [MJD]'],y = dx_pred2[dx_pred2.columns[j]],
           mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75),name = dx_pred2.columns[j]))
       
    fig_dx2.update_layout(legend_title_text = "Models")
    fig_dx2.update_xaxes(title_text="MJD")
    fig_dx2.update_yaxes(title_text="mas")
    
    fig_dx3 = go.Figure()
    for j in range(4,len(dx_err.columns)):
       fig_dx3.add_trace(go.Scatter(
           x = dx_err['Epoch [MJD]'],y = dx_err[dx_err.columns[j]],
           mode = 'markers', marker = dict(size = 3),name = dx_err.columns[j]))
       
    fig_dx3.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_dx3.update_xaxes(title_text="MJD")
    fig_dx3.update_yaxes(title_text="mas")
    fig_dx3.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal2/dy_pred2.txt')
    texto_dy3 = f.readlines()
    f.close()
    aux = [texto_dy3[i].split() for i in range(1,len(texto_dy3))]
    t = []
    for k in range(6):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
    
    lim = np.array(taux[5][:len(t[0])])
            
    dy_pred2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dy, yfcn) ':t[4], 'KRR(dy, yfcn, yp) ':t[5], 'IERS 14 C04':lim })
    dy_err = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dy, yfcn)':abs(np.array(t[4])-lim), 'KRR(dy, yfcn, yp)':abs(np.array(t[5])-lim)})
    media = [np.round(np.mean(dy_err[dy_err.columns[j]]),3)  for j in range(4,6)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'KRR(dy, yfcn) MAE {media[0]} mas,  KRR(dy, yfcn, yp) MAE {media[1]} mas',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    fig_dy2 = go.Figure()
    for j in range(4,len(dy_pred2.columns)):
       fig_dy2.add_trace(go.Scatter(
           x = dy_pred2['Epoch [MJD]'],y = dy_pred2[dy_pred2.columns[j]],
           mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75),name = dy_pred2.columns[j]))
       
    fig_dy2.update_layout(legend_title_text = "Models")
    fig_dy2.update_xaxes(title_text="MJD")
    fig_dy2.update_yaxes(title_text="mas")
    
    
    fig_dy3 = go.Figure()
    for j in range(4,len(dy_err.columns)):
       fig_dy3.add_trace(go.Scatter(
           x = dy_err['Epoch [MJD]'],y = dy_err[dy_err.columns[j]],
           mode = 'markers', marker = dict(size = 3),name = dy_err.columns[j]))
       
    fig_dy3.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_dy3.update_xaxes(title_text="MJD")
    fig_dy3.update_yaxes(title_text="mas")
    fig_dy3.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal2/lod_pred2.txt')
    texto_lod3 = f.readlines()
    f.close()
    aux = [texto_lod3[i].split() for i in range(1,len(texto_lod3))]
    t = []
    for k in range(6):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    lod_pred2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (LOD) ':t[4], 'KRR (LOD, AAM zmass) ':t[5], 'IERS 14 C04':taux[2]})
    lod_err = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (LOD) ':abs(np.array(t[4])-np.array(taux[2])), 'KRR (LOD, AAM zmass) ':abs(np.array(t[5])-np.array(taux[2]))})
    media = [np.round(np.mean(lod_err[lod_err.columns[j]]),3) for j in range(4,6)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'KRR(LOD) MAE {media[0]} ms,  KRR(LOD, AAM zmass) MAE {media[1]} ms',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    
    
    
    fig_lod2 = go.Figure()
    for j in range(4,len(lod_pred2.columns)):
        fig_lod2.add_trace(go.Scatter(
            x = lod_pred2['Epoch [MJD]'],y = lod_pred2[lod_pred2.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2), line = dict(width = .75), name = lod_pred2.columns[j]))
       
    fig_lod2.update_layout(legend_title_text = "Models")
    fig_lod2.update_xaxes(title_text="MJD")
    fig_lod2.update_yaxes(title_text="ms")
    
    fig_lod3 = go.Figure()
    for j in range(4,len(lod_err.columns)):
        fig_lod3.add_trace(go.Scatter(
            x = lod_err['Epoch [MJD]'],y = lod_err[lod_err.columns[j]],
            mode = 'markers', marker = dict(size = 3),name = lod_err.columns[j]))
       
       
    fig_lod3.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_lod3.update_xaxes(title_text="MJD")
    fig_lod3.update_yaxes(title_text="ms")
    fig_lod3.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal2/dut1_pred2.txt')
    texto_dut13 = f.readlines()
    f.close()
    aux = [texto_dut13[i].split() for i in range(1,len(texto_dut13))]
    t = []
    for k in range(7):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    dut1_pred2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (UT1-UTC) ':t[4],'KRR (UT1-UTC, LOD) ':t[5],'KRR (UT1-UTC, LOD, AAM zmass) ':t[6], 'IERS 14 C04':taux[3]})
    dut1_err = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (UT1-UTC) [1] ':1e03*abs(np.array(t[4])-np.array(taux[3])),'KRR (UT1-UTC, LOD) [2] ':1e03*abs(np.array(t[5])-np.array(taux[3])),'KRR (UT1-UTC, LOD, AAM zmass) [3] ':1e03*abs(np.array(t[6])-np.array(taux[3]))})
    media = [np.round(np.mean(dut1_err[dut1_err.columns[j]]),3) for j in range(4,7)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.17,yref = 'paper',text = f'[1] MAE {media[0]} ms,  [2] MAE {media[1]} ms, [3] MAE {media[2]} ms',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
            
    
    
    fig_dut12 = go.Figure()
    for j in range(4,len(dut1_pred2.columns)):
        fig_dut12.add_trace(go.Scatter(
            x = dut1_pred2['Epoch [MJD]'],y = dut1_pred2[dut1_pred2.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75), name = dut1_pred2.columns[j]))
       
    fig_dut12.update_layout(legend_title_text = "Models")
    fig_dut12.update_xaxes(title_text="MJD")
    fig_dut12.update_yaxes(title_text="s")
    
    fig_dut13 = go.Figure()
    for j in range(4,len(dut1_err.columns)):
        fig_dut13.add_trace(go.Scatter(
            x = dut1_err['Epoch [MJD]'],y = dut1_err[dut1_err.columns[j]],
            mode = 'markers', marker = dict(size = 2.5),name = dut1_err.columns[j]))
       
       
    fig_dut13.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_dut13.update_xaxes(title_text="MJD")
    fig_dut13.update_yaxes(title_text="ms")
    fig_dut13.update_layout(annotations = annot)
    
    ######################### Day 10 #######################################
    f = open('archivos/predtotal10/xp_2pred2.txt')
    texto_xp4 = f.read()
    f.close()
    
    f = open('archivos/predtotal10/yp_2pred2.txt')
    texto_yp4 = f.read()
    f.close()
    
    f = open('archivos/predtotal10/dx_2pred2.txt')
    texto_dx4 = f.read()
    f.close()
    
    f = open('archivos/predtotal10/dy_2pred2.txt')
    texto_dy4 = f.read()
    f.close()
    
    f = open('archivos/predtotal10/lod_2pred2.txt')
    texto_lod4 = f.read()
    f.close()
    
    f = open('archivos/predtotal10/dut1_2pred2.txt')
    texto_dut14 = f.read()
    f.close()
    
    
    
    f = open('archivos/predtotal10/iers.txt')
    texto_iers = f.readlines()
    f.close()
    aux = [texto_iers[i].split() for i in range(len(texto_iers))]
    taux = []
    for k in range(1,7):
        if k == 3 or k == 5 or k == 6:
            taux.append([float(aux[i][k])*1e03 for i in range(len(aux))])
        else:
            taux.append([float(aux[i][k]) for i in range(len(aux))])
            
            
    iers2 = pd.DataFrame(data = {'xp':taux[0], 'yp':taux[1], 'LOD':taux[2], 'dut1':taux[3], 'dx':taux[4], 'dy':taux[5]})
    
    
    f = open('archivos/predtotal10/xp_2pred2.txt')
    texto_xp5 = f.readlines()
    f.close()
    aux = [texto_xp5[i].split() for i in range(1,len(texto_xp5))]
    t = []
    for k in range(9):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    xp_pred5 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(xp, AAM xmass) ':t[4], 'SSA 4PC + KRR ':t[5], 'SSA 6PC + KRR ':t[6], 'SSA 4PC + GPR ':t[7], 'SSA 6PC + GPR ':t[8], 'IERS 14 C04':taux[0]})
    xp_err2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(xp, AAM xmass) [1] ':1e03*abs(np.array(t[4])-np.array(taux[0])), 'SSA 4PC + KRR [2] ':1e03*abs(np.array(t[5])-np.array(taux[0])), 'SSA 6PC + KRR [3]':1e03*abs(np.array(t[6])-np.array(taux[0])), 'SSA 4PC + GPR [4]':1e03*abs(np.array(t[7])-np.array(taux[0])), 'SSA 6PC + GPR [5]':1e03*abs(np.array(t[8])-np.array(taux[0]))}) 
    media = [np.round(np.mean(xp_err2[xp_err2.columns[j]]),3)  for j in range(4,9)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'MAE [mas]: [1]: {media[0]}, [2]: {media[1]}, [3]: {media[2]}, [4]: {media[3]}, [5]: {media[4]}',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    
    
    fig_xp5 = go.Figure()
    for j in range(4,len(xp_pred5.columns)):
        fig_xp5.add_trace(go.Scatter(
            x = xp_pred5['Epoch [MJD]'],y = xp_pred5[xp_pred5.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75),name = xp_pred5.columns[j]))
       
    fig_xp5.update_layout(legend_title_text = "Models")
    fig_xp5.update_xaxes(title_text="MJD")
    fig_xp5.update_yaxes(title_text="as")
    
    fig_xp6 = go.Figure()
    for j in range(4,len(xp_err2.columns)):
        fig_xp6.add_trace(go.Scatter(
            x = xp_err2['Epoch [MJD]'],y = xp_err2[xp_err2.columns[j]],
            # mode = 'lines', line = dict(width = .5),name = xp_err2.columns[j]))
            mode = 'markers', marker = dict(size = 2.5),name = xp_err2.columns[j]))
       
    fig_xp6.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_xp6.update_xaxes(title_text="MJD")
    fig_xp6.update_yaxes(title_text="mas")
    fig_xp6.update_layout(annotations = annot)
    
    f = open('archivos/predtotal10/yp_2pred2.txt')
    texto_yp5 = f.readlines()
    f.close()
    aux = [texto_yp5[i].split() for i in range(1,len(texto_yp5))]
    t = []
    for k in range(9):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    yp_pred5 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (yp,dy) ':t[4], 'KRR (yp, AAM ymass)':t[5], 'SSA 2PC + KRR ':t[6], 'SSA 4PC + KRR ':t[7], 'SSA 6PC + KRR ':t[8], 'IERS 14 C04':taux[1]})
    yp_err2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (yp,dy) [1]':1e03*abs(np.array(t[4])-np.array(taux[1])), 'KRR (yp, AAM ymass) [2]':1e03*abs(np.array(t[5])-np.array(taux[1])), 'SSA 2PC + KRR [3]':1e03*abs(np.array(t[6])-np.array(taux[1])), 'SSA 4PC + KRR [4]':1e03*abs(np.array(t[7])-np.array(taux[1])), 'SSA 6PC + KRR [5]':1e03*abs(np.array(t[8])-np.array(taux[1]))})
    media = [np.round(np.mean(yp_err2[yp_err2.columns[j]]),3)  for j in range(4,9)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'MAE [mas]: [1]: {media[0]}, [2]: {media[1]}, [3]: {media[2]}, [4]: {media[3]}, [5]: {media[4]}',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    
    fig_yp5 = go.Figure()
    for j in range(4,len(yp_pred5.columns)):
        fig_yp5.add_trace(go.Scatter(
            x = yp_pred5['Epoch [MJD]'],y = yp_pred5[yp_pred5.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75), name = yp_pred5.columns[j]))
       
    fig_yp5.update_layout(legend_title_text = "Models")
    fig_yp5.update_xaxes(title_text="MJD")
    fig_yp5.update_yaxes(title_text="as")
    
    fig_yp6 = go.Figure()
    for j in range(4,len(yp_err2.columns)):
        fig_yp6.add_trace(go.Scatter(
            x = yp_err2['Epoch [MJD]'],y = yp_err2[yp_err2.columns[j]],
            mode = 'markers', marker = dict(size = 2.5),name = yp_err2.columns[j]))
       
    fig_yp6.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_yp6.update_xaxes(title_text="MJD")
    fig_yp6.update_yaxes(title_text="mas")
    fig_yp6.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal10/dx_2pred2.txt')
    texto_dx5 = f.readlines()
    f.close()
    aux = [texto_dx5[i].split() for i in range(1,len(texto_dx5))]
    t = []
    for k in range(6):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
      
    lim = np.array(taux[4][:len(t[0])])
    dx_pred5 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dx, xfcn) ':t[4], 'KRR(dx, xfcn, xp) ':t[5], 'IERS 14 C04':lim})
    dx_err2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dx, xfcn) ':abs(np.array(t[4])-lim), 'KRR(dx, xfcn, xp) ':abs(np.array(t[5])-lim)})
    media = [np.round(np.mean(dx_err2[dx_err2.columns[j]]),3)  for j in range(4,6)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'KRR(dx, xfcn) MAE {media[0]} mas,  KRR(dx, xfcn, xp) MAE {media[1]} mas',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    fig_dx5 = go.Figure()
    for j in range(4,len(dx_pred5.columns)):
        fig_dx5.add_trace(go.Scatter(
            x = dx_pred5['Epoch [MJD]'],y = dx_pred5[dx_pred5.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75),name = dx_pred5.columns[j]))
       
    fig_dx5.update_layout(legend_title_text = "Models")
    fig_dx5.update_xaxes(title_text="MJD")
    fig_dx5.update_yaxes(title_text="mas")
    
    fig_dx6 = go.Figure()
    for j in range(4,len(dx_err2.columns)):
        fig_dx6.add_trace(go.Scatter(
            x = dx_err2['Epoch [MJD]'],y = dx_err2[dx_err2.columns[j]],
            mode = 'markers', marker = dict(size = 3),name = dx_err2.columns[j]))
       
    fig_dx6.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_dx6.update_xaxes(title_text="MJD")
    fig_dx6.update_yaxes(title_text="mas")
    fig_dx6.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal10/dy_2pred2.txt')
    texto_dy5 = f.readlines()
    f.close()
    aux = [texto_dy5[i].split() for i in range(1,len(texto_dy5))]
    t = []
    for k in range(6):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
    
    lim = np.array(taux[5][:len(t[0])])
            
    dy_pred5 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dy, yfcn) ':t[4], 'KRR(dy, yfcn, yp) ':t[5], 'IERS 14 C04':lim })
    dy_err2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR(dy, yfcn)':abs(np.array(t[4])-lim), 'KRR(dy, yfcn, yp)':abs(np.array(t[5])-lim)})
    media = [np.round(np.mean(dy_err2[dy_err2.columns[j]]),3)  for j in range(4,6)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'KRR(dy, yfcn) MAE {media[0]} mas,  KRR(dy, yfcn, yp) MAE {media[1]} mas',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    fig_dy5 = go.Figure()
    for j in range(4,len(dy_pred5.columns)):
        fig_dy5.add_trace(go.Scatter(
            x = dy_pred5['Epoch [MJD]'],y = dy_pred5[dy_pred5.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75),name = dy_pred5.columns[j]))
       
    fig_dy5.update_layout(legend_title_text = "Models")
    fig_dy5.update_xaxes(title_text="MJD")
    fig_dy5.update_yaxes(title_text="mas")
    
    
    fig_dy6 = go.Figure()
    for j in range(4,len(dy_err2.columns)):
        fig_dy6.add_trace(go.Scatter(
            x = dy_err2['Epoch [MJD]'],y = dy_err2[dy_err2.columns[j]],
            mode = 'markers', marker = dict(size = 3),name = dy_err2.columns[j]))
       
    fig_dy6.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_dy6.update_xaxes(title_text="MJD")
    fig_dy6.update_yaxes(title_text="mas")
    fig_dy6.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal10/lod_2pred2.txt')
    texto_lod5 = f.readlines()
    f.close()
    aux = [texto_lod5[i].split() for i in range(1,len(texto_lod5))]
    t = []
    for k in range(6):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    lod_pred5 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (LOD) ':t[4], 'KRR (LOD, AAM zmass) ':t[5], 'IERS 14 C04':taux[2]})
    lod_err2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (LOD) ':abs(np.array(t[4])-np.array(taux[2])), 'KRR (LOD, AAM zmass) ':abs(np.array(t[5])-np.array(taux[2]))})
    media = [np.round(np.mean(lod_err2[lod_err2.columns[j]]),3) for j in range(4,6)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.2,yref = 'paper',text = f'KRR(LOD) MAE {media[0]} ms,  KRR(LOD, AAM zmass) MAE {media[1]} ms',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
    
    
    
    
    fig_lod5 = go.Figure()
    for j in range(4,len(lod_pred5.columns)):
        fig_lod5.add_trace(go.Scatter(
            x = lod_pred5['Epoch [MJD]'],y = lod_pred5[lod_pred5.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2), line = dict(width = .75), name = lod_pred5.columns[j]))
       
    fig_lod5.update_layout(legend_title_text = "Models")
    fig_lod5.update_xaxes(title_text="MJD")
    fig_lod5.update_yaxes(title_text="ms")
    
    fig_lod6 = go.Figure()
    for j in range(4,len(lod_err2.columns)):
        fig_lod6.add_trace(go.Scatter(
            x = lod_err2['Epoch [MJD]'],y = lod_err2[lod_err2.columns[j]],
            mode = 'markers', marker = dict(size = 3),name = lod_err2.columns[j]))
       
       
    fig_lod6.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_lod6.update_xaxes(title_text="MJD")
    fig_lod6.update_yaxes(title_text="ms")
    fig_lod6.update_layout(annotations = annot)
    
    
    f = open('archivos/predtotal10/dut1_2pred2.txt')
    texto_dut15 = f.readlines()
    f.close()
    aux = [texto_dut15[i].split() for i in range(1,len(texto_dut15))]
    t = []
    for k in range(7):
        if k<4:
            t.append([int(aux[i][k]) for i in range(len(aux))])
        else:
            t.append([float(aux[i][k]) for i in range(len(aux))])
            
    dut1_pred5 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (UT1-UTC) ':t[4],'KRR (UT1-UTC, LOD) ':t[5],'KRR (UT1-UTC, LOD, AAM zmass) ':t[6], 'IERS 14 C04':taux[3]})
    dut1_err2 = pd.DataFrame(data = {'y':t[0], 'm':t[1],'d':t[2], 'Epoch [MJD]':t[3], 'KRR (UT1-UTC) [1] ':1e03*abs(np.array(t[4])-np.array(taux[3])),'KRR (UT1-UTC, LOD) [2] ':1e03*abs(np.array(t[5])-np.array(taux[3])),'KRR (UT1-UTC, LOD, AAM zmass) [3] ':1e03*abs(np.array(t[6])-np.array(taux[3]))})
    media = [np.round(np.mean(dut1_err2[dut1_err2.columns[j]]),3) for j in range(4,7)]
    pmedio = (t[3][-1]-t[3][0])//2
    annot = [dict(x = t[3][pmedio],y = -.17,yref = 'paper',text = f'[1] MAE {media[0]} ms,  [2] MAE {media[1]} ms, [3] MAE {media[2]} ms',xanchor='center', yanchor='top',showarrow = False, font = dict(color = 'black'))]
            
    
    
    fig_dut15 = go.Figure()
    for j in range(4,len(dut1_pred5.columns)):
        fig_dut15.add_trace(go.Scatter(
            x = dut1_pred5['Epoch [MJD]'],y = dut1_pred5[dut1_pred5.columns[j]],
            mode = 'lines+markers', marker = dict(size = 2.5), line = dict(width = .75), name = dut1_pred5.columns[j]))
       
    fig_dut15.update_layout(legend_title_text = "Models")
    fig_dut15.update_xaxes(title_text="MJD")
    fig_dut15.update_yaxes(title_text="s")
    
    fig_dut16 = go.Figure()
    for j in range(4,len(dut1_err2.columns)):
        fig_dut16.add_trace(go.Scatter(
            x = dut1_err2['Epoch [MJD]'],y = dut1_err2[dut1_err2.columns[j]],
            mode = 'markers', marker = dict(size = 2.5),name = dut1_err2.columns[j]))
       
       
    fig_dut16.update_layout(legend_title_text = "AE of IERS 14 C04 & Models")
    fig_dut16.update_xaxes(title_text="MJD")
    fig_dut16.update_yaxes(title_text="ms")
    fig_dut16.update_layout(annotations = annot)
except:
    print("Data is being updated. This process might take a few minutes")
    
