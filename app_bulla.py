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

st.set_page_config(layout = 'wide', page_title='EOP data', page_icon = ':earth_africa:')

#Creating a "scroll to top of the page" button
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')  # Scroll to the top of the page
    st.session_state.scroll_to_top = False  # Reset the state after scrolling
def scroll():
    st.session_state.scroll_to_top = True



#here we store the larger texts so the code doesn't get too overcrowded
text1 = 'The prediction of the parameters is calculated using **Machine Learning** algorithms. The prediction horizon extends 10 days into the future, in addition to the day on which the calculations are conducted, referred to as Day 0.'
text2 = '[IERS EOP 20 C04, IERS finals.all](https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html) and [GFZ Effective Angular Momentum Functions](http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=e0fff81f-dcae-469e-8e0a-eb10caf2975b) are employed as input data. On 5 June 2025 the series IERS EOP 20 C04 was discontinued and ever since IERS EOP 20u23 C04 is used as input.'
text3 = text2+' Two predictive models are applied. **w/o EAM** utilises only EOP data as input whereas **w/ EAM** includes both EOP data and Effective Angular Momentum data.'
text4 = 'Here we present a compilation of all the predictions, calculated every Wednesday, in a single file. As two different prediction models are used, two separate files are provided.'
text5 = 'Here we present the **FCN-CPOs** solutions that we obtained in the FCN_CPO model, alongside the IERS 20u23 C04 CPOs solutions for comparison.'
text6 = text5 + 'The methodology and details about this model can be found in the following paper: [Belda, S., Ferrándiz J.M., Heinkelmann R., Nilsson T. and Schuh H. (2016). *Testing a new Free Core Nutation empirical model (2016)*](DOI:10.1016/j.jog.2016.02.002)'


#Banner image
custom_html = """
<div class="banner">
     <img src="https://github.com/ldelnidoher/stream_app/blob/main/logos.png?raw=true" alt="Banner Image">
</div>
<style>
     <center>
         .banner {
             width: 100%;
             height: 70px;
             overflow: hidden;
         }
         .banner img {
             width: 75%;
             object-fit: cover;
         }
    </center>
</style>
"""
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
    st.markdown(
    """
    ### **Welcome to the repository of the VLBI Analysis Center of the University of Alicante (UAVAC).**

    In this app you will be able to find:
    - EOP short-term predictions.
    - FCN-CPOs predictions.
    - Downloadable data in different formats and plots.
        
    In the menu option :orange[***"EOP PREDICTIONS"***] you will find different parameters predictions, both with downloadable historic data files in .txt and .csv. and interactive plots.  
    In this plots you will be able to zoom in/out, select and especific area, choose which data to display (by right-clicking the parameter in the plot legend) and download them as .png. This options 
    are found in the top right corner of the plot.

    In the menu option :orange[***"PREDICTION MODELS"***] you will find diagrams and explanations further in depth about the prediction models used. 

    In the menu option :orange[***"ABOUT US"***] you will find about the institutions involved in this project and contact information.

    *This app is still under construction, so it might change with time. Thank you for your understanding.*    
    """
    )

#About us page
if menu == "ABOUT US":
    st.markdown(
    """
    We are a team of scientists working in collaboration from:
    - VLBI Analysis Center of the University of Alicante: [UAVAC](https://web.ua.es/en/uavac/)
    - Geodesy Area of the Spanish National Geographic Institute: [IGN Geodesy](https://www.ign.es/web/ign/portal/gds-area-geodesia)
    - Atlantic Network of Space Geodetic Stations: [RAEGE](https://raege.eu/)'
    
    *If you have any questions or suggestions, please write to lucia.delnido@ua.es*
    """
    )



#EOP predictions page     
if menu == "EOP PREDICTIONS":
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
            st.write(text1+f' *(Last updated: {upt})*')
            st.markdown(text3) 
    
            st.divider()
            
            st.subheader('Historical records:')
            st.write(text4)
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
            if selected == 'xpol':
                 val = 'xp'
            if selected == 'ypol':
                 val = 'yp'
            if selected == 'dX':
                 val = 'dx'
            if selected == 'dY':
                 val = 'dy'
            if selected == 'UT1-UTC':
                 val = 'dt' 
            st.write(f'**Predictions for {selected:}**')
            # st.write(text3) 
        
            
            df2 = dff[dff['param']==val]
            df_mjd = dff[dff['param'] == 'mj']
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
            dff_fcn = read_db(2)
            upt = (dff_fcn.pub_date[len(dff_fcn)-1])[:10]
            df_fcn, fm = fcn_cpo(dff_fcn)
            np.savetxt('fcn_cpo.txt',df_fcn,fmt = fm, delimiter = '   \t', header = 'Date [YY-MM-DD]    |  Epoch [MJD] |    Ac [muas]   |   As [muas]  |    X0 [muas]  |    Y0 [muas]  |    dX [muas]   |   dY [muas]')
            
            f = open('fcn_cpo.txt','r')
            ls = f.read()
            f.close()
            
            #read iers
            dx_c04, dy_c04 = read_iers()
            
            st.header('FCN-CPOs prediction')
            st.write(text6)
            st.write(f'This data gets updated bi-monthly *(last updated: {upt})*.')
            
            st.subheader("Interactive plot")
            inicio, fin = interval_dates(df_fcn)
            intervalo = st.date_input("Select a range",
                                      value = [inicio, fin],
                                      min_value = datetime.date(1962,1,1),
                                      max_value = fin,
                                      help = 'In order not to potentially freeze the app, it is advised to select less than 10 years of data. Nevertheless it is possible to load all 60+ years.',
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
    st.markdown('- For **xpol** prediction, each component is preprocessed by applying **Singular Spectrum Analysis (SSA)** in order to obtain a reconstructed time series and the residual noise time series. Using the **Kernel Ridge Regression (KRR)** algorithm, two models are trained: one to predict the reconstructed time series and the other to predict the noise. Both predictions are then added to generate the final xpol prediction. Idem **ypol**.')
    st.markdown('- For the **dX** prediction, the **Free Core Nutation (FCN)** x component (xFCN) is calculated, and alongside dX they are used to train a model using **KRR** to predict dX. Idem **dY**.')
    st.markdown('- For the **dUT1** prediction, the data is preprocessed by removing the leap seconds. Afterwards, a model is trained using **KRR** to predict this modified dUT1 time series. Lastly, the leap seconds are added back to obtain the final dUT1 prediction.')
    st.image('esquema.png',output_format = 'PNG',width = 1420) 
    st.divider()

    st.subheader("Prediction models using EAM")
    st.write("To predict EOP using **Effective Angular Momentum** Functions data, we will sum into one variable -called **xEAM**- the xmass and xmotion components of Atmospheric Angular Momentum (AAM), Oceanic Angular Momentum (OAM) and Hydrological Angular Momentum (HAM). We follow the same proceeding with the y and z components to obtain the variables **yEAM** and **zEAM**.")
    st.markdown("- For **xpol** prediction, each component is preprocessed by applying **Singular Spectrum Analysis (SSA)** in order to obtain a reconstructed time series and the residual noise time series. Using this parameters alongside xEAM a model is trained using **Kernel Ridge Regression (KRR)** algorithm to predict xpol. Idem **ypol**.")
    st.markdown("- For the **dX** prediction, the **Free Core Nutation (FCN)** x component (xFCN) is calculated, and alongside dX and xEAM they are used to train a model using **KRR** to predict dX. Idem **dY**.")
    st.markdown("- For the **dUT1** prediction, the data is preprocessed by removing the leap seconds. Afterwards, alongside with zEAM, a model is trained using **KRR** to predict this modified dUT1 time series. Lastly, the leap seconds are added back to obtain the final dUT1 prediction.")
    st.image('esquema_eam.png',output_format = 'PNG',width = 1420)
   
     

columns = st.columns([0.9,0.1], gap = "small")
with columns[0]: 
    pass
with columns[1]:
    st.button('Scroll to top', on_click=scroll)

    
     


