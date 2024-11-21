from sentence_transformers import SentenceTransformer
import logging
import numpy as np
"""
    Clase encragada de los embeddings apartir de los chunks generados para cada documento
"""
logger=logging.getLogger(__name__)
class Embedder:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        

    def generate_embeddings(self,chunks):
        """
        Genera embeddings para un chunk de texto  adiciona el atributo embeddings al diccionario 
        y retorna el diccionario con los embeddings incluidos 

        Args:
            chunks (list of str): Fragmentos de texto a procesar.

        Returns:
            list of dict: Lista de diccionarios con los embeddings incluidos.
           {contenido: 'texto',embeddings: [0.1,0.2,0.3,0.4,0.5]}
        """
        try:
            for chunk in chunks:

                embedding = self.model.encode(chunk.get('contenido'), convert_to_numpy=True)
                chunk['embedding'] = embedding
                chunk['metadata']['contenido'] = chunk['contenido']

                assert chunk['embedding'] is not None, "Error al generar los embeddings"

        except Exception as e:
            raise ValueError("Problema generando los embeddings")
    
        return chunks