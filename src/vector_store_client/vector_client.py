from dotenv import load_dotenv
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance,PointStruct
from typing import Dict,List,Any,Tuple
import uuid
import os
from langchain_qdrant import QdrantVectorStore
from langchain_qdrant import RetrievalMode
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer


"""
    Maneja la interaccion entre la logica interna y los servicios externos
    - Base de datos vectorizada
"""
logger = logging.getLogger(__name__)
class VectorStoreClient:

    def init_client(self,**kwargs):
        """ Este metodo inicializa una conexion con el cliente externo
           adicionalmente valida que la coleccion se encuentre dentro de la base de datos
           en caso de que no exista crea una collecion usando una configuracion (default_params)
           si no se proven los parametros
        Raises:
            ConnectionRefusedError: Lanza una excepcion si no podemos conectarnos a la base de dato
        Returns:
            client:conexion al cliente asociado a la base de datos
        """        
       
        
        if kwargs.get('type')=='qdrant':
            try:    
                client=QdrantClient(url=self._url_db,
                                api_key=self._api,
                                port=6334,
                                prefer_grpc=True,
                                https=True
                                )
                
        #coleccion de no existir la creo con la confiuracion
               

            except Exception as e:
                raise ConnectionRefusedError(f"No se puede conectar a la base de datos {e}")
                
            return client
        


            
    def __init__(self,**kwargs):
        load_dotenv()
        self._url_db:str=os.getenv('PIPE_DB_ENDPOINT','None')
        self._data:str=os.getenv('PIPE_DATA_PATH')
        self._api:str=os.getenv('PIPE_API_DB')
        self._collection:str=os.getenv('PIPE_COLLECTION_NAME')
        # carga de modelo de embeddings cambiar 
        self.client=self.init_client(**kwargs)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    
    def insert_embeddings(self,data:List[Dict[str,any]]):
        """
        Transdormacion e insercion de los datos
        Args:
            data List[Tuple[List[float],any]] : tuple que contiene los embeddings en la llave 'embeddings' y metadata de informacion en la llave 'metadata'
        """ 
        #Construccion de puntos construccion de PointStruct
        points = [PointStruct(id=str(uuid.uuid4()), vector=vector.get('embedding'),payload=vector.get('content')) for vector in data]
        try:
            #envio de datos mediante la api 
            self.client.upsert(collection_name=self._collection,points=points)
            return True
        except Exception as e:
            raise ConnectionError(f"Problema insertando los datos: {e}")
    
    def validar_estado(self):
        """
        Metodo el cual valida que en la base de datos existan los embeddings.
        Returns:
            bool: True si la base de datos contiene los embeddings
        """        
        default_params={"index_name":self._collection,
                        "vectors_config":{
                                "size":384,
                                "distance":Distance.COSINE}}
        
        status=self.client.collection_exists(collection_name=self._collection)
        if status:
                return True
        else:
                logger.info(f"{default_params.get('vector_config')}")
                vector_config=VectorParams(size=default_params.get('vectors_config').get('size'),
                                                distance=default_params.get('vectors_config').get('distance'))
                self.client.create_collection(collection_name=self._collection,vectors_config=vector_config)
                return False
    
        
    def search(self,query:str,limit=5,**kwargs)->List[Document]:
        """
        Realiza una busqueda en la base de datos vectorizada
        Args:
            query str: texto de la query
        Returns:
            results: resultados de la query
        """        
        vectorized_query= self.model.encode(query)
        retriever=self.client.search(collection_name=self._collection,query_vector=vectorized_query,limit=5)
        lista_documentos=[]
        # pydantic o dataclasss?
        for result in retriever:
             documento={}
             documento['id']=result.id
             documento['score']=result.score
             for  k_p in result.payload.keys():
                  if k_p=='content':
                    documento['content']=result.payload.get(k_p)['content']
                  elif k_p=='contenido':
                    documento['content']=result.payload.get(k_p)

             lista_documentos.append(documento)      
        return lista_documentos




    
    
    