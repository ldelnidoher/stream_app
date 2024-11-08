# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 09:57:47 2024

@author: lddelnido
"""

import numpy as np
import pandas as pd
import time
import math
import requests
import matplotlib.pyplot as plt
from joblib import load
from sklearn.decomposition import PCA
from scipy.interpolate import PchipInterpolator
import datetime
import numpy.linalg  as la
import copy
import os

frecFCN = -(2*math.pi)/430.0027   #Free Core Nutation frecquency

def links():
    """
    Returns
    -------
    urls : list of strings
           link to the last 6 versions of IERS Bulletin A .txt file
    """
    r = requests.get('https://datacenter.iers.org/availableVersions.php?id=6')
    x = r.text
    urls = []
    i = 0
    while i<6:
        ini, fin = x.index('bulletina'),x.index('txt')+3
        if fin-ini<50:
            if (urls!= [] and x[fin-7:fin-4]!=urls[-1][-7:-4]) or (urls == []):
                if x[fin-3:fin] == 'txt' and (fin-ini<50):
                    aux = 'https://datacenter.iers.org/data/6/'+x[ini:fin]
                    urls.append(aux)
                    i+=1
            if urls!= [] and x[fin-7:fin-4]==urls[-1][-7:-4]:
                x = copy.deepcopy(x[(x.index('txt'))+3:])
        else:
            x = copy.deepcopy(x[(x.index('txt'))+3:])
    return urls


def get_data(today):
    """
    Parameters
    ----------
    today : int
        today's date at 00:00h in MJD 

    Returns
    -------
    date : list of lists of ints    
    xp, yp, dut1 : list of lists of floats
            Solutions given by Bulletin A of xpol, ypol, dut1 at the epochs in
            "date" (until yesterday)
    xp_comp, yp_comp, dut1_comp : lists of floats
                    Idem as "xp", "yp", "dut1" but from today until 10 days in the future
    """
    date = []
    xp,yp,dut1 = [],[],[]
    urls = links()
    fechas = ['2022','2023','2024','2025','2026','2027']
    for items in urls:
        r = requests.get(items)
        datos = r.text
        datos = datos.split("\n")
        for j in range(len(datos)):
            if (datos[j][7:11] in fechas):
                break
        lista = datos[j:]
        lista_def = [lista[k].split() for k in range(20)]
        date.append([int(float(lista_def[k][3])) for k in range(10)])
        xp.append([float(lista_def[k][4]) for k in range(10)])  
        yp.append([float(lista_def[k][5]) for k in range(10)])  
        dut1.append([float(lista_def[k][6]) for k in range(10)])  
        
        if items == urls[0]:
            i = date[0].index(today)
            xp_comp = [float(lista_def[k][4]) for k in range(i,i+10)]
            yp_comp = [float(lista_def[k][5]) for k in range(i,i+10)]
            dut1_comp = [float(lista_def[k][6]) for k in range(i,i+10)]
    date.reverse(), xp.reverse(), yp.reverse(), dut1.reverse()
    return date, xp, yp, dut1, xp_comp, yp_comp, dut1_comp


def reduc(date, xp, yp, dut1, today):
    """
    Parameters
    ----------
    date : list of lists of int
        
    xp, yp, dut1 : list of lists of float
        Bulletin A solutions of xpol, ypol, dut1 for the epochs in "date"
    today : int
        today's date at 00:00h in MJD 

    Returns
    -------
    date_def: list of int
        
    xp_def, yp_def dut1_def: list of float
        Bulletin A solutions of xpol, ypol, dut1 for the epochs in "date_def"
    
    Notes
    -----
    We are adding this predictions to the corrected solutions, so this algorithm
    selects the Bulletin A data between the last corrected solution available 
    in the IERS C04 14 series and yesterday.
    """
    date_def = []
    xp_def, yp_def, dut1_def = [],[],[]
    for i in range(len(date)):
        aux ,aux2, aux3, aux4 = [],[],[],[]
        for j in range(10):
            if date[i][j] in date_def:
                pass
            else:
                aux.append(date[i][j])
                aux2.append(xp[i][j])
                aux3.append(yp[i][j])
                aux4.append(dut1[i][j])
        a,b,c,d = aux, aux2, aux3, aux4
        date_def+=a
        xp_def+=b
        yp_def+=c
        dut1_def+=d
    ind = date_def.index(today)
    return date_def[:ind], xp_def[:ind], yp_def[:ind], dut1_def[:ind],


def finals_all(start,today):
    """
    Parameters
    ----------
    mjd : int
        epoch in MJD
    today : int
        today's date at 00:00h

    Returns
    -------
    dx, dy : list of float
        solution from finals.data.iau2000 starting in start and finishing
        10 days into the future (all at 00:00h)
    fechas : list of int
        "dx", "dy" solution epochs
    """
    f = int(today-48622+10)   # 48622 corresponds to the first epoch in the file in mjd
    i = int(start-48622-201)  #"-201" is because we need some earlier data for future calculations
    r = requests.get('https://datacenter.iers.org/data/latestVersion/finals.data.iau2000.txt')
    rt = (r.text).split("\n")
    lista = rt[i:f]
    lista = [lista[j].split() for j in range(len(lista))]
    dx, dy = [],[]
    dx = [float(lista[k][-4]) for k in range(len(lista))]
    dy = [float(lista[k][-2]) for k in range(len(lista))]
    fechas = list(range(i+48622,i+len(dx)+48622))
    
    return dx,dy, fechas
    
def comp(today):
    """
    Parameters
    ----------
    today : int
        today's date at 00:00h in MJD

    Returns
    -------
    dx, dy : list of float
           future predictions of dx and dy published by IERS 

    """
    r = requests.get('https://datacenter.iers.org/data/latestVersion/finals.data.iau2000.txt')
    rt = (r.text).split("\n")
    for j in range(len(rt)-1,-1,-1):
        if str(today)+'.00' in rt[j]:
            lista = rt[j:j+10]
        else:
            pass
    lista = [lista[j].split() for j in range(len(lista))]
    dx, dy = [],[]
    dx = [float(lista[k][-4]) for k in range(len(lista))]
    dy = [float(lista[k][-2]) for k in range(len(lista))]
    return dx,dy


def leap_inv(x, mjd,leaps,s):
    """
    Parameters
    ----------
    x : list of float
        parameter solutions for epochs "mjd".
    mjd : list of int.
    
    leaps : list of int
        epochs in which a leap second was inserted
    s : int
        parameter that returned from another function

    Returns
    -------
    p : list of float
        parameter solution taking into account leap seconds

    """
    p = copy.deepcopy(x)
    p[0]+=0
    for j in range(1,len(x)):
        if mjd[j-1] in leaps:
            s+=1
        p[j]+=s
    return p


def decimal(lista):
    """
    Parameters
    ----------
    lista : list of floats
        Coordinate in the format: [degrees, minutes, seconds]

    Returns
    -------
    int
        Tranformation of {lista} to decimal degrees

    """
    if lista[0]>=0:
        return lista[0] + lista[1] / 60 + lista[2] / 3600 
    else:
        return lista[0] - lista[1] / 60 - lista[2] / 3600


def mult(A,B):
    """
    Parameters
    ----------
    A, B : np.array of float where A.shape[1] = B.shape[0]
        Two-dimensional matrices. 

    Returns
    -------
    C : np.array
        Matrix product between A & B
    """
    C = np.zeros([A.shape[0],B.shape[1]])
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            C[i,j] = np.array(sum([A[i,r]*B[r,j] for r in range(A.shape[1])]))
    return C


def onedim(M):
    """
    Parameters
    ----------
    M : np.array of float
        Two-dimensional Hankel matrix

    Returns
    -------
    C : list
        Transforms the Hankel matrix into a one-dimensional time series
        
    Example
    -------
    In:  onedim(np.array([[0,1,2,3],[1,2,3,4],[2,3,4,5]])
    Out: [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    """
    K = M.shape[1]
    L = M.shape[0]
    C = []
    for i in range(L):
        j=0
        ind = []
        while i>=0 and j<=K-1:
            ind.append(M[i,j])
            i-=1
            j+=1
        C.append(np.mean(ind))
    for j in range(1,K):
        i = L-1
        ind = []
        while i>=0 and j<=K-1:
            ind.append(M[i,j])
            i-=1
            j+=1
        C.append(np.mean(ind))
    return C



def greg_to_mjd(f):   
    """
    Parameters
    ----------
    f : datetime.datetime
        Gregorian time date

    Returns
    -------
    mjd : int
        f at 00:00h in MJD
    """
    y,m,d=f.timetuple()[:3]
    jd = 367*y-int((7*(y+int((m+9)/12.0)))/4.0)+int((275*m)/9.0)+d+1721013.5-0.5*math.copysign(1,100*y+m-190002.5)+0.5
    mjd = int(jd-2400000.5)
    return mjd

def read_iers():
    """
    Returns
    -------
    mjd : list of floats
        last 500 epoch values on the EOP IERS 14 C04 series
    xp : list of floats
        last 500 xpol values on the EOP IERS 14 C04 series
    yp : list of floats
        last 500 ypol values on the EOP IERS 14 C04 series
    dy : list of floats
        last 500 dy values on the EOP IERS 14 C04 series
    lod : list of floats
        last 500 lod values on the EOP IERS 14 C04 series
    dut : list of floats
        last 500 dut values on the EOP IERS 14 C04 series
    """
    r = requests.get("https://datacenter.iers.org/data/224/eopc04_14_IAU2000.62-now.txt")
    datos = r.text
    cont,j = 0,0
    while cont<14:
        if datos[j] =='\n':
            cont+=1
        j+=1
    datos=datos[j:]
    lista = datos.split("\n")
    aux = [lista[i].split() for i in range(len(lista)-501, len(lista)-1)]   #last value is an empty line
    mjd = [int(float(aux[i][3])) for i in range(len(aux))]
    xp = [float(aux[i][4]) for i in range(len(aux))]
    yp = [float(aux[i][5]) for i in range(len(aux))]
    dy = [float(aux[i][9]) for i in range(len(aux))]
    lod = [float(aux[i][7]) for i in range(len(aux))]
    dut =  [float(aux[i][6]) for i in range(len(aux))]
    return mjd,xp,yp,dy,lod,dut


def reduccion(lista):
    """
    Parameters
    ----------
    lista : list of float

    Returns
    -------
    lista_aux : list of floats
        calculates the mean value for every 8 values on the list
    """
    i = 0
    lista_aux=[]
    while i+8 <= len(lista):
        aux = 0
        for p in range(8):
            aux+=lista[i+p]
        aux = aux/8
        lista_aux.append(aux)
        i+=8
    return lista_aux


def read_aam():
    """
    Returns
    -------
    epoch : list of floats
        epoch of the xmass, ymass, zmass solutions  (daily at 00:00h from 1/01/2023
                                                  up until yesterday)
    xmass : list of floats
        xmass solution of the Atmospheric Angular Momentum at said epochs
    ymass : list of floats
        idem
    zmass : list of floats
        idem
    """
    r = requests.get("http://rz-vm115.gfz-potsdam.de:8080/repository/entry/get/ESMGFZ_AAM_v1.0_03h_2023.asc?entryid=3a09f41b-79c0-4d9b-b637-40985171a9e3")
    aam2023 = r.text
    r2 = requests.get("http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
    r2t = r2.text
    ind = r2t.index('ESMGFZ_AAM_v1.0_03h_2024.asc')
    url = 'http://rz-vm115.gfz-potsdam.de:8080/repository/entry/get/ESMGFZ_AAM_v1.0_03h_2024.asc?entryid='+ r2t[ind-36-11:ind-11]
    r3 = requests.get(url)
    aam2024 = r3.text
    r4 = requests.get('http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=39f33bc7-5ea8-4184-b940-08534f3d911f')
    r4t = r4.text
    r4t = r4t[r4t.index('"name":"ESMGFZ_AAM_v1.0_W')+20:]
    ind = r4t.index('"name":"ESMGFZ_AAM_v1.0_W')    
    url = 'http://rz-vm115.gfz-potsdam.de:8080/repository/entry/get/'+str(r4t[ind+8:ind+57])+'?entryid='+str(r4t[ind-39:ind-3])
    r5 = requests.get(url)
    aux = r5.text
    
    cont,cont2,j,i = 0,0,0,0
    
    while(cont<40):
        if aam2023[j] =="\n":
          cont+=1
        j+=1
     
    while(cont2<45):
        if aux[i] =="\n":
          cont2+=1
        i+=1
        
    aam2023=(aam2023[j:]).split("\n")
    aam2024=(aam2024[j:]).split("\n")
    ld = aux[i:].split("\n") #prediction of yesterday values (needed to predict today's)
    
    aam2023 = [aam2023[i].split() for i in range(len(aam2023)-1)]
    aam2024 = [aam2024[i].split() for i in range(len(aam2024)-1)]+[ld[i].split() for i in range(8)]
    
    epoch, xmass, ymass = [],[],[]
    epoch = [float(aam2023[j][4]) for j in range(len(aam2023))]+[float(aam2024[j][4]) for j in range(len(aam2024))]
    xmass = [float(aam2023[j][5]) for j in range(len(aam2023))]+[float(aam2024[j][5]) for j in range(len(aam2024))]
    ymass = [float(aam2023[j][6]) for j in range(len(aam2023))]+[float(aam2024[j][6]) for j in range(len(aam2024))]
    zmass = [float(aam2023[j][7]) for j in range(len(aam2023))]+[float(aam2024[j][7]) for j in range(len(aam2024))]
    
    xmass = reduccion(xmass)
    ymass = reduccion(ymass)
    zmass = reduccion(zmass)
    epoch = epoch[0:-1:8]
    return epoch,xmass,ymass,zmass

def read_oam():
    """
    Returns
    -------
    epoch : list of floats
        epoch of the xmass, ymass, zmass solutions  (daily at 00:00h from 1/01/2023
                                                  up until yesterday)
    xmass : list of floats
        xmass solution of the Oceanic Angular Momentum at said epochs
    ymass : list of floats
        idem
    zmass : list of floats
        idem
    """
    r = requests.get("http://rz-vm115.gfz-potsdam.de:8080/repository/entry/get/ESMGFZ_OAM_v1.0_03h_2023.asc?entryid=9da2cd2e-9db9-47bb-96dd-b32fce398aac")
    oam2023 = r.text
    r2 = requests.get("http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=6db4b21e-40be-4099-ad4c-358fb3f4cae8")
    r2t = r2.text
    ind = r2t.index('ESMGFZ_OAM_v1.0_03h_2024.asc')
    url = 'http://rz-vm115.gfz-potsdam.de:8080/repository/entry/get/ESMGFZ_OAM_v1.0_03h_2024.asc?entryid='+ r2t[ind-36-11:ind-11]
    r3 = requests.get(url)
    oam2024 = r3.text
    r4 = requests.get('http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=b481fb96-721c-459f-84a3-5e03f4b81220')
    r4t = r4.text
    r4t = r4t[r4t.index('"name":"ESMGFZ_OAM_v1.0')+20:]
    ind = r4t.index('"name":"ESMGFZ_OAM_v1.0')    
    url = 'http://rz-vm115.gfz-potsdam.de:8080/repository/entry/get/'+str(r4t[ind+8:ind+41])+'?entryid='+str(r4t[ind-39:ind-3])
    r5 = requests.get(url)
    aux = r5.text
    
    cont,cont2,j,i= 0,0,0,0
    
    while(cont<42):
        if oam2023[j] =="\n":
          cont+=1
        j+=1

    oam2023=(oam2023[j:]).split("\n")
    oam2024=(oam2024[j:]).split("\n")
    ld = aux[j:].split("\n")[2:] #prediction of yesterday values (needed to predict today's)
    
    oam2023 = [oam2023[i].split() for i in range(len(oam2023)-1)]
    oam2024 = [oam2024[i].split() for i in range(len(oam2024)-1)]+[ld[i].split() for i in range(8)]
    
    epoch, xmass, ymass = [],[],[]
    epoch = [float(oam2023[j][4]) for j in range(len(oam2023))]+[float(oam2024[j][4]) for j in range(len(oam2024))]
    xmass = [float(oam2023[j][5]) for j in range(len(oam2023))]+[float(oam2024[j][5]) for j in range(len(oam2024))]
    ymass = [float(oam2023[j][6]) for j in range(len(oam2023))]+[float(oam2024[j][6]) for j in range(len(oam2024))]
    zmass = [float(oam2023[j][7]) for j in range(len(oam2023))]+[float(oam2024[j][7]) for j in range(len(oam2024))]
    
    xmass = reduccion(xmass)
    ymass = reduccion(ymass)
    zmass = reduccion(zmass)
    epoch = epoch[0:-1:8]
    return epoch,xmass,ymass,zmass

def equal(mjd,epoch,xmass,ymass,zmass):
    """
    Parameters
    ----------
    mjd : list of floats
        epoch of the EOP IERS 14 C04 series returned by the function read_iers()
    
    epoch, xmass, ymass, zmass : list of floats
        said solutions of the Atmospheric Angular Momentum returned by function read_aam()

    Returns
    -------
    xmass, ymass, zmass : list of floats
        said values for the epochs of the input parameter mjd
    """
    i = epoch.index(mjd[0])
    f = epoch.index(mjd[-1])+1
    xmass = xmass[i:f]
    ymass = ymass[i:f]
    zmass = zmass[i:f]
    return xmass,ymass,zmass


def ssa(num,param):
    """
    *** Singular Spectrum Analysis***
    
    Parameters
    ----------
    num : int
        number of the Principal Components to reconstruct the time series {param}
    param : list of floats
        time series in which we separate signal from noise by SSA

    Returns
    -------
    R : np.array of floats
        reconstructed time series using {num} principal components (signal)
    N : np.array of floats
        resiudal noise left after applying SSA to {param}
    """
    #PCA
    Rdef,Ndef = [],[]
    T = len(param)
    L = 50
    K = T-L+1
    X = np.zeros([L,K])
    #maping the {param} series into the trajectory matrix (Hankel matrix) X with a window length of L (1<L<T/2)
    for i in range(L-1):
        X[i][:] = np.array(param[(-K-L+i+1):(-L+1+i)])  
    X[-1,:] = np.array(param[-K:])        
    S = mult(X,np.transpose(X))    
    #Eigenvalues and eigenvectors
    egval,egvect = la.eig(S)        
    indices = egval.argsort()[::-1]
    egval = egval[indices]
    egvect = np.transpose((np.transpose(egvect))[indices,:])
    egvect2 = np.array([(mult(np.transpose(X),egvect[:,i].reshape(-1,1)))/math.sqrt(egval[i])
                        for i in range(X.shape[0])])
    Yaux = []
    for i in range(L):
        Yaux.append(math.sqrt(egval[i])*mult(egvect[:,i].reshape(-1,1),np.transpose(egvect2[i,:,:])))  
    Y = np.array([sum(Yaux[:num])])       #Separation in PCs for reconstruction and noise
    noise = np.array([sum(Yaux[num:])])
    F = []
    for j in range(Y.shape[0]):
        F.append(onedim(Y[j]))
    F = np.array(F)
    F2 = []
    for j in range(noise.shape[0]):
        F2.append(onedim(noise[j]))
    F2 = np.array(F2)
    R = np.array([sum(F[:,i]) for i in range(F.shape[1])])
    N = np.array([sum(F2[:,i]) for i in range(F2.shape[1])]) 
    aux = [onedim(Yaux[i]) for i in range(L)]
    for i in range(num):
        aux[i] = [aux[i][j] for j in range(len(aux[i]))]
    return R,N


def interp(fecha,R):
    """
    Parameters
    ----------
    fecha : list of floats
        epoch of each value of input {R}
    R : np.array of floats
        time series to interpolate

    Returns
    -------
    extr : np.array of floats
        extrapolation of the interpolation of R for the next 10 days
    """
    pcp = PchipInterpolator(fecha[-365:],R[-365:])
    fecha2 = [fecha[-1]-j+11 for j in range(10,0,-1)]
    extr=pcp(fecha2)
    return extr
   
 
def pred_xp(xp,xmass,mjd):
    """
    Parameters
    ----------
    xp, xmass, mjd : list of floats
        input data necessary to predict {xp}. They need to correspond to the same epoch,
        i.e., {xp[30]}, {xmass[30]} are the solutions of these parameters 
        for the epoch {mjd[30]} MJD.
    Returns
    -------
    p1, p21, p22, p31, p32: np.array of floats
        prediction of {xp} for the 10 following days of {mjd}. each parameter is 
        a prediction calculated with a different model (written as a comment within the function)
    """
    #KRR:
    m = []
    for v in range(1,11):
        m.append(load(f'models/output_xp/2model/day{v}_model_xp.joblib'))   #we load the prediction models
    test = np.array(xp[-100:]+xmass[-100:]).reshape(1,-1)
    pred1 = []
    for j in range(10):
        pred1.append(m[j].predict(test))
    
    #SSA + KRR (pred2), SSA + GPR (pred3):
    pred2,pred3 = [],[]
    for num in [4,6]:
        R,N = ssa(num,xp)
        ex = interp(mjd,R)
        m1,m2 = [],[]
        for i in range(1,11):    #modelos
            m1.append(load(f'models/output_xp/model{num}/day{i}_model_xp.joblib'))
            m2.append(load(f'models/output_xp/modelgpr/{num}day{i}_model_xp.joblib')) 
        test = N[-100:].reshape(1,-1)
        aux1,aux2 = [],[]
        for i in range(10):
            aux1.append(ex[i]+m1[i].predict(test))  #predicción final = interpolado + predicho
            aux2.append(ex[i]+m2[i].predict(test))
        pred2.append(aux1)
        pred3.append(aux2)
        
    p1 = (np.array(pred1).transpose()).tolist()[0]
    p21 = (np.array(pred2[0]).transpose()).tolist()[0]
    p22 = (np.array(pred2[1]).transpose()).tolist()[0]
    p31 = (np.array(pred3[0]).transpose()).tolist()[0]
    p32 = (np.array(pred3[1]).transpose()).tolist()[0]
    return p1,p21,p22,p31,p32


def pred_yp(yp,dy,ymass,mjd):
    """
    Parameters
    ----------
    yp, dy, ymass, mjd : lists of floats
        input data necessary to predict {yp}
    Returns
    -------
    p1, p21, p22, p23, p3: np.array of floats
        prediction of {yp} for the 10 following days of {mjd}. each parameter is 
        a prediction calculated with a different model.
    """
    #KRR:
    m1,m3 = [],[]
    for v in range(1,11):
        #m1.append(load(f'models/output_yp/2model/day{v}_model_yp.joblib'))   #we load the prediction models
        m3.append(load(f'models/output_yp/modelaam/day{v}_model_yp.joblib'))   #we load the prediction models
    #test = np.array(yp[-100:]+dy[-100:]).reshape(1,-1)
    test3 = np.array(yp[-300:]+ymass[-300:]).reshape(1,-1)
    pred1,pred2,pred3 = [],[],[]
    
    for j in range(10):
        #pred1.append(m1[j].predict(test))
        pred3.append(m3[j].predict(test3))
    #SSA + KRR (pred2), SSA + GPR (pred3):
    
        
    for num in [2,4,6]:
        R,N = ssa(num,yp)
        ex = interp(mjd,R)
        m = []
        for i in range(1,11):    #modelos
            m.append(load(f'models/output_yp/model{num}/day{i}_model_yp.joblib'))
        test = N[-100:].reshape(1,-1)
        aux=[]
        for i in range(10):
            aux.append(ex[i]+m[i].predict(test))  #predicción final = interpolado + predicho
        pred2.append(aux)
        
    #p1 = (np.array(pred1).transpose()).tolist()[0]
    p21 = (np.array(pred2[0]).transpose()).tolist()[0]
    p22 = (np.array(pred2[1]).transpose()).tolist()[0]
    p23 = (np.array(pred2[2]).transpose()).tolist()[0]
    p3 = (np.array(pred3).transpose()).tolist()[0]
    return p21,p22,p23,p3
    
def pred_dx(dx,xfcn,xp):
    """
    Parameters
    ----------
    dx, xfcn, xp : lists of float
        solutions for these parameters during a certain interval of time

    Returns
    -------
    p1, p2 : list of floats
        10 day prediction of dX according to two different models
    """
    m1,m2 = [], []
    for v in range(1,11):
        m1.append(load(f'models/output_dx/model4/day{v}_model_dx.joblib'))
        m2.append(load(f'models/output_dx/model5/day{v}_model_dx.joblib'))
    test1 = np.array(dx[-500:]+xfcn[-500:]).reshape(1,-1)
    test2 = np.array(dx[-450:]+xfcn[-450:]+xp[-450:]).reshape(1,-1)
    p1,p2 = [],[]
    for j in range(10):
        p1.append(m1[j].predict(test1))
        p2.append(m2[j].predict(test2))
    p1 = (np.array(p1).transpose()).tolist()[0]
    p2 = (np.array(p2).transpose()).tolist()[0]
    return p1,p2

def pred_dy(dy,yfcn,yp):
    """
    Parameters
    ----------
    dy, yfcn, yp : lists of float
        solutions for these parameters during a certain interval of time

    Returns
    -------
    p1, p2 : list of floats
        10 day prediction of dY according to two different models
    """
    m1,m2 = [], []
    for v in range(1,11):
        m1.append(load(f'models/output_dy/model2/day{v}_model_dy.joblib'))
        m2.append(load(f'models/output_dy/model3/day{v}_model_dy.joblib'))
    test1 = np.array(dy[-500:]+yfcn[-500:]).reshape(1,-1)
    test2 = np.array(dy[-400:]+yfcn[-400:]+yp[-400:]).reshape(1,-1)
    p1,p2 = [],[]
    for j in range(10):
        p1.append(m1[j].predict(test1))
        p2.append(m2[j].predict(test2))
    p1 = (np.array(p1).transpose()).tolist()[0]
    p2 = (np.array(p2).transpose()).tolist()[0]
    return p1,p2

def pred_lod(lod,zmass,mjd):
    """
    Parameters
    ----------
    lod, zmass, mjd : list of floats
        input data necessary to predict {lod}
    Returns
    -------
    p1,p2 : np.array of floats
        prediction of {lod} for the 10 following days of {mjd}. each parameter is 
        a prediction calculated with a different model (written as a comment within the function)
    """
    #1:KRR (lod). 2:KRR (lod, AAM zmass)
    m1,m2 = [],[]
    for v in range(1,11):
        m1.append(load(f'models/output_lod/model/day{v}_model_lod.joblib'))   #we load the prediction models
        m2.append(load(f'models/output_lod/modelaam/day{v}_model_lod.joblib'))   #we load the prediction models
    test = np.array(lod[-400:]).reshape(1,-1)
    test2 = np.array(lod[-300:]+zmass[-300:]).reshape(1,-1)
    pred1,pred2 = [],[]
    for j in range(10):
        pred1.append(m1[j].predict(test))
        pred2.append(m2[j].predict(test2))

    p1 = (np.array(pred1).transpose()).tolist()[0]
    p2 = (np.array(pred2).transpose()).tolist()[0]
    return p1,p2
    
def pred_dut1(dut1,lod,zmass,czmass,mjd):
    """
    Parameters
    ----------
    dut1, mjd : list of floats
        input data necessary to predict {dut1}
    Returns
    -------
    p : np.array of floats
        prediction of {dut1} for the 10 following days of {mjd}. each parameter is 
        a prediction calculated with a different model (written as a comment within the function)
    """
    #1:KRR (dut1).
    m1,m2,m3,m4= [],[],[],[]
    for v in range(1,11):
        m1.append(load(f'models/output_dut1/model/day{v}_model_dut.joblib'))   #we load the prediction models
        #m2.append(load(f'models/output_dut1/model2/day{v}_model_dut1.joblib'))   #we load the prediction models
        #m3.append(load(f'models/output_dut1/model3/day{v}_model_dut1.joblib'))   #we load the prediction models
        m4.append(load(f'models/output_dut1/modelAM/day{v}_model_dut1.joblib'))   #we load the prediction models
    test1 = np.array(dut1[-30:]).reshape(1,-1)
    #test2 = np.array(dut1[-300:]+lod[-300:]).reshape(1,-1)
    #test3 = np.array(dut1[-300:]+lod[-300:]+zmass[-300:]).reshape(1,-1)
    test4 = np.array(dut1[-300:]+czmass[-300:]).reshape(1,-1)
    pred1,pred2,pred3,pred4 = [],[],[],[]
    p1a,p2a,p3a,p4a = [],[],[],[]
    for j in range(10):
        pred1.append(m1[j].predict(test1))
        # pred2.append(m2[j].predict(test2))
        # pred3.append(m3[j].predict(test3))
        pred4.append(m4[j].predict(test4))
        p1a.append((m1[j].predict(test1)).tolist()[0])
        #p2a.append((m2[j].predict(test2)).tolist()[0])
        #p3a.append((m3[j].predict(test3)).tolist()[0])
        p4a.append((m4[j].predict(test4)).tolist()[0])
    
    leaps = [56108,57203,57753]
    dt = mjd
    s1 = len(list(filter(lambda n: dt[0]<=n & n<=dt[-1],leaps))) 
    
    
    
    p1 = leap_inv(p1a,dt,leaps,s1)
    #p2 = leap_inv(p2a,dt,leaps,s1)
    #p3 = leap_inv(p3a,dt,leaps,s1)
    p4 = leap_inv(p4a,dt,leaps,s1)
    p1 = (np.array(pred1).transpose()).tolist()[0]
    # p2 = (np.array(pred2).transpose()).tolist()[0]
    # p3 = (np.array(pred3).transpose()).tolist()[0]
    p4 = (np.array(pred4).transpose()).tolist()[0]
    return p1,p4#p1,p2,p3,p4
    

def fcn(dx, dy, dt):
    """
    Parameters
    ----------
    dx : list of float
        dX solutions for epochs in {dt}
    dy : list of float
        dY solutions for epochs in {dt}
    dt : list of int
        

    Returns
    -------
    XF[0][0]: float
        Ac value for the epoch {dt[-1]+1} MJD
    XF[1][0]: float
        As value for the epoch {dt[-1]+1} MJD
        
    Note
    ----
    Calculates the amplitude of the FCN components. Used in function coord_fcn(dx,dy,dt,today)
    """
    A,D = np.zeros([400*2,2]),np.zeros([400*2,1])

    for i in range(400):
        ang = frecFCN*dt[i]
        C = math.cos(ang)
        S = math.sin(ang)
        A[2*i,0] = C
        A[2*i,1] = -S
        A[2*i+1,0] = S
        A[2*i+1,1] = C
    for i in range(400):
        D[2*i] = dx[i]
        D[2*i+1] = dy[i]
    A2 = np.transpose(A)
    C = np.linalg.inv(mult(A2,A))
    C2 = mult(A2,D)
    XF = mult(C,C2)
    
    return XF[0][0], XF[1][0]

def coord_fcn(dx,dy,dt):
    """
    Parameters
    ----------
    dx, dy : list of float
        solutions for these parameters 
    dt : list of float
        epoch of the solutions in J2000.0

    Returns
    -------
    x, y : list of floats
        solutions for xFCN and yFCN respectively
    fechas : list of int
        the corresponding epoch of the solutions {x}, {y}
    """
    x,y = np.array([]), np.array([])
    Ac, As, fechas = [],[],[]
    for i in range(400,len(dt)):
        j = i-400
        a,b = fcn(dx[j:i],dy[j:i],dt[j:i])
        Ac.append(a)
        As.append(b)
    for i in range(0,len(dt)-199):
        if i<len(Ac):
            j = i+200-1
            fechas.append(dt[j]+51544.5)
            a = dt[j]*frecFCN
            x = np.append(x,-As[i]*math.sin(a)+Ac[i]*math.cos(a))  #X_FCN para el día dt(j)
            y = np.append(y,As[i]*math.cos(a)+Ac[i]*math.sin(a)) 
        else:
            j = i+200-1
            fechas.append(dt[j]+51544.5)
            a = dt[j]*frecFCN
            x = np.append(x,-As[-1]*math.sin(a)+Ac[-1]*math.cos(a))  #X_FCN para el día dt(j)
            y = np.append(y,As[-1]*math.cos(a)+Ac[-1]*math.sin(a)) 

    return x.tolist(),y.tolist(), fechas


def add_date(mjd1, f,today):   
    """
    Parameters
    ----------
    mjd1 : int
        epoch in MJD at 00.00h of the first prediction date
    f : datetime.datetime 
        today's date in gregorian format
    today : int
        today's date in MJD  (today = greg_to_mjd(f))

    Returns
    -------
    lista_fechas : list of tuples 
        Predicted days' date in the format (year, month, day)
    """
    dif = today-int(mjd1)
    d = datetime.timedelta(days = dif)
    resta = f-d
    lista_fechas = []
    for i in range(10):
        d2 = datetime.timedelta(days = i)
        lista_fechas.append((resta+d2).timetuple()[:3])
    return lista_fechas
      
def act_df(texto_xp,texto_yp,texto_dx,texto_dy,texto_dut1):
    t = datetime.datetime.today()
    day_of_week = t.isoweekday()
    suffix = t.strftime('%Y%m%d')
    csv_file = 'base.csv'

    if os.path.exists(csv_file):
        files = pd.read_csv(csv_file, delimiter = ';',index_col = 0) 
        files.index = files.index.astype(str)
    else:
        files = pd.DataFrame(
            {'XPOL':[],
             'YPOL':[],
             'dX':[],
             'dY':[],
             'dUT1':[]
            },
            index = np.array([],dtype = str)
        )
    if suffix not in files.index:
        if day_of_week in {3,5}:
             b = pd.DataFrame({'XPOL':[texto_xp],'YPOL':[texto_yp],'dX':[texto_dx],'dY':[texto_dy],'dUT1':[texto_dut1]},index = [suffix])
             files = pd.concat([files,b])
             files.index = files.index.astype(str)
             files.to_csv(csv_file, sep = ';',index=True, mode = 'w')

    return files
        




    
