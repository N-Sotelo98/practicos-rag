import os
import uuid
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from typing import Any,Dict,List
from langchain_core.documents import Document
from .vector_store_client.vector_client import VectorStoreClient
from .loaders.proccesing import Processing
from .retrievers.retriever import Retriever
from dotenv import load_dotenv
import logging
import glob
from .chunking.chunker import Chunker
import json
from .vector_store_client.formater import Formater
from typing import List,Dict
import asyncio
logger=logging.getLogger(__name__)

class Controler:
    """ 
   Manage the interaction between the user interface and the main logic of the program
   orchestrate the different operations between the modules:
    - Loader: Store the information in the vectorized databases
    - Chunking: Establish and apply the strategies to divide the documents
    - Processing: Handles the pre-processing logic responsible for data cleaning
    - Retrieval  LLM component use to retrieve the most similar documents
    """    
    _instance=None

    def __new__(cls,**kwargs):
        if cls._instance is None:
            cls._instance=super().__new__(cls)

        return cls._instance

    def __init__(self,data_path='./data/staging',**kwargs):
        '''
            Initialize the controler class
            estabilish the connection with the vector store client
            raises an error if the connection is not possible
        '''
        try:
            self.client:VectorStoreClient=VectorStoreClient(**kwargs)
            self.retriever=Retriever()
            self.path:str=data_path

        except:
            raise ValueError(f"Problema estableciendo la conguracion inicial del programa ")
        
    
    def init_chunking(self)->List[Dict[str,Any]]:
        try:
            logging.info("Iniciando el proceso de segmentación")
            data_content: List[str]=glob.glob(self.path+"/*.json")
            logger.info(f"Se encontraron {len(data_content)} jsons en la ruta {self.path}")
            data_store:List[str]=[]
            for data_path in data_content:
                
                with open(data_path,"r",encoding='utf-8') as file:

                    data=json.load(open(data_path))
                    chunker=Chunker(data)
                    chunks:List[Dict[str,Any]]=chunker.chunking_hybrid()
                    for chunk in chunks:
                        data_store.append(chunk)

            logger.info(f"Se generaron {len(data_store)} chunks")
        except:
            raise ValueError("Problema con la segmentación de los documentos")
        return data_store

    def init_loading(self):
        '''
        Extraction and cleaning of the data
        '''
        try:
            logger.info("Inicializando el proceso de carga de datos")
            p=Processing()
            p.pdf_to_json()
            p.clean_data()
        except:
          
            raise ValueError("Problema con la carga de datos")
        
    def init_embedding(self,data):
            '''
            Load embedding into the database
            '''
            try:
                logger.info("Inicializando el proceso de embedding")
                for i in range(0,len(data),1000):
                    insert_data= asyncio.run(self.client.insert_embeddings(data[i:i+1000]))
            except:
                raise ValueError("Problema generando los embeddings")
            return data

        
    def init_pipeline(self):
        '''
        Orchestrates the pipeline execution steps
        '''
        self.init_loading()
        data:List[Dict[str,Any]]=self.init_chunking()
        data:List[Dict[str,Any]]=self.init_embedding(data)
        



    def db_check(self)->None:
        '''
        Check the status of the collection inside the database
        '''
        try:
            logger.info(f"Validando la base de datos")
            self.client.collection_check()
            return True
        except:
           raise ValueError("Problema con la base de datos")
        
   

    def process_query(self,query:str)->List[Document]:
        logger.info(f"Procesando la consulta: {query}")
        lista_resultados=self.client.search(query)
        contenido='\n'.join([doc.get('page_content') for doc in lista_resultados])
        respuesta=self.retriever.process_query(question=query,context=contenido)
        
        #respuesta_formateada=Formater.format_data(respuesta)
        return respuesta





