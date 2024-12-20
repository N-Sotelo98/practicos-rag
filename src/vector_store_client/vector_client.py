from dotenv import load_dotenv
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import Dict, List, Any
import uuid
import os
from langchain_qdrant import QdrantVectorStore
from langchain_qdrant import RetrievalMode
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
import asyncio

"""
    Connection between the vector store client and the main logic of the program
"""
logger = logging.getLogger(__name__)

class VectorStoreClient:

    def init_client(self, **kwargs):
        """ 
        Initialize the connection with the vector store client
        if the connection is not possible raise an error ConnectionRefusedError
        """         
        if kwargs.get('type') == 'qdrant':
            try:    
                client = QdrantClient(
                    url=self._url_db,
                    port=6334,
                    prefer_grpc=True,
                    https=True
                )
            except:
                raise ConnectionRefusedError(f"No se puede conectar a la base de datos")
                
            return client
        
    def __init__(self, **kwargs):
        load_dotenv()
        self._url_db: str = os.getenv('PIPE_DB_ENDPOINT', 'None')
        self._data: str = os.getenv('PIPE_DATA_PATH')
        self._collection: str = os.getenv('PIPE_COLLECTION_NAME')
        self._model: str = os.getenv('PIPE_EMBEDDING_MODEL')
        self.client = self.init_client(**kwargs)
        self.model = HuggingFaceEmbeddings(model_name=self._model)
        self.collection_check()
        self.qdrant_vector_store = QdrantVectorStore(self.client, self._collection, embedding=self.model)
        
    async def insert_embeddings(self, data: List[Dict[str, Any]]):
        """
        Parse data from chunks generated into Document objects and insert them into the database using the Asynchronous Add Documents method
        """ 
        documents = [
            Document(
                id=str(uuid.uuid4()), 
                page_content=vector.get('contenido'), 
                metadata=vector.get('metadata')
            ) for vector in data
        ]
        logger.info(f"Insertando los datos en la base de datos {documents[:5]}")
        try:
            logger.info(f"Insertando los datos en la base de datos {len(documents)}")
            await self.qdrant_vector_store.aadd_documents(documents)
        except Exception as e:
            raise ConnectionError(f"Problema insertando los datos {e}")
    
    def collection_check(self) -> None:
        """
        Validates if collection exists inside the database. If it does not exist, it creates it.
        If any problem raises while creating the collection, it raises a ValueError.
        """        
        default_params = {
            "index_name": self._collection,
            "vectors_config": {
                "size": 384,
                "distance": Distance.COSINE
            }
        }
        
        status_collection = self.client.collection_exists(collection_name=self._collection)
        if not status_collection:
            try:
                vector_config = VectorParams(
                    size=default_params.get('vectors_config').get('size'),
                    distance=default_params.get('vectors_config').get('distance')
                )
                self.client.create_collection(collection_name=self._collection, vectors_config=vector_config)
            except:
                raise ValueError(f"Problema creando la colección")
                
    def search(self, query: str, limit=5, **kwargs) -> List[Document]:
        """
        Perform a search query in the database
        Args:
            query str: user input query
        Returns:
            results: results from the query
        """        
        vector_retriever = self.qdrant_vector_store.as_retriever(search_kwargs={"k": limit})
        query_results: List[Document] = vector_retriever.invoke(query)
        lista_documentos = []
        for result in query_results:
            documento = {}
            documento['page_content'] = result.page_content
            documento['metadata'] = result.id
            lista_documentos.append(documento)      
        return lista_documentos