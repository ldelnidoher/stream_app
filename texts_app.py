# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 13:11:42 2025

@author: lddelnido
"""


#Banner image
custom_html = """
<div class="banner">
     <img src="https://github.com/ldelnidoher/stream_app/blob/main/logos.png?raw=true" alt="Banner Image">
<style>
     <center>
         .banner {
             width: 100%;
             height: 70px;
             overflow: hidden;
         }
         .banner img {
             width: 100%;
             object-fit: cover;
         }
    </center>
</style>
</div>
"""
# css_tabs = """
# <div class="st-emotion-cache-bfgnao e1g8wfdw0">
# <\button}
# <style>
#     .st-emotion-cache-bfgnao {
#         --scrollbar-width: 0px;
#         text-size-adjust: 100%;
#         -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
#         -webkit-font-smoothing: auto;
#         color-scheme: light;
#         font-weight: normal;
#         line-height: 1.6;
#         white-space: nowrap;
#         cursor: pointer;
#         box-sizing: border-box;
#         scrollbar-width: thin;
#         scrollbar-color: transparent transparent;
#         font-family: "Source Sans", sans-serif;
#         font-size: 1.5rem;
#         color: inherit;
#     }
# <\style>
# <\button>
# <\div>
# """
css_tabs="""
<style>
    .stTabs > .tablist > .react-tabs__tab--selected {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Custom style for all tabs */
    .stTabs > .tablist > .react-tabs__tab {
        background-color: #e8e8e8;
        color: #4f4f4f;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
"""

introduction = """<div style="text-align: justify;">
<h3>
    <b>Welcome to the repository of the VLBI Analysis Center of the University
    of Alicante (UAVAC)</b>
</h3>

In this app you will be able to find:
<ul>
    <li><b>EOP short-term predictions.</b></li>
    <li><b>FCN-CPOs predictions.</b></li>
    <li><b>Downloadable data in different formats and plots.</b></li>
</ul>

  
In the menu option <span style="color: #fb6a00"><i><b>"EOP PREDICTIONS"</b></i></span> you will find different
parameters predictions, with downloadable historic data files in .txt
and .csv and interactive plots.  
In these plots you will be able to zoom in/out, select and especific area,
choose which data to display (by right-clicking the parameter in the plot
legend) and download them as .png. This options are found in the top right
corner of the plot.

In the menu option <span style="color: #fb6a00"><i><b>"PREDICTION MODELS"</b></i></span> you will find diagrams 
and explanations further in depth about the prediction models used. 

In the menu option <span style="color: #fb6a00"><i><b>"ABOUT US"</b></i></span> you will find about the 
institutions involved in this project and contact information.

<i>This app is still under construction, so it might change with time. Thank you
for your understanding.</i>    </div>"""



about_us = """<div style="text-align: justify;">

We are a team of scientists working in collaboration from:
<ul>
    <li>VLBI Analysis Center of the University of Alicante: 
        <a href="https://web.ua.es/en/uavac/">UAVAC</a>
    </li>
    <li>Geodesy Area of the Spanish National Geographic Institute: 
        <a href="https://www.ign.es/web/ign/portal/gds-area-geodesia">IGN Geodesy</a>
    </li>
    <li>Atlantic Network of Space Geodetic Stations:
        <a href="https://raege.eu/">RAEGE</a>
    </li>
</ul>

<i>If you have any questions or suggestions, please write (ES/EN) to
<a href = "mailto:lucia.delnido@ua.es">lucia.delnido@ua.es</a></i>
</div>
"""


pred_short_no = """<div style="text-align: justify;">
<ul>
    <li>For <b>xpol</b> prediction, each component is preprocessed by
        applying <b>Singular Spectrum Analysis (SSA)</b> in order to obtain a 
        reconstructed time series and the residual noise time series. Using the 
        <b>Kernel Ridge Regression (KRR)</b> algorithm, two models are trained: one to 
        predict the reconstructed time series and the other to predict the noise. Both
        predictions are then added to generate the final xpol prediction. Idem <b>ypol</b>.
    </li>  
    <li>For the <b>dX</b> prediction, the <b>Free Core Nutation (FCN)</b> x component (xFCN)
        is calculated, and alongside dX they are used to train a model using <b>KRR</b> 
        to predict dX. Idem <b>dY</b>.  
    </li>
    <li>For the <b>dUT1</b> prediction, the data is preprocessed by removing the leap
        seconds. Afterwards, a model is trained using <b>KRR</b> to predict this modified
        dUT1 time series. Lastly, the leap seconds are added back to obtain the final
        dUT1 prediction. 
    </li> 
    <li>The output returns 1 day only, so there is 11 models (day 0 to day 10) per 
        parameter. For the CPOs results with the <b>NEW</b> title, the algorithm is
        multi-output and returns all 11 days simultaneously.
    </li>
</ul>
</div>
"""


pred_short_si = """<div style="text-align: justify;">
To predict EOP using <b>Effective Angular Momentum</b>
Functions data, we will sum into one variable -called <b>xEAM</b>- the xmass and
xmotion components of Atmospheric Angular Momentum (AAM), Oceanic Angular 
Momentum (OAM) and Hydrological Angular Momentum (HAM). We follow the same 
proceeding with the y and z components to obtain the variables <b>yEAM</b> and 
<b>zEAM</b>. 
<ul>
    <li>For <b>xpol</b> prediction, each component is preprocessed by applying 
        <b>Singular Spectrum Analysis (SSA)</b> in order to obtain a reconstructed time
        series and the residual noise time series. Using this parameters alongside
        xEAM a model is trained using <b>Kernel Ridge Regression (KRR)</b> algorithm 
        to predict xpol. Idem <b>ypol</b>. 
    </li> 
    <li>For the <b>dX</b> prediction, the <b>Free Core Nutation (FCN)</b> x component
        (xFCN) is calculated, and alongside dX and xEAM they are used to train a 
        model using <b>KRR</b> to predict dX. Idem <b>dY</b>.  
    </li>
    <li>For the <b>dUT1</b> prediction, the data is preprocessed by removing the leap
        seconds. Afterwards, alongside with zEAM, a model is trained using <b>KRR</b> to
        predict this modified dUT1 time series. Lastly, the leap seconds are added
        back to obtain the final dUT1 prediction.
    </li>
    <li>The output returns 1 day only, so there is 11 models (day 0 to day 10) per 
        parameter. For the CPOs results with the <b>NEW</b> title, the algorithm is
        multi-output and returns all 11 days simultaneously.
    </li>
</ul>
</div>
"""

ml_intro1 = """
<div style="text-align: justify;">
The prediction of the parameters is calculated using <b>Machine Learning</b> 
algorithms. The prediction horizon extends 10 days into the future, in addition
to the day on which the calculations are conducted, referred to as Day 0.
"""

ml_intro2 = """<div style="text-align: justify;">
<a href="https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html">IERS EOP 20 C04 (*), IERS finals.all</a> and
<a href="http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=e0fff81f-dcae-469e-8e0a-eb10caf2975b">GFZ Effective Angular Momentum Functions</a>
are employed as input data.(*) On 5 June 2025 the series IERS EOP 20 C04 was 
discontinued and ever since <b>IERS EOP 20u23 C04<\b> is used as input.
Two predictive models are applied. <b>w/o EAM</b> utilises only EOP data as input 
whereas <b>w/ EAM</b> includes both EOP data and Effective Angular Momentum data.
</div>
"""

ml_historical = """<div style="text-align: justify;">
Here we present a compilation of all the predictions, calculated every 
Wednesday, in a single file. As two different prediction models are used, two 
separate files are provided.
</div>
"""

fcn_intro = """<div style="text-align: justify;">
Here we present the <b>FCN-CPOs</b> solutions that we obtained in the FCN_CPO
model, alongside the IERS 20u23 C04 CPOs solutions for comparison.
The methodology and details about this model can be found in the following 
paper: <a href="https://www.sciencedirect.com/science/article/pii/S0264370715300120">Belda, S., Ferrándiz J.M., Heinkelmann R., Nilsson T. and Schuh H. (2016).
        <i>Testing a new Free Core Nutation empirical model (2016)</i></a>

This data gets updated bi-monthly
"""


fcn_help_plot = """
In order not to potentially freeze the app, it is advised to select less than
 10 years of data. Nevertheless it is possible to load all 60+ years.
"""
