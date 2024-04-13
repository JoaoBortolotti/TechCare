import pygsheets
import os
import pandas as pd
import numpy as np
import streamlit as st


cred = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")
url ="https://docs.google.com/spreadsheets/d/1lGEHS1j5fN9FL3PpyoQvgJw2h_YBJvZw8UdIeAVkkPM/edit#gid=1746936965"

arquivo = cred.open_by_url(url)
aba = arquivo.worksheet_by_title("FCD674738315")

col_data = aba.get_col(1)
col_hora = aba.get_col(2)
col_temp= aba.get_col(3)
col_hum = aba.get_col(4)
col_cla = aba.get_col(5)

col_data = [data + '/2024' for data in col_data]
data_hora = [pd.to_datetime(data + ' ' + hora) for data, hora in zip(col_data, col_hora)]
col_temp = [float(temp) if temp != '-' else np.nan for temp in col_temp]
col_hum = [float(hum) if hum != '-' else np.nan for hum in col_hum]
col_cla = [float(cla) if cla != '-' else np.nan for cla in col_cla]

df = pd.DataFrame({'DataHora': data_hora, 'Temperatura': col_temp, 'Umidade': col_hum, 'Claridade': col_cla})
df['Data'] = df['DataHora'].dt.date
df['Hora'] = df['DataHora'].dt.hour

df_avg = df.groupby(['Data', 'Hora'])[['Temperatura', 'Umidade', 'Claridade']].mean().reset_index()
df_avg['DataHora'] = pd.to_datetime(df_avg['Data'].astype(str) + ' ' + df_avg['Hora'].astype(str) + ':00')

temp_recente = df['Temperatura'].iloc[-1]
umd_recente = df['Umidade'].iloc[-1]
cla_recente = df['Claridade'].iloc[-1]


st.image('techcare.svg', width=100)


st.title("TechCare - Sistema de Monitoramento de Ambientes ")

st.write("")
st.write("")
st.write("")

df_temp = df.groupby(df['DataHora'].dt.date)['Temperatura'].agg(['first', 'last'])
df_hum = df.groupby(df['DataHora'].dt.date)['Umidade'].agg(['first', 'last'])
df_cla = df.groupby(df['DataHora'].dt.date)['Claridade'].agg(['first', 'last'])

df_temp['Variação'] = ((df_temp['last'] - df_temp['first']) / df_temp['first'] * 100).round(2)
df_hum['Variação'] = ((df_hum['last'] - df_hum['first']) / df_hum['first'] * 100).round(2)
df_cla['Variação'] = ((df_cla['last'] - df_cla['first']) / df_cla['first'] * 100).round(2)

var_temp = df_temp['Variação'].iloc[-1]
var_hum = df_hum['Variação'].iloc[-1]
var_cla = df_cla['Variação'].iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", f"{temp_recente} °C", f"{var_temp} %")
col2.metric("Umidade", f"{umd_recente} ur", f"{var_hum} %")
col3.metric("Claridade", f"{cla_recente} cd", f"{var_cla} %")



st.write("")
st.write("")
st.write("")

st.subheader('Gráfico de Temperatura')
st.line_chart(df_avg.set_index('DataHora')['Temperatura'])

st.write("")

st.subheader('Gráfico de Umidade')
st.line_chart(df_avg.set_index('DataHora')['Umidade'])

st.write("")

st.subheader('Gráfico de Claridade')
st.line_chart(df_avg.set_index('DataHora')['Claridade'])



