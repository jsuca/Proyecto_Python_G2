import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

@st.cache_data
def load_data_vacunacion(url_vacunacion, url_ubigeo):
  df = pd.read_csv(url_vacunacion, delimiter=';')
  df_ubigeo = pd.read_csv(url_ubigeo, delimiter=';')
  df = df[df['longitud'] != 0]
  df = pd.merge(df, df_ubigeo, how="left", on=["id_ubigeo", "id_ubigeo"])
  df = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitud_x, df.latitud_x))
  return df

@st.cache_data
def load_data_geoperu(url):
  df = gpd.read_file(url)
  return df

region_geojson = load_data_geoperu("peru_provincial_simple.geojson")
df_geo = load_data_vacunacion("TB_CENTRO_VACUNACION.csv", "TB_UBIGEOS.csv")

st.title('Centros de Vacunación de COVID 19')

option = st.selectbox('Elegir departamento:', ('APURIMAC', 'HUANCAVELICA', 'CUSCO', 'ANCASH', 'LORETO', 'HUANUCO',
       'AREQUIPA', 'LA LIBERTAD', 'UCAYALI', 'PIURA', 'PUNO', 'AMAZONAS',
       'LIMA', 'SAN MARTIN', 'CAJAMARCA', 'CALLAO', 'TACNA', 'AYACUCHO',
       'JUNIN', 'LAMBAYEQUE', 'ICA', 'TUMBES', 'PASCO', 'MOQUEGUA',
       'MADRE DE DIOS'))

st.write('Departamento seleccionado:', option)

fig, ax = plt.subplots(figsize = (10,8))
region_geojson[region_geojson.FIRST_NOMB == option].plot(ax = ax, edgecolor=u'gray', cmap='Pastel1')
df_geo[df_geo['departamento'] == option].plot(ax = ax, color = 'black', markersize=2)

st.pyplot(fig)
