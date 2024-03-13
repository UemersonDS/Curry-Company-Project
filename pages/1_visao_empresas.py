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
# ou import PIL.Image as imgpil

st.set_page_config (page_title='Visão Empresa', page_icon='📈', layout = 'wide')

# ---------------------------------------------------------------------------
# Funções
# ---------------------------------------------------------------------------

def country_maps(df1):
        
    df_aux = df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    map = folium.Map()

    # desenhando mapa
    
    for index, location_info in df_aux.iterrows(): #iterrows transforma linhas em objetos de interação, encapsulase o datafraqme
            folium.Marker([location_info['Delivery_location_latitude'],
                           location_info['Delivery_location_longitude']],
                           popup = location_info[['City', 'Road_traffic_density']] ).add_to(map)
    folium_static ( map, width = 1024, height = 600 )
    return None
    # Com ou sem return None tanta faz, poderia fazer sem tbm
            
            
            

def order_share_by_week(df1):
        
    # A quantidade de pedidos por entregador(unicos) por semana.
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux1, df_aux2, how='inner', on='week_of_year' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
        
    return fig
        
        
        
        

def order_by_week(df1):
        
    # Criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')
    
    return fig
   




def traffic_order_city(df1):         
    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .count()
                 .reset_index())
                
    fig = px.scatter(df_aux, x='City',y='Road_traffic_density', size='ID', color='City' )

    return fig





            
def traffic_order_share(df1):
                
    df_aux = df1.loc[:,['ID', 'Road_traffic_density' ]].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = 100 * df_aux['ID'] / df_aux['ID'].sum()
            
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density' )
                
    return fig





def order_metric(df1):
            
    # Order Metric
     
    cols = ['ID', 'Order_Date'] # colunas
        
    #seleção de linhas
    df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()

    #Desenhar o gráfico de linhas
  
    fig = px.bar(df_aux, x='Order_Date', y='ID')
     
    
            
    return fig

# Import dataset
df_raw = pd.read_csv( '../dataset/train.csv')

df1 = df_raw.copy()


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
# Import dataset
df_raw = pd.read_csv( '../dataset/train.csv' )


# Limpando os Dados

df = df_raw.copy()

# cleaning dataset

df1 = clean_code (df)



# ==================================================
# Barra Lateral
# ==================================================
st.header( 'Marketplace - Visão Cliente' )

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
    'Quais as condições do trânsito',
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

tab1, tab2, tab3 = st.tabs ( [ 'Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

# clausula = reservada do python
with tab1:
    with st.container():
                # Order Metric
                fig = order_metric(df1)
                st.markdown('# Orders by Day')
                st.plotly_chart(fig,use_container_width=True)
        
        
       
    
    with st.container():
        col1, col2 = st.columns ( 2 )
        with col1:
                fig = traffic_order_share(df1)
                st.header( "Traffic Order Share" )
                st.plotly_chart(fig, use_container_width = True )
                 

            
        with col2:
                st.header( "Traffic Order City" )
                fig = traffic_order_city(df1)
                st.plotly_chart (fig, use_container_width=True )
        
            
        
        
with tab2:
    
    with st.container():
                st.markdown ( "# Order by Week" )
                fig = order_by_week(df1)
                st.plotly_chart (fig, use_container_width=True )
    

    
    
    with st.container():
                st.markdown ( "# Order Share by Week" )
                fig = order_share_by_week(df1)
                st.plotly_chart (fig )
        

        
        
with tab3:
                st.markdown("# Country Maps")
                country_maps(df1)
