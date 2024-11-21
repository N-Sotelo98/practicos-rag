import logging.config
import streamlit as st
from src.controler import Controler
import logging  
import os

# Interfaz grafica de usuario
#Revisamos el status de la base de datos si no existen embeddings en la coleccion incializa el pipeline
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s',filename='operation.log')
logger.info(os.getcwd())

@st.cache_resource
def get_controler():
    return Controler(type='qdrant')

controller=get_controler()
db_status=controller.validar_estado()

if db_status:
  st.title("Reglamentación alimentaria Argentina")

  with st.chat_message('assistant'):
    st.write("Bienvenido a la aplicación de búsqueda de reglamentación alimentaria Argentina")

  if prompt:=st.chat_input("Ingrese su consulta"):
        with st.chat_message('user'):
            st.write(prompt)

        similitud=controller.process_query(prompt)
        with st.chat_message('assistant'):
            for mensaje in similitud:
                st.text(mensaje)
        
    
else:
   controller.init_pipeline()

    






