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

st.set_page_config(layout = 'wide', page_title='EOP prediction', page_icon = ':earth_africa:')

#Creating a "scroll to top of the page" button
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    scroll_to_here(0, key='top')  # Scroll to the top of the page
    st.session_state.scroll_to_top = False  # Reset the state after scrolling
def scroll():
    st.session_state.scroll_to_top = True


text1 = 'The prediction of the parameters is calculated using **Machine Learning** algorithms. The prediction horizon extends 10 days into the future, in addition to the day on which the calculations are conducted, referred to as Day 0.'
text2 = '[IERS EOP 20 C04, IERS Bulletin A](https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html) and [GFZ Effective Angular Momentum Functions](http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=e0fff81f-dcae-469e-8e0a-eb10caf2975b) are employed as input data.'
text3 = text2+' Two predictive models are applied. **w/o EAM** utilises only EOP data as input whereas **w/ EAM** includes both EOP data and Effective Angular Momentum data.'


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
                   options=["EOP PREDICTIONS", "PREDICTION MODELS", "ABOUT US"],
                   orientation = "horizontal",
                   menu_icon = None,
                   styles = {
                        "container": {"background-color": "#FFC498" },
                        "nav-link": {"font-size": "16px", "text-align": "center"},
                        "nav-link-selected": {"background-color": "#FB6A00", "font-size": "18px"},
                        },
                  )
st.divider()

#About us page
if menu == "ABOUT US":
    st.write("We are a team of scientists working in collaboration from:")
    st.markdown('- VLBI Analysis Center of the University of Alicante: [UAVAC](https://web.ua.es/en/uavac/)')
    st.markdown('- Geodesy Area of the Spanish National Geographic Institute: [IGN Geodesy](https://www.ign.es/web/ign/portal/gds-area-geodesia)')
    st.markdown('- Atlantic Network of Space Geodetic Stations: [RAEGE](https://raege.eu/)')



#EOP predictions page     
if menu == "EOP PREDICTIONS":
    try:
        #Connection to db database where all predictions are stored
        db_path = 'db.db' 
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""SELECT * from polls_files """)
        dff=pd.read_sql("""SELECT * from polls_files """, conn)  #DataFrame with all the prediction data from the database
        conn.close()

        #For easy access to the desired file, we will filter it by year, then month and finally day.
        dff = separate_dates(dff)
        
        #Construction of historic data
        df_no_hist, df_si_hist = history(dff)
        
        
        ##############################################################################################################
        #Filter the files for the user
        st.header('Short-term EOP predictions: 10 days')
        st.write(text1)
        st.markdown(text3) 

        st.divider()
        
        st.subheader('Historical records:')
        f = open('historic_no_eam.txt','r') 
        lista_no = f.read()
        f.close()
        
        f = open('historic_with_eam.txt','r') 
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
        
        if val in {'dx','dy'}:
            db_path = 'db.db' 
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""SELECT * from polls_files_new """)
            dff_aux=pd.read_sql("""SELECT * from polls_files_new """, conn)  #DataFrame with all the prediction data from the database
            conn.close()

            #For easy access to the desired file, we will filter it by year, then month and finally day.
            dff_aux = separate_dates(dff_aux)
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
            
        #Visualization of the predictions for the chosen epoch in a table format
        styles = [dict(selector="", props=[('border','2px solid #fb9a5a')]), dict(selector="th", props=[("background-color","#b2d6fb"),('color','black')])] 
        s = df.style.set_table_styles(styles)
        st.table(s)

        #Creating .txt and .csv files with the predictions for the chosen epoch
        string, lista = create_download(df,selected,txt,fm)
        
        # col1,col2 = st.columns([0.2,0.8],gap = 'small')
        # with col1:
        #      st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = f'{string}_{epochs[0]}.txt', data = lista)
        # with col2:
        #      st.download_button(label =':arrow_heading_down: Save data as .csv :arrow_heading_down:', file_name = f'{string}_{epochs[0]}.csv', data = df.to_csv(index = False))
         
        #Visualization of the chosen data in an interactive plot 
        st.write('Interactive plot:')
        
        if val in {'dx','dy'} and t:
            lim = 5
        else: 
            lim = 3
            
        fig = go.Figure()
        for j in range(1,lim):
             fig.add_trace(go.Scatter(
                 x = df['Epoch [MJD]'],y = df[df.columns[-j]],
                 mode = 'lines+markers', marker = dict(size = 5), line = dict(width = 1.5),name = df.columns[-j]))
         
        fig.update_layout(legend_title_text = "Models")
        fig.update_xaxes(title_text="MJD")
        fig.update_yaxes(title_text=f"[{txt}")
        
        st.plotly_chart(fig, use_container_width=True)
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
    st.image('esquema.png',output_format = 'png', use_container_width = False)
    st.divider()

    st.subheader("Prediction models using EAM")
    st.write("To predict EOP using **Effective Angular Momentum** Functions data, we will sum into one variable -called **xEAM**- the xmass and xmotion components of Atmospheric Angular Momentum (AAM), Oceanic Angular Momentum (OAM) and Hydrological Angular Momentum (HAM). We follow the same proceeding with the y and z components to obtain the variables **yEAM** and **zEAM**.")
    st.markdown("- For **xpol** prediction, each component is preprocessed by applying **Singular Spectrum Analysis (SSA)** in order to obtain a reconstructed time series and the residual noise time series. Using this parameters alongside xEAM a model is trained using **Kernel Ridge Regression (KRR)** algorithm to predict xpol. Idem **ypol**.")
    st.markdown("- For the **dX** prediction, the **Free Core Nutation (FCN)** x component (xFCN) is calculated, and alongside dX and xEAM they are used to train a model using **KRR** to predict dX. Idem **dY**.")
    st.markdown("- For the **dUT1** prediction, the data is preprocessed by removing the leap seconds. Afterwards, alongside with zEAM, a model is trained using **KRR** to predict this modified dUT1 time series. Lastly, the leap seconds are added back to obtain the final dUT1 prediction.")
    st.image('esquema_eam.png',output_format = 'png', use_container_width = False) 

     
d = datetime.datetime.now().date()

columns = st.columns([0.9,0.1], gap = "small")
with columns[0]: 
    st.write(f'Last updated: {d}')
with columns[1]:
    st.button('Scroll to top', on_click=scroll)

    
     


