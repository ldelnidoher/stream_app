# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 09:31:18 2026

@author: lddelnido
"""

import numpy as np
import math
from astropy.time import Time
import os
import sqlite3
from contextlib import closing

#Path to app local repository
direc2 = "C:/Users/becario.adsaz/Documents/Prueba/stream_app"

day = 61139

# URL Santiago
url = 'https://unialicante-my.sharepoint.com/:u:/g/personal/santiago_belda_mscloud_ua_es/IQDmLGAPUE3CSbJmOpiesTZ6AZ9r3QPzk0kZfidSxidSllY?e=rRhHk6&download=1/FCN.zip/'


################### AUXILIARY  FUNCTIONS ################################
def read_db(num,lista):
    with closing(sqlite3.connect(f"{direc2}/eop_predictions.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(f""" {to_str(lista,num)}  """)
        conn.commit()   
    #conn = sqlite3.connect(f"{direc2}/eop_predictions.db", timeout = 5)
    #cursor = conn.cursor()
    #cursor.execute(f""" {to_str(lista,num)}  """)
    #conn.commit()
    #conn.close()
    return 0

"""
SI ERROR AL EJECUTAR CON RESTART EL KERNEL SUELE FUNCIONAR
"""

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

def to_str(lst,num):
    aa = ['eop_old','eop_new','fcn_cpo']
    st = f'INSERT INTO {aa[num]} (date, epoch, ac, [as], x0, y0, dx, dy) VALUES '
    for x in lst:
        st = st+str(tuple(x))+','
    #print(st[:-1]+';')
    return st[:-1]+';'

def delete_range(conn, id_inicio, id_fin, num):
    aa = ['eop_old','eop_new','fcn_cpo']
    query = f"DELETE FROM {aa[num]} WHERE epoch BETWEEN ? AND ?"
    with closing(conn.cursor()) as cursor:
        cursor.execute(query, (id_inicio, id_fin))
    conn.commit()

def get_last_epoch(conn, num, param):
    aa = ['eop_old','eop_new','fcn_cpo']
    query = f"SELECT MAX({param}) FROM {aa[num]}"
    with closing(conn.cursor()) as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result[0]
            
###################### FCN ###########################

with closing(sqlite3.connect(f"{direc2}/eop_predictions.db")) as conn:
    last_day=get_last_epoch(conn, 2, 'epoch')
    delete_range(conn, last_day-564, last_day, 2)

direc = direc2+'/fcn_cpo/FCN_CPO_IERS_C0420_20260329.txt'

fday = (Time(day, format = 'mjd').to_datetime()).strftime('%Y%m%d')
print(fday)
dir1 = url+f'FCN_CPO_IERS_C0420_{fday}.txt'
print(dir1)


f= open(direc,'r')
data = f.readlines()
f.close()

new_day=int(float(data[-1].split()[0]))

data = list(np.transpose([j.split() for j in data[(last_day-565-new_day):]]))

data[0] = [int(float(x)) for x in data[0]]
for j in range(1,7):
    data[j] = [float(x) for x in data[j]]
    
rows = []
a= data[0]
mjd = [Time(j,format = 'mjd') for j in a]
date = [j.iso[:-4] for j in mjd]
rows.append(date)
for j in range(0,7):
    rows.append(data[j])

rows1 = [[fila[i] for fila in rows] for i in range(len(rows[0]))]

df_old= read_db(2,rows1)

"""
for i in range(2):
    f = open(dirs1[i],'r')
    data = f.readlines()
    f.close()
    
    data = list(np.transpose([j.split() for j in data]))
    
    names = ['MJD','ac','as','x0','y0','dx','dy']
    num = [0,1,2,3,7,8]
    
    data[0] = [int(x) for x in data[0]]
    for j in range(1,6):
        data[num[j]] = [float(x) for x in data[num[j]]]
      
    
    rows1 = []
    for j in range(len(names)):
        aux = [d,names[j],i]
        if num[j] == 0:
            aux = aux+data[num[j]]
        else:
            aux = aux+ data[num[j]]
        rows1.append(aux)
     
    df_old= read_db(0,rows1)
    
    

    f = open(dirs2[i],'r')
    data = f.readlines()
    f.close()

    data = list(np.transpose([j.split() for j in data]))

    names = ['epoch','dx','dy']
    num = [0,7,8]

    data[0] = [int(x) for x in data[0]]
    for j in range(1,3):
        data[num[j]] = [float(x) for x in data[num[j]]]
        
    rows2 = []
    for j in range(len(names)):
        aux = [d,names[j],i]
        if num[j] == 0:
            aux = aux+data[num[j]]
        else:
            aux = aux+ data[num[j]]
        rows2.append(aux)
     
    df_new = read_db(1,rows2)
    
"""
