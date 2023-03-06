import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import math
import plotly.express as px

url1='https://raw.githubusercontent.com/Siri2191/study_area/main/streamlit/lisbon_weekdays.csv'
url2='https://raw.githubusercontent.com/Siri2191/study_area/main/streamlit/lisbon_weekends.csv'

@st.cache_data
def load_data():
    df_week = pd.read_csv(url1,index_col=False)
    df_weekend = pd.read_csv(url2,index_col=False)

    rename = {'realSum':'preco',
              'person_capacity':'capacidade',
              'guest_satisfaction_overall':'pontuacao'}
    
    drop = ['room_type','room_shared','room_private','host_is_superhost','multi', 'biz','bedrooms', 'dist',
            'metro_dist', 'attr_index', 'attr_index_norm', 'rest_index','rest_index_norm']
    
    # retira colunas desnecessarias
    df_week.drop(drop,axis=1,inplace=True)
    df_weekend.drop(drop,axis=1,inplace=True)
    
    # renomea as colunas
    df_week.rename(columns=rename,inplace=True)
    df_weekend.rename(columns=rename,inplace=True)

    #cria categoria final e semana
    df_week['cat.semana'] = 'dia de semana'
    df_weekend['cat.semana'] = 'fim de semana'

    df = pd.concat([df_week,df_weekend],ignore_index=True)
    
    return df

# carregando os dados

df = load_data()

#conteudo da barra lateral
st.sidebar.header('Vamos descobrir, me mostre o que você procura?')

# seleção de preço

preco_filter =st.sidebar.slider('Quanto vc tem para gastar por dia? em Euros, hem?!!!',0,2000,(100,600)) 

#seleção de capacidade 

capacidade_filter = st.sidebar.slider('Quantas pessoas são ao total?',1,8,1)

# seleção de data

fds_filter = st.sidebar.multiselect(label='Escolha se é fim de semana ou não', options=['dia de semana','fim de semana'])

# mensagem a quantidade de dado selecionados


df_filtrado = df[(df['preco']>=preco_filter[0]) &(df['preco']<=preco_filter[1]) & (df['capacidade'] == float(capacidade_filter)) & (df['cat.semana'].isin(fds_filter))]

st.sidebar.write('Existem {} imovéis na regiaão com estas caracteristicas'.format(len(df_filtrado)))

#Ao lado da barra de filtro

st.title('Será que existem muitos Arbnb em lisboa? :sunglasses: ')
st.subheader('Quanto maior a barra maior a concentração de imoveis')

st.pydeck_chart(pydeck_obj=pdk.Deck(layers = pdk.Layer("GridLayer",
                                                       df_filtrado,
                                                       fickable=True,
                                                       extruded=True,
                                                       cell_size=50,
                                                       elevation_scale=4,
                                                       get_position=['lng','lat']),
                                    initial_view_state = pdk.ViewState(latitude=38.7,
                                                        longitude=-9.15,
                                                        zoom=11,
                                                        bearing=0,
                                                        pitch=45)
                                    )
                )

st.subheader('Distribuição dos preços dentro da faixa escolhida')

st.plotly_chart( px.histogram(df_filtrado, x="preco", color="cat.semana",
                   marginal="box",
                   hover_data=df.columns).update_layout(xaxis_title='Preço dos Imóveis', yaxis_title='Contagem de imóveis'))


