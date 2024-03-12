# Libraries
from haversine import haversine

import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static

# Bibliotecas necessárias
import pandas as pd
import re
import streamlit as st
from PIL import Image
import folium
import numpy as np
# ou import PIL.Image as imgpil




# Import dataset
df_raw = pd.read_csv( 'train.csv')

df1 = df_raw.copy()


# Limpando os Dadojj

st.set_page_config (page_title='Visão Entregadores', page_icon='🚚', layout = 'wide')

# --------------------------------------------------------------
# Funções
# --------------------------------------------------------------


def top_delivers(df1, top_asc): 
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby( ['City', 'Delivery_person_ID'] )
              .mean()
              .sort_values(['City', 'Time_taken(min)'],ascending = top_asc).reset_index())
                
    # selecionado linhas 
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    # Concatenar
    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index(drop=True)
                
    return df3

# Limpando os Dados

def clean_code(df1):
    """""
        Está função tem a responsabilidade de limpar o DATAFRAME
        
        Tipos de limpezas:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texxto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo ( Remoção dos texto da variavel númerica )
        
        Input: Dataframe
        Output: Dataframe
    
    """""
    
    # 1. Convertendo a coluna Age de texto para número
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


    # 1.1. Revomendo os 'NaN' da coluna = 'Road_traffic_density'
    linhas_selecionadas = (df['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 1.2. Revomendo os 'NaN' da coluna = 'City'
    linhas_selecionadas = (df['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 1.3. Revomendo os 'NaN' da coluna = 'festival'
    linhas_selecionadas = (df['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 2. Convertendo a coluna Ratigs de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. Convertendo a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    # 4. Convertendo multiple deliveries de texto para numero inteiro (int)
    linhas_selecionadas1 = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas1, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 5. Removendo os espaços dentro de strings/texto/object
    #df = df.reset_index ( drop = True )
    #for i in range (len(df)):
    #  df.loc[i, 'ID'] =  df.loc[i, 'ID'].strip()

    # 6. Removendo os espaços dentro de strings/texto/object
    df1.loc[:, 'ID'] =  df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] =  df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] =  df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] =  df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] =  df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] =  df1.loc[:, 'Festival'].str.strip()
    # Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] ) #apply == quero aplicar uma função a todos 
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    #lambda de x: da o acesso ao x, e o x é o valor de linha - representa a linha

    return df1

# -------------------------------------------------- Inicio da estrutura logica do código ---------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
df_raw = pd.read_csv(  'dataset/train.csv' )


# Limpando os Dados

df = df_raw.copy()

# cleaning dataset
df1 = clean_code (df)


# ==================================================
# Barra Lateral
# ==================================================


st.header( 'Marketplace - Visão Entregadores' )

# image_path = '\Users\uemer\Repos\FTC\CICLO_5\logo.png'
#image_path = 'logo.png'
image = Image.open ( 'logo.png' )
st.sidebar.image ( image, width=120 )

st.sidebar.markdown ( '# Cury Company' )
st.sidebar.markdown ( '## Fastest Delivery in Tow' )
st.sidebar.markdown ( """___""" )

st.sidebar.markdown( '## Selecione uma data limite' )
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime( 2022, 2, 11 ),
    max_value=pd.datetime ( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown ( """___""" )


traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )

climate_options = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'] )

st.sidebar.markdown ( """___""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin ( traffic_options ) # isin == esta em 
df1 = df1.loc[linhas_selecionadas, :]

#filtro de clima
linhas_selecionadas = df1['Weatherconditions'].isin ( climate_options ) # isin == esta em 
df1 = df1.loc[linhas_selecionadas, :]


# ==================================================
# Layout no Streamlit
# ==================================================

tab1, tab2, tab3 = st.tabs ( [ 'Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
            st.title( 'Overall Metrics' )
            
            col1, col2, col3, col4 = st.columns ( 4, gap='large' )
            with col1:
                #  A Maior idade dos entregadores.
                maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
                col1.metric( 'Maior idade', maior_idade )

                
            with col2:
                #  A Menor idade dos entregadores.
                menor_idade =df1.loc[:, 'Delivery_person_Age'].min()
                col2.metric( 'Menor idade', menor_idade )
                
            with col3:
                 # A melhor condição de veículos.
                 melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
                 col3.metric( 'Melhor condicao', melhor_condicao )
                    
            with col4:
                 # A pior condição de veículos.
                 pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
                 col4.metric( 'Pior condicao', pior_condicao )
                
                
    with st.container():
        st.markdown("""___""")
        st.title ( 'Avaliacoes' )
        
        col1, col2= st.columns ( 2 )
        with col1:
            st.markdown( '##### Avaliacao media por entregador' )
            df_avg_ratings_per_deliver = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe ( df_avg_ratings_per_deliver )
            
            
            
        with col2:
            st.markdown( '##### Avaliacao media por transito' )
            df_avl = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg( {'Delivery_person_Ratings': ['mean','std']} ) )
            
            #Mudança de nome das colunas
            df_avl.columns = (['delivery_mean', 'delivery_std'])
            
            # reset do index
            df_avl = df_avl.reset_index()
            st.dataframe( df_avl )
            
            
            st.markdown( '##### Avaliacao media por clima' )
            df_avl = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                         .groupby('Weatherconditions')
                         .agg( {'Delivery_person_Ratings': ['mean','std']} ) )
            
            # Mudança de nome das colunas
            df_avl.columns = (['Weather_mean', 'Weather_std'])
            
            # reset do index
            df_avl = df_avl.reset_index()
            st.dataframe( df_avl )

            
    with st.container():
        st.markdown("""___""")
        st.title ( 'Velocidade de Entrega' )
        
        col1, col2= st.columns ( 2 )
        with col1:
            st.markdown( '##### Top entregadores mais rapidos' )
            # Os 10 entregadores mais rapidos por cidade.
            df3 = top_delivers(df1, top_asc=True )
            st.dataframe( df3 )
            
            
            
        with col2:
            st.markdown( '##### Top entregadores mais lentos' )
            # Os 10 entregadores mais lentos por cidade.
            df3 = top_delivers(df1, top_asc=False )
            st.dataframe( df3 ) #mostrar no streamlit / exibir na página q estámos criando
            
            