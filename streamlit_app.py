import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import random

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

departamentos = df_geo['departamento'].unique()
departamentos_seleccionados = st.multiselect('Selecciona los departamentos:', departamentos)

if not departamentos_seleccionados:
    st.write("No se han seleccionado departamentos.")
else:
    df_seleccionado = df_geo[df_geo['departamento'].isin(departamentos_seleccionados)]

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    
    region_geojson[region_geojson.FIRST_NOMB.isin(departamentos_seleccionados)].plot(ax=ax, edgecolor=u'gray', cmap='Pastel1')
    df_seleccionado.plot(ax=ax, color='black', markersize=2)
    st.pyplot(fig)
    
    departamentos_unicos = df_seleccionado['departamento'].unique()
    random.seed(89040)
    colors_bar = {}
    for departamento in departamentos_unicos:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors_bar[departamento] = color
    
    provincias_counts = df_seleccionado['provincia'].value_counts()
    
    fig_bar, ax_bar = plt.subplots()
    provincias_counts.plot(kind='bar', ax=ax_bar, color=[colors_bar[df_seleccionado.loc[df_seleccionado['provincia'] == provincia, 'departamento'].iloc[0]] for provincia in provincias_counts.index])
    ax_bar.set_xlabel('Provincia')
    ax_bar.set_ylabel('Cantidad')
    ax_bar.set_title('Cantidad de Centros de Vacunación por provincia')
    
    legend_handles = []
    for departamento, color in colors_bar.items():
        legend_handles.append(matplotlib.patches.Patch(color=color, label=departamento))
        ax_bar.legend(handles=legend_handles, title="Departamentos")

    st.pyplot(fig_bar)