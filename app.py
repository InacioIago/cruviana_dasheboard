import streamlit as st
import pandas as pd
from api.service import get_data
import folium
from streamlit_folium import st_folium

st.image('img/ifpi.png', width=255)
st.title('Cruviana Dashboard')
st.subheader('Estação Meteorológica: UAPP IFPI Oeiras')
st.write('---')
st.header("Leituras")
data = st.date_input('Data')

def load_data():
    df = pd.DataFrame(get_data(data))

    df = df.drop(columns=['Data_add', 'Data',
                          'WindSpeed', 'WindSpeed10Min',
                          'RainRate', 'ETMonth',
                          'RainStorm', 'Station'])

    df = df.set_index('id')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Datetime'] = df['Datetime'].dt.strftime('%d/%m/%y %H:%M')


    return df

leituras = load_data()
st.write(leituras)
st.write('---')
st.subheader('Temperatura')
st.line_chart(data=leituras, x='Datetime', y='TempOut', color='#F00')
st.write(f'Temperatura Mínima: {leituras.TempOut.min()} °C')
st.write(f'Temperatura Máxima: {leituras.TempOut.max()} °C')
st.write('---')  
st.subheader('Precipitações')
st.line_chart(data=leituras, x='Datetime', y='RainDay')
st.write(f'Volume Total acumulado: {leituras.RainDay.max()} mm')
st.write('---')
st.subheader('Localização')
m = folium.Map(location=[-7.000100013292593, -42.100894125125826],
               zoom_start=16
)
folium.Marker(
    [-7.000100013292593, -42.100894125125826],
    popup='Estação Meteorológica UAPP - IFPI',
    tooltip='Estação Meteorológica UAPP - IFPI'
).add_to(m)

mapa = st_folium(m, width=700)

st.write('---')
st.subheader('Umidade')
st.line_chart(data=leituras, x='Datetime', y='HumOut', color='#ffaa0088')
st.write(f'Umidade Mínima: {leituras.HumOut.min()} %')
st.write(f'Umidade Máxima: {leituras.HumOut.max()} %')
st.write('---')
st.subheader('Radiação Solar')
st.line_chart(data=leituras, x='Datetime', y='SolarRad', color='#F999')
st.write(f'Radiação Solar Mínima: {leituras.SolarRad.min()} W/m²')
st.write(f'Radiação Solar Máxima: {leituras.SolarRad.max()} W/m²')