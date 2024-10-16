import streamlit as st
import numpy as np
import pandas as pd
import time
import datetime
from main_ba import *
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
#arreglar en todos intervalo dt en pred_dut1

add_selectbox = st.sidebar.radio('Choose data to show:',
("Predictions", "Past predictions","Contact info"))
if add_selectbox == "Contact info":
    pass

try:
    xp_pred[0]

    # if chosen == "Predictions":
    if add_selectbox == "Predictions":
        chosen2 = st.sidebar.radio(
            'Which prediction?',
            ('xpol','ypol','dX','dY')
        )
        st.header('Short-term prediction for 10 days:')
        if chosen2 == 'xpol':
            st.write('Predictions using different models for **XPOL [as]** during the epoch [MJD]:')
            c2 = st.radio("Data visualization:",("Table","Interactive plot"))
            if c2 == "Table":
                st.dataframe(xp_pred, hide_index = True)
            if c2 == "Interactive plot":
                st.plotly_chart(fig_xp, use_container_width=False)
                
            col1, col2 = st.columns([1,1])
            with col1:
                st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'xp_preds.txt', data = texto_xp)
            with col2:
                st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'xp_historic.txt', data = texto_xp2)
        if chosen2 == 'ypol':
            st.write('Predictions using different models for **YPOL [as]** during the epoch [MJD]:')
            c2 = st.radio("Data visualization:",("Table","Interactive plot"))
            if c2 == "Table":
                st.dataframe(yp_pred, hide_index = True)
            if c2 == "Interactive plot":
                st.plotly_chart(fig_yp, use_container_width=False)
                
            st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'yp_preds.txt', data = texto_yp)
            st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'yp_historic.txt', data = texto_yp2)
            
        if chosen2 == 'dX':
            st.write('Predictions using different models for **dX [as]** during the epoch [MJD]:')
            c2 = st.radio("Data visualization:",("Table","Interactive plot"))
            if c2 == "Table":
                st.dataframe(dx_pred, hide_index = True)
            if c2 == "Interactive plot":
                st.plotly_chart(fig_dx, use_container_width=False)
                
            st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'dx_preds.txt', data = texto_dx)
            st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dx_historic.txt', data = texto_dx2)
            
        if chosen2 == 'dY':
            st.write('Predictions using different models for **dY [as]** during the epoch [MJD]:')
            c2 = st.radio("Data visualization:",("Table","Interactive plot"))
            if c2 == "Table":
                st.dataframe(dy_pred, hide_index = True)
            if c2 == "Interactive plot":
                st.plotly_chart(fig_dy, use_container_width=False)
                
            st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'dy_preds.txt', data = texto_dy)
            st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dy_historic.txt', data = texto_dy2)
            
        # if chosen2 == 'LOD':
        #     st.write('Predictions using different models for ***LOD [ms]*** during the epoch [MJD]:')
        #     c2 = st.radio("Data visualization:",("Table","Interactive plot"))
        #     if c2 == "Table":
        #         st.dataframe(lod_pred, hide_index = True)
        #     if c2 == "Interactive plot":
        #         st.plotly_chart(fig_lod, use_container_width=False)
        #     col1, col2 = st.columns([1,1])
        #     with col1:
        #         st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'lod_preds.txt', data = texto_lod)
        #     with col2:
        #         st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'lod_historic.txt', data = texto_lod2)
            
        # if chosen2 == 'UT1-UTC':
        #     st.write('Predictions using different models for **UT1-UTC [s]** during the epoch [MJD]:')
        #     c2 = st.radio("Data visualization:",("Table","Interactive plot"))
        #     if c2 == "Table":
        #         st.dataframe(dut1_pred, hide_index = True)
        #     if c2 == "Interactive plot":
        #         st.plotly_chart(fig_dut1, use_container_width=False)
        #     col1, col2 = st.columns([1,1])
        #     with col1:
        #         st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'dut1_preds.txt', data = texto_dut1)
        #     with col2:
        #         st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dut1_historic.txt', data = texto_dut12)
        
                                                   
    if add_selectbox == "Past predictions":
        chosen3 = st.sidebar.radio(
            'Which prediction?',
            ('xpol','ypol','dX','dY','LOD','UT1-UTC')
        )
        add_selectbox2 = st.sidebar.radio('Using model:',('Day 1', 'Day 10'))
        if add_selectbox2 == 'Day 1':
            col1, col2, col3 = st.columns(3)
            if chosen3 == "xpol":
                st.plotly_chart(fig_xp2, use_container_width=True)
                st.plotly_chart(fig_xp3, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'xp_historic.txt', data = texto_xp2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
                        
            if chosen3 == "ypol":
                st.plotly_chart(fig_yp2, use_container_width=True)
                st.plotly_chart(fig_yp3, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'yp_historic.txt', data = texto_yp2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
            if chosen3 == "dX":
                st.plotly_chart(fig_dx2, use_container_width=True)
                st.plotly_chart(fig_dx3, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dx_historic.txt', data = texto_dx2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
            if chosen3 == "dY":
                st.plotly_chart(fig_dy2, use_container_width=True)
                st.plotly_chart(fig_dy3, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dy_historic.txt', data = texto_dy2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
            if chosen3 == "LOD":
                st.plotly_chart(fig_lod2, use_container_width=True)
                st.plotly_chart(fig_lod3, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'lod_historic.txt', data = texto_lod2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
            if chosen3 == "UT1-UTC":
                st.plotly_chart(fig_dut12, use_container_width=True)
                st.plotly_chart(fig_dut13, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dut1_historic.txt', data = texto_dut12)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
        if add_selectbox2 == 'Day 10':
            col1, col2, col3 = st.columns(3)
            if chosen3 == "xpol":
                st.plotly_chart(fig_xp5, use_container_width=True)
                st.plotly_chart(fig_xp6, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'xp_historic.txt', data = texto_xp2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
                        
            if chosen3 == "ypol":
                st.plotly_chart(fig_yp5, use_container_width=True)
                st.plotly_chart(fig_yp6, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'yp_historic.txt', data = texto_yp2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
            if chosen3 == "dX":
                st.plotly_chart(fig_dx5, use_container_width=True)
                st.plotly_chart(fig_dx6, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dx_historic.txt', data = texto_dx2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
            if chosen3 == "dY":
                st.plotly_chart(fig_dy5, use_container_width=True)
                st.plotly_chart(fig_dy6, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dy_historic.txt', data = texto_dy2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
            if chosen3 == "LOD":
                st.plotly_chart(fig_lod5, use_container_width=True)
                st.plotly_chart(fig_lod6, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'lod_historic.txt', data = texto_lod2)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
            if chosen3 == "UT1-UTC":
                st.plotly_chart(fig_dut15, use_container_width=True)
                st.plotly_chart(fig_dut16, use_container_width=True)
                with col1:
                    st.download_button(label =':arrow_heading_down: Save historic data as .txt :arrow_heading_down:', file_name = 'dut1_historic.txt', data = texto_dut12)
                with col2:
                    st.link_button(label = "Link to IERS EOP 14 C04 series",url = "https://datacenter.iers.org/data/latestVersion/EOP_14_C04_IAU2000A_one_file_1962-now.txt")
                with col3:
                    st.link_button(label = "Link to ESMGFZ repository: AAM",url = "http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=57600abc-2c31-481e-9675-48f488b9304d")
                                                         
                                                                 

    d = datetime.datetime.now()
    d = d.replace(microsecond=0)
     
    st.write(f'Last updated: {d} UTC+2')

except:
    st.write(':hourglass: Data is currently being updated. This process might take a few minutes :hourglass:')



 


