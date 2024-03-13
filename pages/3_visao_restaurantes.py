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

st.set_page_config (page_title='Visão Restaurantes', page_icon='🍽️', layout = 'wide')


# --------------------------------------------------------------
# Funções
# --------------------------------------------------------------
# Import dataset
df_raw = pd.read_csv( 'train.csv')

df1 = df_raw.copy()

# Funções


def avg_std_time_on_traffic(df1):
    df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .agg( {'Time_taken(min)': ['mean', 'std']} ))
            
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', 
                      color='std_time', color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(df_aux['std_time']))
               
    return fig

    
    
    

def avg_std_time_graph(df1):
                
        df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)': ['mean', 'std'] } )
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
            
        fig = go.Figure()
        fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
        fig.update_layout(barmode='group')
    
        return fig


def avg_std_time_delivery(df1, festival, op):
    """ 
        Esta função calcula o tempo médio e desvio padrão do tempo de entrega.
        Parâmetros:
           input:
             -df: Dataframe com os dados necessários para o cálculo
             - op: Tipo de operção que precisa ser calculado.
                    'avg_time: Calcula o tempo médio.
                    'std_time': Calcula o desvio padrão do tempo.
                           
           output:
             -df: Dataframe com 2 colunas e 1 linha.
                        
    """                
                
    df_aux = df1.loc[:, ['Festival', 'Time_taken(min)']].groupby('Festival').agg( {'Time_taken(min)': ['mean', 'std']} )
 
    df_aux.columns = ['avg_time', 'std_time']

    df_aux = df_aux.reset_index()

    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)
                
    return df_aux



def distance(df1, fig):
       if fig == False:         
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x: 
                                        haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis = 1 )
            
            avg_distance = np.round( df1['distance'].mean(),2)
            # avg_distance = round(df1['distance'].mean(),2) posso fazer assim par não da um numero grande ou no jeito apresentado no print
            #laibol nome escrirto como str 
            # {:.2f} pegue todos os valores antes do ponto pra mim, mas depois do ponto so quero 2 
            return avg_distance
       
       else:
        
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x: 
                                         haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                         (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis = 1 )
            
            avg_distance = df1.loc[:, ['City' , 'distance']].groupby('City').mean().reset_index()
            fig = go.Figure( data=[go.Pie( labels = avg_distance['City'], values =  avg_distance['distance'], pull=[0, 0.1, 0])])
        
            return fig
        


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
df_raw = pd.read_csv(  '../dataset/train.csv' )


# Limpando os Dados

df = df_raw.copy()

# cleaning dataset
df1 = clean_code (df)


# ==================================================
# Barra Lateral
# ==================================================


st.header( 'Marketplace - Visão Restaurantes' )

# image_path = '\Users\uemer\Repos\FTC\CICLO_5\logo.png'
#image_path = 'logo.png'
image = Image.open ( 'logo.png' )
st.sidebar.image ( image, width=120 )


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
        st.title( "Overal Metrics")
        
        col1, col2, col3, col4, col5, col6 = st.columns ( 6 )
        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique()) #st.dataframe ( df_avg_ratings_per_deliver ) // col4.metric( 'Pior condicao', pior_condicao )
            col1.metric( 'Entregadores', delivery_unique )
            
            
        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric( 'A distancia Media', avg_distance) #laibol nome escrirto como str
                
       
    
    
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.metric('Tempo médio', df_aux)
            
            
            


            
        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
            col4.metric('STD Entrega', df_aux)
            
            
                        
            
            
        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.metric('Tempo médio', df_aux)

            
            
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.metric('STD Entrega', df_aux)

            
            
            
        
    with st.container():
        st.markdown("""___""")
        
        col1, col2 = st.columns ( 2 )
        
        with col1:
                st.title ('Tempo Medio de entrega, por cidade')
                fig = avg_std_time_graph(df1)
                st.plotly_chart(fig, use_container_width=True)
            
            
        
        with col2:
            st.title ('Distribuição da Distancia')
            df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                         .groupby(['City', 'Type_of_order'])
                         .agg( {'Time_taken(min)': ['mean', 'std']} ) )
            
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe( df_aux, use_container_width=True)
            
        
            
        

        
        
        
        
    with st.container():
        st.markdown("""___""")
        st.title( "Distrubuição do tempo")
        
        col1, col2 = st.columns ( 2 )
        
        with col1:
            fig = distance(df1, fig=True)              
            st.plotly_chart(fig, use_container_width=True)
                    
                
                
                
        with col2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart( fig, use_container_width=True)
            
                  
        
        
    
    
                                                                 

