import os
import uuid
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from typing import Any,Dict,List
from langchain_core.documents import Document
from .vector_store_client.vector_client import VectorStoreClient
from .loaders.proccesing import Processing
from .embedding.embedder import Embedder
from dotenv import load_dotenv
import logging
from typing import List,Dict
import glob
from .chunking.chunker import Chunker
import json
from .vector_store_client.formater import Formater

"""
    Clase que actua como intermediario mediante la interfaz grafica y la logica 
    principal del programa se encarga de orquestar las disitntas operaciones entre los modulos:
    - Loader:  Almacenar la información en las bases de datos vectorizadas
    - Chunking: Establece y aplica las estrategias para dividir los documentos
    - Processing: Maneja la logica de pre-procesamiento encargado de la limpieza de datos
    """
logger=logging.getLogger(__name__)

class Controler:
    """ Usamos un singleton para manejar el estado global de la aplicación

    Returns:
        VectorStoreClient: Instancia de la clase VectorStoreClient
    """    
    _instance=None

    def __new__(cls,**kwargs):
        if cls._instance is None:
            cls._instance=super().__new__(cls)

        return cls._instance

    def __init__(self,ruta_json='./data/staging',**kwargs):
        '''
            Inicializamos configuración inicial del programa
            conexion a la base de datos asi como la creación 
            de la coleccion en caso de que no exista
        '''
        try:
            self.client:VectorStoreClient=VectorStoreClient(**kwargs)
            self.ruta=ruta_json

        except Exception as e :
                logger.error(f"Problema con Conifg: {e} ")
                raise ValueError(f"Problema estableciendo la conguracion inicial del program{e}")
        
        
    """
    ---------------- Funciones de la logica interna ----------------
    """
    
    def init_chunking(self)->List[Dict[str,Any]]:
        """ Reorna una lista de diccionarios con los documentos segmetados:
        { 'contenido': chunks:str, 
        
        'metadata': { filename:str,
                        type:str 
                    }
        }
        """        
        try:
            logging.info("Iniciando el proceso de segmentación")
            data_content=glob.glob(self.ruta+"/*.json")
            logger.info(f"Se encontraron {len(data_content)} jsons en la ruta {self.ruta}")
            data_store=[]
            for data_path in data_content:
                with open(data_path,"r",encoding='utf-8') as file:
                    data=json.load(open(data_path))
                    chunker=Chunker(data)
                    chunks:List[Dict[str,Any]]=chunker.chunking_hybrid()
                    for chunk in chunks:
                        data_store.append(chunk)
        except:
            raise ValueError("Problema con la segmentación de los documentos")
        logger.info(f"Se generaron {len(data_store)} chunks")
        return data_store

    def init_loading(self):
        '''
        Metodo que se encarga de inicializar el proceso de extraccion y limpieza de los datos mediante el modulo de procesamiento 'Proceesing'
        '''
        try:
            logger.info("Inicializando el proceso de carga de datos")
            p=Processing()
            p.pdf_to_json()
            p.clean_data()
        except Exception as e:
            logger.error(f"Problema con la carga de datos: {e}")
            raise ValueError("Problema con la carga de datos")
        
    def init_embedding(self,data):
            '''
            Metodo que se encarga de inicializar el proceso de embedding de los datos
            '''
            embedder=Embedder()
            try:
                logger.info("Inicializando el proceso de embedding")
                for i in range(0,len(data),1000):
                    data[i:i+1000]=embedder.generate_embeddings(data[i:i+1000])
                    self.client.insert_embeddings(data[i:i+1000])
            except Exception as e:
                logger.error(f"Problema con la carga de datos: {e}")
                raise ValueError("Problema generando los embeddings")
            return data

        
    def init_pipeline(self):
        '''
        Metodo que se encarga de orquestar el pipeline de procesamiento de los datos
        '''
        #paso 1: Inicializamos el proceso de carga de datos y limpieza
        self.init_loading()
        data:List[Dict[str,Any]]=self.init_chunking()
        
        data:List[Dict[str,Any]]=self.init_embedding(data)


    def validar_estado(self)->bool:
        '''
        Metodo el cual valida que en la base de datos existan los embeddings.
        '''
        try:
            # Validamos que la base de datos tenga los embeddings
            logger.info(f"Validando la base de datos")
            if self.client.validar_estado():
                return True
        except Exception as e:
            logger.error(f"Problema con la validación de la base de datos: {e}")
        return False  
        


    """"
    ---------------- Funciones de la interfaz grafica ----------------

    """
   

    def process_query(self,query:str)->List[Document]:
        logger.info(f"Procesando la consulta: {query}")
        lista_resultados=self.client.search(query)
        #LLamamos al formater para alterar los datos
        query_answer=Formater.format_data(query,lista_resultados)
        return query_answer





