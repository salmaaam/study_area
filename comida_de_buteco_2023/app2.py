

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import FloatImage
from streamlit_folium import st_folium

url ='https://raw.githubusercontent.com/Siri2191/study_area/main/comida_de_buteco_2023/comida_de_buteco_2023'

def gera_mapa(df):
    # Criar o mapa
    m = folium.Map(location=[-22.9068, -43.1729], zoom_start=12)

    # Iterar sobre cada bar e adicionar um marcador com as informações
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=folium.Popup('<b>'+row['nome_do_bar']+'</b><br>'+str(row['pratos'])+'<br><img src="'+row['link_da_Imagem']+'" width="100%">',max_width=800),
            icon=folium.Icon(color='red', icon='beer', prefix='fa')
        ).add_to(m)

    # Adicionar imagem de fundo
    FloatImage('https://www.riodejaneiro.com.br/images/home_rj_bg.jpg', bottom=0, left=0).add_to(m)

    # Mostrar o mapa
    return m

# Ler os dados do arquivo CSV
df=pd.read_csv('https://raw.githubusercontent.com/Siri2191/study_area/main/comida_de_buteco_2023/comida_de_buteco_2023',index_col = False)

# Mostrar o mapa no Streamlit
st.markdown('<h1>Mapa do Comida de Buteco 2023</h1>', unsafe_allow_html=True)
st.markdown('<p>O mapa mostra a localização dos bares do comida de buteco 2023</p>', unsafe_allow_html=True)

bairros_unicos = df['bairros']
bairros_selecionados = st.multiselect('Selecione o(s) bairro(s) que desejar', bairros_unicos)

df_filtrado = df[df['bairros'].isin(bairros_selecionados)]
# Gerar o mapa
if len(df_filtrado)>0:  
    mapa = gera_mapa(df_filtrado)
    
else:
    mapa = gera_mapa(df)
    

st_folium(mapa,height=500,width=1000)

if len(df_filtrado)>0:
    st.table(df[['nome_do_bar','endereco','pratos']])
else:
    st.table(df[['nome_do_bar','endereco','pratos']])

st.markdown('<p>Created by Guilherme Irigon</p>',unsafe_allow_html=True)

st.write('<a href="https://www.linkedin.com/in/guilherme-irigon-22a1a458/"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30"></a> Linkedin',unsafe_allow_html=True)
st.write('<a href="https://www.instagram.com/seedzz.digital/"><img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" width="30"></a> Instagram', unsafe_allow_html=True)
