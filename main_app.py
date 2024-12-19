import logging.config
import streamlit as st
from src.controler import Controler
import logging  
import os

logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s',filename='operation.log')
logger.info(os.getcwd())

@st.cache_resource
def get_controler():
    controller=Controler(type='qdrant')
    controller.init_pipeline()
    return controller

controller=get_controler()
db_status=controller.db_check()

if db_status:
  st.title("Reglamentación alimentaria Argentina")

  with st.chat_message('assistant'):
    st.write("Bienvenido a la aplicación de búsqueda de reglamentación alimentaria Argentina")

  if prompt:=st.chat_input("Ingrese su consulta"):
        with st.chat_message('user'):
            st.write(prompt)

        similitud=controller.process_query(prompt)
        with st.chat_message('assistant'):
                st.text(similitud)
        

    






