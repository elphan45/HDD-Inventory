import streamlit as st 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from numpy import random
from scipy import stats

st.title ('IT Upgradation 2024')
st.subheader('Fachgebiet: SYS')
#st.page_link("https://www.zsw-bw.de/ueber-uns/fachgebiete.html", label="ZSW Team Structure")

# Step 1: Uploading the CSV file
uploaded_file = st.file_uploader('Please upload the CSV file with your inventory list', type='csv')
if uploaded_file is not None:
    st.markdown('## File uploaded')
    st.write('\n Pre Processing...')
    df = pd.read_csv(uploaded_file, delimiter=';', decimal=',')
    st.dataframe(df) #used to display dataframes as interactive tables in Streamlit apps.

# Step 2: Calculate the number of HDDs of each type and size
    st.subheader('HDD Summary')
    if 'Type' in df.columns and 'Size (TB)' in df.columns:
        hdd_summary = df.groupby(['Type', 'Size (TB)']).size().reset_index(name='Count')
        st.dataframe(hdd_summary)
    else:
        print('Sorry please re-upload corrected CSV file containing datatype and size.')

# Step 3: User input for power consumption of each HDD type
st.subheader('HDD Power Consumption')
power_consumption= {}
for i in df['Type'].unique(): 
    power_consumption[i]= st.number_input(f"Power consumption for {i} W",min_value=0.0, step=0.1)

#unique function will eliminate any repeating ones. 
#If you don’t use the unique() function, the loop will iterate over every row in the dataframe, creating an input field for each HDD type in every row. 
# This means if you have multiple rows with the same HDD type, you’ll end up creating multiple input fields for that type,
# which is unnecessary and confusing for the user.

#st.table(df): is used to display static tables. This means the table’s contents are laid out directly on the page without any interactive features.
# Basic Use: It’s ideal for simple, non-interactive data presentations where you don’t need sorting, filtering, or other interactive capabilities.

# Step 4: Calculate total power consumption for a whole year (assuming 24/7 usage)
st.subheader('Annual Power Consumption')
df['Power consumption (W)'] = df['Type'].map(power_consumption)
df['Annual Consumption (kWh)'] =  df['Power consumption (W)'] * 24 * 365 / 1000  # Convert to kWh
total_annual_consumption = df['Annual Consumption (kWh)'].sum() #
st.write(f"Total annual power consumption: {total_annual_consumption:.2f} kWh")

# Step 5: User input for modernization scenario
st.subheader('Modernization Scenario')
modernized_hdds={}
for i in df['Type'].unique():
    modernized_hdds[i]=st.number_input(f"Number of {i} HDDs to modernize", min_value=0, max_value=int(df[df['Type'] == i].shape[0]), step=1)

# Step 6: Calculate power and CO2 savings
st.subheader('Power and CO_2 Savings')
co2_factor = st.number_input('Enter the co__2 emission factor (kg co2 per kwh)', min_value=0.0, value=0.5, step =0.01)
saved_power = 0
for i, count in modernized_hdds.items():
    if count>0:
        # Assuming the modernized HDDs use 30% less power
        old_power = power_consumption[i] * count * 24 * 365 / 1000  # Annual power of old HDDs
        new_power = old_power * 0.7  # Modernized HDDs use 30% less power
        saved_power += (old_power - new_power)

saved_co2 = saved_power * co2_factor
st.write(f"Total power saved: {saved_power:.2f} kWh")
st.write(f"Total CO2 saved: {saved_co2:.2f} kg")