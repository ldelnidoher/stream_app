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
text2 = '[IERS EOP 20 C04](https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html) and [GFZ Effective Angular Momentum Functions](http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=e0fff81f-dcae-469e-8e0a-eb10caf2975b) are employed as input data.'
text3 = 'Two predictive models are applied. **w/o EAM** utilises only EOP data as input whereas **w/ EAM** includes both EOP data and Effective Angular Momentum data.'


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
        dates = dff['pub_date'].values
        year = [s[:4] for s in dates]
        month = [m[5:7] for m in dates]
        day = [d[8:10] for d in dates]
        
        dff.insert(0, column = 'year', value = year)
        dff.insert(1, column = 'month', value = month)
        dff.insert(2, column = 'day', value = day)
         
        #Filter the files for the user
        st.header('Short-term EOP predictions: 10 days')
        st.write(text1)
        st.markdown(text2) 
        st.divider() 
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
        st.subheader(f'Predictions for {selected:}')
        st.write(text3) 
    
         
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

        #Visualization of the predictions for the chosen epoch in a table format
        df = pd.DataFrame({'Date [YY-MM-DD]':dates_fmt,'Epoch [MJD]':epochs, f'w/o EAM [{txt}]':conv1, f'w/ EAM [{txt}]':conv2}, index = (['Day'+str(v) for v in range(11)]))
        styles = [dict(selector="", props=[('border','2px solid #fb9a5a')]), dict(selector="th", props=[("background-color","#b2d6fb"),('color','black')])] 
        s = df.style.set_table_styles(styles)
        st.table(s)

        #Creating .txt and .csv files with the predictions for the chosen epoch
        l = len(txt)
        if l<3:
            txt = txt+']'+(' '*(2-l))
        else:
            txt = txt+']'
        np.savetxt('param.txt',df, fmt = ['% s','%5d',f'{fm}',f'{fm}'], delimiter='   \t', header = f'  Date [YY-MM-DD]  |  Epoch[MJD]  |  w/o EAM [{txt}  |    w/EAM  [{txt}')
        f = open('param.txt','r') 
        lista =f.read()
        f.close()

        if selected == 'UT1-UTC':
             string = 'dut1'
        else:
             string = selected
             
        col1,col2 = st.columns([0.2,0.8],gap = 'small')
        with col1:
             st.download_button(label =':arrow_heading_down: Save data as .txt :arrow_heading_down:', file_name = f'{string}_{epochs[0]}.txt', data = lista)
        with col2:
             st.download_button(label =':arrow_heading_down: Save data as .csv :arrow_heading_down:', file_name = f'{string}_{epochs[0]}.csv', data = df.to_csv(index = False))
         
        #Visualization of the chosen data in an interactive plot 
        fig = go.Figure()
        for j in range(1,3):
             fig.add_trace(go.Scatter(
                 x = df['Epoch [MJD]'],y = df[df.columns[-j]],
                 mode = 'lines+markers', marker = dict(size = 5), line = dict(width = 1.5),name = df.columns[-j]))
         
        fig.update_layout(legend_title_text = "Models")
        fig.update_xaxes(title_text="MJD")
        fig.update_yaxes(title_text=f"{txt}")
        
        st.plotly_chart(fig, use_container_width=True)
        st.divider()  
        
        
        #Construction of historic data
        df_hist_no = pd.DataFrame(data = [], columns = ['pub_date','xp','yp','dt','dx','dy'])
        df_no = df2[df2['type_EAM'] == 0].sort_values('pub_date')
        df_hist_no.pub_date = df_no.pub_date
        df_hist_no.xp = df_no['values']
        
        df_hist_si = pd.DataFrame(data = [], columns = ['pub_date','xp','yp','dt','dx','dy'])
        df_si = df2[df2['type_EAM'] == 1].sort_values('pub_date')
        df_hist_si.pub_date = df_si.pub_date
        df_hist_si.xp = df_si['values']
        
        for item in ['yp','dx','dy','dt']:
            df_aux = dff[dff['param']==item]
            
            df_no = df_aux[df_aux['type_EAM'] == 0].sort_values('pub_date')
            df_hist_no[item] = df_no['values'].values
            
            df_si = df_aux[df_aux['type_EAM'] == 1].sort_values('pub_date')
            df_hist_si[item] = df_si['values'].values
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
    st.button('Scroll to top', on_click=scroll, type = 'secondary' )

    
     


