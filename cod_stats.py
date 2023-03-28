import streamlit as st
import pandas as pd
import numpy as np
import codecs
import plotly.express as px

st.set_page_config(page_title="Call of Duty Skills",
                   page_icon="icon.png")
st.image("banner.png")

DATE_COLUMN = 'started_at'
name_link =codecs.open('cod.csv')

st.title('Ranking de las estadísticas de juego de los mejores jugadores de Call of Duty: Modern Warfare')
st.header('Autor: Luis David Cocotle Yáñez')
st.header('Matrícula: S20006746')

st.sidebar.image("icon.png")
st.sidebar.markdown("##")
sidebar= st.sidebar

@st.cache_data
def load_data(nrows):
    name_link = codecs.open('cod.csv',)
    data = pd.read_csv(name_link, nrows=nrows)
    return data

def filtro_jugador(Jugador):
    jugador_filt = data[data['Jugador'].str.upper().str.contains(Jugador)]
    return jugador_filt

data_load_state = st.text('Cargando datos...')
data = load_data(100)
data_load_state.text('Datos cargados')

agree=sidebar.checkbox("Mostrar todos los jugadores")
if agree:
    st.header("Todos los jugadores")
    st.dataframe(data)

nombreJugador = st.sidebar.text_input('Nombre del jugador:')
botonBuscar = st.sidebar.button('Buscar jugador')

if (botonBuscar):
   jugador = filtro_jugador(nombreJugador.upper())
   count_row = jugador.shape[0]
   st.header("Jugadores")
   st.write(f"Total de jugadores mostrados: {count_row}")
   st.write(jugador)

agreeHistogram=sidebar.checkbox("Mostrar histograma")
fig_wins = px.histogram(data,
                   x="wins",
                   title="Numero de victorias por jugador",
                   labels=dict(Victorias="Numero de victorias por jugador"),
                   color_discrete_sequence=["#634a71"],
                   template="plotly_white"
                   )
fig_wins.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.header("Histograma de victorias")
st.plotly_chart(fig_wins)
st.write("Se muestra el número de victorias que han conseguido los jugadores (algunos datos están en cero por que los usuarios decidieron poner en privado algunos datos)")

agreeBar=sidebar.checkbox("Mostrar gráfica de barras")
killcountBytitle=(
    data.groupby(by=['kills']).count()
    )
fig_kill=px.bar(killcountBytitle,
                x=killcountBytitle.index,
                y='Jugador',
                title="Cantidad de jugadores que han causado ese número de bajas",
                labels=dict(Title="Cantidad de bajas",Source="kills",),
                color_discrete_sequence=["#f86749"],
                template="plotly_white")
fig_kill.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.header("Gráfica de barras")
st.plotly_chart(fig_kill)
st.write("Cantidad de bajas causadas por jugador")

agreeScatter=sidebar.checkbox("Mostrar gráfica de baja/muerte")
if agreeScatter:
    kdRatio=data['kdRatio']
    jugador=data['Jugador']
    fig_scatter=px.scatter(data,
                             x=jugador,
                             y=kdRatio,
                             labels=dict(kdRatio='K/D',jugador="Jugador"),
                             title="Baja/muerte por jugador",
                             template="plotly_white")
    fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.header("Gráfica de Scatter")
    st.plotly_chart(fig_scatter)
    st.write("Se muestra el promedio de Baja/muerte de los jugadores")
    
#Se espera agregar más funcionalidades