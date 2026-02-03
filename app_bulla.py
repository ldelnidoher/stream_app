import streamlit as st
import numpy as np
import pandas as pd
import time
import datetime 
from astropy.time import Time
import os
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
import sqlite3
from streamlit_option_menu import option_menu
from streamlit_scroll_to_top import scroll_to_here
from functions_app import *
from texts_app import *
st.set_page_config(layout = 'wide', page_title='EOP data', page_icon = ':earth_africa:')

#Creating a "scroll to top of the page" button
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')  # Scroll to the top of the page
    st.session_state.scroll_to_top = False  # Reset the state after scrolling
def scroll():
    st.session_state.scroll_to_top = True


st.components.v1.html(custom_html)

#Menu on top of the page
menu = option_menu(menu_title = None,
                   options=["INTRODUCTION","EOP PREDICTIONS", "PREDICTION MODELS","ABOUT US"],
                   orientation = "horizontal",
                   menu_icon = None,
                   styles = {
                        "container": {"background-color": "#FFC498" },
                        "nav-link": {"font-size": "16px", "text-align": "center"},
                        "nav-link-selected": {"background-color": "#FB6A00", "font-size": "18px"},
                        },
                  )

if menu == "INTRODUCTION":
    st.markdown(introduction,unsafe_allow_html=True)
   

#About us page
if menu == "ABOUT US":
    st.markdown(about_us, unsafe_allow_html=True)


#EOP predictions page     
if menu == "EOP PREDICTIONS":
    st.markdown('### Choose a model:')

    tab1, tab2 = st.tabs(["**MACHINE LEARNING PREDICTION**", "**FCN-CPOs PREDICTION**"])
    with tab1:
        try:
            #Connection to db database where all predictions are stored
            dff = read_db(0)
            dff_aux= read_db(1)
            
            #For easy access to the desired file, we will filter it by year, then month and finally day.
            dff = separate_dates(dff)
            dff_aux = separate_dates(dff_aux)
            
            #Construction of historic data
            df_no_hist, df_si_hist = history(dff,dff_aux)
           
            upt = (dff.pub_date[len(dff)-1])[:10]
            
            ##############################################################################################################
            #Filter the files for the user
            st.header('Short-term EOP predictions: 10 days')
            st.subheader('Introduction')
            st.markdown(ml_intro1+f' <i>(Last updated: {upt})</i></div>',unsafe_allow_html=True)
            st.markdown(ml_intro2, unsafe_allow_html=True) 
    
            st.divider()
            
            st.subheader('Historical records:')
            st.markdown(ml_historical,unsafe_allow_html=True)
            np.savetxt('history_no_eam.txt',df_no_hist, fmt = ['% s','%5d','%1d','% .8f','% .8f','% .9f', '% .5f','% .5f', '% s','% s'], delimiter='   \t', header = 'Date [YY-MM-DD]  | Epoch[MJD] |Prediction day| xpol[as]     |  ypol[as]    |   dUT1[s]     |   dX[mas]    |    dY[mas]    |    dX_new[mas] |   dY_new[mas]  ')   
            np.savetxt('history_with_eam.txt',df_si_hist, fmt = ['% s','%5d','%1d','% .8f','% .8f','% .9f', '% .5f','% .5f', '% s','% s'], delimiter='   \t', header = 'Date [YY-MM-DD]  | Epoch[MJD] |Prediction day| xpol[as]     |  ypol[as]    |   dUT1[s]     |   dX[mas]    |    dY[mas]    |    dX_new[mas] |   dY_new[mas]  ') 
            
            f = open('history_no_eam.txt','r') 
            lista_no = f.read()
            f.close()
            
            f = open('history_with_eam.txt','r') 
            lista_si = f.read()
            f.close()
            
            col1,col2 = st.columns([0.5,0.5],gap = 'small')
            with col1:
                st.write('Historic predictions for all EOPs using **w/o EAM models**:')
                col3,col4 = st.columns([0.3,0.7],gap = 'small')
                with col3:
                     st.download_button(label =':arrow_heading_down: .txt file :arrow_heading_down:', file_name = f'history_no_eam.txt', data = lista_no)
                with col4:
                     st.download_button(label =':arrow_heading_down: .csv file :arrow_heading_down:', file_name = f'history_no_eam.csv', data = df_no_hist.to_csv(index = False))
            with col2:
                st.write('Historic predictions for all EOPs using **w/ EAM models**:')
                col3,col4 = st.columns([0.3,0.7],gap = 'small')
                with col3:
                     st.download_button(label =':arrow_heading_down: .txt file :arrow_heading_down:', file_name = f'history_with_eam.txt', data = lista_si)
                with col4:
                     st.download_button(label =':arrow_heading_down: .csv file :arrow_heading_down:', file_name = f'history_with_eam.csv', data = df_si_hist.to_csv(index = False)) 
                     
                 
            st.divider() 
            ####################################################################################################################
            
            st.subheader('Results by parameter:')
            st.write('Filtering results by epoch and parameter:')
            selected = st.selectbox('Choose an EOP:', ('xpol', 'ypol', 'dX', 'dY', 'UT1-UTC'),)  #choosing a parameter
            eop = ['xpol', 'ypol', 'dX', 'dY', 'UT1-UTC']
            if selected in ['xpol','ypol']:
                 val = selected
            if selected == 'dX':
                 val = 'dx'
            if selected == 'dY':
                 val = 'dy'
            if selected == 'UT1-UTC':
                 val = 'dut1' 
            st.write(f'**Predictions for {selected:}**')

        
            df2 = dff[dff['parameter']==val]
            df_mjd = dff[dff['parameter'] == 'epoch']
            st.write('Filters:') 
            col1,col2,col3 = st.columns(3)
            with col1:
                 ll = list(set(df2.year.values))
                 ll.sort(reverse=False)
                 years = st.selectbox(label = '1.- Select a year:', options = ll, index = ll.index(max(ll)))
                 df3 = df2[df2['year']==years]
            with col2:
                 ll = list(set(df3.month.values))
                 ll.sort(reverse=False)
                 months = st.selectbox(label = '2.- Select a month:', options = ll, index = ll.index(max(ll)))
                 df4 = df3[df3['month']==months]
            with col3:
                 ll = list(set(df4.day.values))
                 ll.sort(reverse=False)
                 days = st.selectbox(label = '3.- Select a day:', options = ll, index = ll.index(max(ll)))
                 df5 = df4[df4['day']==days]
            

            df, txt, fm = create_df(val,df5,df_mjd)
            t = False
            if val in {'dx','dy'}:
                df, t = df_filtered(dff_aux,df,val, years, months, days)
            #Visualization of the predictions for the chosen epoch in a table format
            
            styles = [dict(selector="", props=[('border','2px solid #fb9a5a')]), dict(selector="th", props=[("background-color","#b2d6fb"),('color','black')])] 
            s = df.style.set_table_styles(styles)
            st.table(s)
    
            #Creating .txt and .csv files with the predictions for the chosen epoch
            string, lista = create_download(df,selected,txt,fm,t)
            d = df['Epoch [MJD]'].iloc[0]
            
            col1,col2 = st.columns([0.2,0.8],gap = 'small')
            with col1:
                  st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = f'{string}_{d}.txt', data = lista)
            with col2:
                  st.download_button(label =':arrow_heading_down: Save data as .csv :arrow_heading_down:', file_name = f'{string}_{d}.csv', data = df.to_csv(index = False))
             
            #Visualization of the chosen data in an interactive plot 
            
            st.write('Interactive plot:')
            
            if val in {'dx','dy'} and t:
                lim = 5
            else: 
                lim = 3
                
            with st.container(border = True):
                fig = fig_eops(df,txt,selected,lim)
                st.plotly_chart(fig, use_container_width=True)
                
        #Error message
        except:
            with st.spinner(text="Uploading. This process might take a few minutes..."):
                time.sleep(15)
                st.rerun()
         
    with tab2: #CPO_FCN MODEL
        try:
            #Connection to db database where all predictions are stored
            df_fcn = read_db(2)
            upt = (df_fcn.date[len(df_fcn)-1])[:10]
            fm = ['% s','%5d','% .4f','% .4f','% .4f','% .4f','% .4f','% .4f']  
            np.savetxt('fcn_cpo.txt',df_fcn,fmt = fm, delimiter = '   \t', header = 'Date [YY-MM-DD]    |  Epoch [MJD] |    Ac [muas]   |   As [muas]  |    X0 [muas]  |    Y0 [muas]  |    dX [muas]   |   dY [muas]')
            
            f = open('fcn_cpo.txt','r')
            ls = f.read()
            f.close()
            
            #read iers
            dx_c04, dy_c04 = read_iers()
            
            st.header('FCN-CPOs prediction')
            st.markdown(fcn_intro +f' <i>(last updated: {upt}).</i></div>', unsafe_allow_html=True)
            
            st.subheader("Interactive plot")
            inicio, fin = interval_dates(df_fcn)
            intervalo = st.date_input("Select a date range:",
                                      value = [inicio, fin],
                                      min_value = datetime.date(1962,1,1),
                                      max_value = fin,
                                      help = fcn_help_plot,
                                      label_visibility='visible'
                                      )
            
            with st.container(border = True):
                figfcn = fig_fcn(intervalo, df_fcn, dx_c04, dy_c04)
                st.plotly_chart(figfcn, use_container_width=True)
                
           
            #Create .txt and .csv files:
            st.subheader('Data files')
            st.write('Here you can download all the solutions of this model since 1962-01-01: amplitudes (Ac, As), constant offsets (X0, Y0) and the celestial polar offsets.')
            col1,col2,col3 = st.columns([0.2,0.2,0.6],gap = 'small')
            with col1:
                  st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = 'fcn_cpo.txt', data = ls)
            with col2:
                  st.download_button(label =':arrow_heading_down: Save data as .csv :arrow_heading_down:', file_name = 'fcn_cpo.csv', data = df_fcn.to_csv(index = False))
            with col3:
                  st.download_button(label =':arrow_heading_down: Save plot as .png :arrow_heading_down:', file_name = 'fcn_cpo_plot.png', data = open('fcn_cpo_plot.png','rb').read())
            
            
            st.write('**Please, if you use this data we would appreciate you to cite our article:**')  
            col1,col2= st.columns([0.2,0.8],gap = 'small')
            with col1: 
                st.download_button(label =':memo: Citation to .bib', file_name = 'article_citation.bib', data = open('article_citation.bib','rb').read())
            with col2: 
                st.download_button(label =':memo: Citation to .txt', file_name = 'article_citation.txt', data = open('article_citation.txt','rb').read())
                      
            st.divider()  

            
        #Error message
        except:
            with st.spinner(text="Uploading. This process might take a few minutes..."):
                time.sleep(15)
                st.rerun()  
        

#Prediction models theory page
if menu == "PREDICTION MODELS":
    st.header("Short-term EOP predictions: 10 days")
    st.subheader("Prediction models without EAM")
    st.markdown(pred_short_no, unsafe_allow_html = True)
    st.image('esquema.png',output_format = 'PNG',width = 1420) 
    st.divider()

    st.subheader("Prediction models using EAM")
    st.markdown(pred_short_si, unsafe_allow_html = True)
    st.image('esquema_eam.png',output_format = 'PNG',width = 1420)
   
     

columns = st.columns([0.9,0.1], gap = "small")
with columns[0]: 
    pass
with columns[1]:
    st.button('Scroll to top', on_click=scroll)

    