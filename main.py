import streamlit as st
import pandas as pd
from pathlib import Path
import json
import io
import csv
from re import search
from standard_names import standard_amanat_names_ordered, standard_region_names_ordered
from regions_geo import regions_geo

expected_region_names = ['Ryad', 'Riyadh', 'الرياض', 'Al Riyadh']


st.set_page_config(layout="wide")
header = st.container()
input_box = st.container()
output_box = st.container()


with header:
    st.title('Data Manipulation App')
   
with input_box:
    st.header('insert csv and geojson files')
    
    # st.text(regions_geo[1]["REGIONCODE"])

    # file upploading
    uploaded_csv_file = st.file_uploader('csv', key='csv')

    # dropdown menu for the division type
    division_type = st.selectbox('Division Type', [
                                 'choose division type', 'Manateq', 'Baladeyat', 'Mohafazat', 'Amanat', 'Netaq el ishraf al edary lel modn'])
    # Manateq , Amanat etc
    foriegn_key_type = st.selectbox('Foriegn key Type', [
        'choose arranging type', 'REGIONNAME', 'REGIONCODE'])
    type_lang = st.selectbox('Type Language', ['Language', 'EN', 'AR'])

    # uploaded_geojson_file = st.file_uploader('Geojson', key='geojson')
    file_name = st.text_input('')
    st.caption('Please insert your output file name')

    st.subheader('csv data uploaded')
    if uploaded_csv_file is not None:
        data = uploaded_csv_file.getvalue().decode("utf-8")
        # read data from csv file
        csv_dataFrame = pd.read_csv(io.StringIO(data), sep=',')
        # remove object_id column from csv data frame
        csv_dataFrame.pop('OBJECTID')
        # save the dataframe as a python dict
        csv_dataFrame_as_dict = csv_dataFrame.to_dict('records')

        #* Function to merge two dict
        def Merge(dict1, dict2):
            res = {**dict1, **dict2}
            return res
        
        # get the geometry data from region_geo.py file 
        #! make region code generic as we get the geometry based on it 
        geometry = regions_geo[1]
        
        my_dict = {}
        #! will it always be "type" = "Feature" or should I make it generic?
        my_dict.update(type="Feature") 
        my_dict.update(properties=csv_dataFrame_as_dict[0]) 
        #* Merge the properties with the geometry
        #! will this key always be called properties? 
        total = Merge(my_dict, geometry)
        

        for x in csv_dataFrame_as_dict:
            for y in expected_region_names:
                if search(y.lower(), x[f'{foriegn_key_type}_{type_lang}'].lower()):
                    x.update(REGIONNAME_EN=standard_region_names_ordered[x["REGIONCODE"]])
                    st.text(x)
        st.text(csv_dataFrame_as_dict)
        
        if file_name is not None:
            f = open("output.geojson", "w" , encoding="utf-8")
            json.dump(total, f, ensure_ascii=False)
            f.close()


with output_box:
    st.button('Generate', on_click='')
