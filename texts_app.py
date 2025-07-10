# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 13:11:42 2025

@author: lddelnido
"""


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


introduction = """
### **Welcome to the repository of the VLBI Analysis Center of the University of Alicante (UAVAC)**

In this app you will be able to find:
- **EOP short-term predictions.**
- **FCN-CPOs predictions.**
- **Downloadable data in different formats and plots.**
    
In the menu option :orange[***"EOP PREDICTIONS"***] you will find different
 parameters predictions, with downloadable historic data files in .txt
 and .csv. and interactive plots.  
In this plots you will be able to zoom in/out, select and especific area,
 choose which data to display (by right-clicking the parameter in the plot
                               legend) and download them as .png. This options 
are found in the top right corner of the plot.

In the menu option :orange[***"PREDICTION MODELS"***] you will find diagrams 
and explanations further in depth about the prediction models used. 

In the menu option :orange[***"ABOUT US"***] you will find about the 
institutions involved in this project and contact information.

*This app is still under construction, so it might change with time. Thank you
 for your understanding.*    """



about_us = """
We are a team of scientists working in collaboration from:
- VLBI Analysis Center of the University of Alicante: 
 [UAVAC](https://web.ua.es/en/uavac/)
- Geodesy Area of the Spanish National Geographic Institute: 
 [IGN Geodesy](https://www.ign.es/web/ign/portal/gds-area-geodesia)
- Atlantic Network of Space Geodetic Stations:
 [RAEGE](https://raege.eu/)

*If you have any questions or suggestions, please write (ES/EN) to lucia.delnido@ua.es*
"""


pred_short_no = """- For **xpol** prediction, each component is preprocessed by
 applying **Singular Spectrum Analysis (SSA)** in order to obtain a 
 reconstructed time series and the residual noise time series. Using the 
 **Kernel Ridge Regression (KRR)** algorithm, two models are trained: one to 
 predict the reconstructed time series and the other to predict the noise. Both
 predictions are then added to generate the final xpol prediction. Idem **ypol**.  
- For the **dX** prediction, the **Free Core Nutation (FCN)** x component (xFCN)
 is calculated, and alongside dX they are used to train a model using **KRR** 
 to predict dX. Idem **dY**.    
- For the **dUT1** prediction, the data is preprocessed by removing the leap
 seconds. Afterwards, a model s trained using **KRR** to predict this modified
 dUT1 time series. Lastly, the leap seconds are added back to obtain the final
 dUT1 prediction.  
"""


pred_short_si = """To predict EOP using **Effective Angular Momentum**
 Functions data, we will sum into one variable -called **xEAM**- the xmass and
 xmotion components of Atmospheric Angular Momentum (AAM), Oceanic Angular 
 Momentum (OAM) and Hydrological Angular Momentum (HAM). We follow the same 
 proceeding with the y and z components to obtain the variables **yEAM** and 
 **zEAM**.  
- For **xpol** prediction, each component is preprocessed by applying 
**Singular Spectrum Analysis (SSA)** in order to obtain a reconstructed time
 series and the residual noise time series. Using this parameters alongside
 xEAM a model is trained using **Kernel Ridge Regression (KRR)** algorithm 
 to predict xpol. Idem **ypol**.  
- For the **dX** prediction, the **Free Core Nutation (FCN)** x component
 (xFCN) is calculated, and alongside dX and xEAM they are used to train a 
 model using **KRR** to predict dX. Idem **dY**.  
- For the **dUT1** prediction, the data is preprocessed by removing the leap
 seconds. Afterwards, alongside with zEAM, a model is trained using **KRR** to
 predict this modified dUT1 time series. Lastly, the leap seconds are added
 back to obtain the final dUT1 prediction.")
"""

ml_intro1 = """
The prediction of the parameters is calculated using **Machine Learning** 
algorithms. The prediction horizon extends 10 days into the future, in addition
 to the day on which the calculations are conducted, referred to as Day 0.
"""

ml_intro2 = """
[IERS EOP 20 C04, IERS finals.all](https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html) and
 [GFZ Effective Angular Momentum Functions](http://rz-vm115.gfz-potsdam.de:8080/repository/entry/show?entryid=e0fff81f-dcae-469e-8e0a-eb10caf2975b)
 are employed as input data. On 5 June 2025 the series IERS EOP 20 C04 was 
 discontinued and ever since IERS EOP 20u23 C04 is used as input.
Two predictive models are applied. **w/o EAM** utilises only EOP data as input 
whereas **w/ EAM** includes both EOP data and Effective Angular Momentum data.'
"""

ml_historical = """
Here we present a compilation of all the predictions, calculated every 
Wednesday, in a single file. As two different prediction models are used, two 
separate files are provided.
"""

fcn_intro = """
Here we present the **FCN-CPOs** solutions that we obtained in the FCN_CPO
 model, alongside the IERS 20u23 C04 CPOs solutions for comparison.
The methodology and details about this model can be found in the following 
paper: [Belda, S., Ferrándiz J.M., Heinkelmann R., Nilsson T. and Schuh H. (2016).
        *Testing a new Free Core Nutation empirical model (2016)*](doi:10.1016/j.jog.2016.02.002)

This data gets updated bi-monthly
"""


fcn_help_plot = """
In order not to potentially freeze the app, it is advised to select less than
 10 years of data. Nevertheless it is possible to load all 60+ years.
"""