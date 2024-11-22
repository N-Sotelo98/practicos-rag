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
import time


"""
    Maneja la interaccion entre la logica interna y los servicios externos
    - Base de datos vectorizada
"""
logger = logging.getLogger(__name__)
class VectorStoreClient:    
    def init_client(self, **kwargs):
        """Este metodo inicializa una conexion con el cliente externo"""        
        if kwargs.get('type') == 'qdrant':
            retry_count = 0
            max_retries = 5
            while retry_count < max_retries:
                try:    
                    client = QdrantClient(
                        url=self._url_db.strip(),
                        api_key=None if not self._api or self._api.strip() == "" else self._api.strip(),
                        prefer_grpc=False,  # Changed to False to use HTTP
                        timeout=10
                    )
                    # Test connection
                    client.get_collections()
                    logger.info(f"Successfully connected to Qdrant at {self._url_db.strip()}")
                    return client
                except Exception as e:
                    retry_count += 1
                    logger.warning(f"Retry {retry_count}/{max_retries} - Connection failed: {e}")
                    if retry_count == max_retries:
                        raise ConnectionRefusedError(f"No se puede conectar a la base de datos después de {max_retries} intentos: {e}")
                    time.sleep(5)  # Wait 5 seconds before retrying

    def __init__(self, **kwargs):
        load_dotenv()
        self._url_db: str = os.getenv('PIPE_DB_ENDPOINT', 'http://localhost:6333')
        self._data: str = os.getenv('PIPE_DATA_PATH', '')
        self._api: str = os.getenv('PIPE_API_DB', '')
        self._collection: str = os.getenv('PIPE_COLLECTION_NAME', 'default')
        
        logger.info(f"Initializing client with URL: {self._url_db}")
        self.client = self.init_client(**kwargs)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        # Initialize collection if it doesn't exist
        self.validar_estado()

    def validar_estado(self) -> bool:
        try:
            status = self.client.collection_exists(collection_name=self._collection)
            if status:
                logger.info(f"Collection {self._collection} already exists")
                return True
            else:
                logger.info(f"Creating collection '{self._collection}'")
                vector_config = VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
                self.client.create_collection(
                    collection_name=self._collection,
                    vectors_config=vector_config
                )
                logger.info(f"Collection '{self._collection}' created successfully")
                return False
        except Exception as e:
            logger.error(f"Error validando estado: {e}")
            raise ConnectionError(f"Problema con la validación de la base de datos: {e}")
        
    def validar_estado(self) -> bool:
        """
        Metodo el cual valida que en la base de datos existan los embeddings.
        Returns:
            bool: True si la base de datos contiene los embeddings
        """        
        default_params = {
            "vectors_config": {
                "size": 384,
                "distance": Distance.COSINE
            }
        }
        
        try:
            status = self.client.collection_exists(collection_name=self._collection)
            if status:
                logger.info(f"Collection {self._collection} already exists")
                return True
            else:
                logger.info(f"Creating collection '{self._collection}' with config: {default_params.get('vectors_config')}")
                vector_config = VectorParams(
                    size=default_params.get('vectors_config').get('size'),
                    distance=default_params.get('vectors_config').get('distance')
                )
                self.client.create_collection(
                    collection_name=self._collection,
                    vectors_config=vector_config
                )
                logger.info(f"Collection '{self._collection}' created successfully")
                return False
        except Exception as e:
            logger.error(f"Error validando estado: {e}")
            raise ConnectionError(f"Problema con la validación de la base de datos: {e}")
    
    def insert_embeddings(self, data: List[Dict[str, Any]]):
        """
        Transdormacion e insercion de los datos
        Args:
            data List[Tuple[List[float],any]] : tuple que contiene los embeddings en la llave 'embeddings' 
            y metadata de informacion en la llave 'metadata'
        """ 
        try:
            # Ensure collection exists before insertion
            if not self.validar_estado():
                logger.warning("Collection was created. Proceeding with insertion.")
            
            # Process in smaller batches
            batch_size = 100
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                points = [
                    PointStruct(
                        id=str(uuid.uuid4()), 
                        vector=vector.get('embedding'),
                        payload=vector.get('content')
                    ) for vector in batch
                ]
                self.client.upsert(
                    collection_name=self._collection,
                    points=points,
                    wait=True
                )
            return True
        except Exception as e:
            raise ConnectionError(f"Problema insertando los datos: {e}")
    

    
    def search(self, query: str, limit=5, **kwargs) -> List[Dict]:
        """
        Realiza una busqueda en la base de datos vectorizada
        Args:
            query str: texto de la query
        Returns:
            results: resultados de la query
        """        
        # Ensure collection exists before search
        if not self.validar_estado():
            logger.warning("Collection was just created. It might be empty.")
            
        vectorized_query = self.model.encode(query)
        retriever = self.client.search(
            collection_name=self._collection,
            query_vector=vectorized_query,
            limit=limit
        )
        lista_documentos = []
        
        for result in retriever:
            documento = {
                'id': result.id,
                'score': result.score
            }
            for k_p in result.payload.keys():
                if k_p == 'content':
                    documento['content'] = result.payload.get(k_p)['content']
                elif k_p == 'contenido':
                    documento['content'] = result.payload.get(k_p)

            lista_documentos.append(documento)      
        return lista_documentos




    
    
    