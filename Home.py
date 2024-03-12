import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🎲"
)

#image_path = '/Users/uemer/Repos/FTC/CICLO_5/'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown ( '# Cury Company' )
st.sidebar.markdown ( '## Fastest Delivery in Tow' )
st.sidebar.markdown ( """___""" )

st.write ("# Curry Company Growth Dashbarding")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
      - Visão Gerencial: Métricas gerais de comportamento.
      - Visão Tática: Indicadores semanais de crescimento.
      - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
      - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
      - Indicadores semanais de crescimento dos restaurantes
    ### Ask for  help
    - Time de Data Science no Discord
    - @meigarom
""" )