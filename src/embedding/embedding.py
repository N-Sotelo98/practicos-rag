import openai  # Asegúrate de que esta línea esté presente
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_embeddings(chunks):
    """
    Genera embeddings para una lista de fragmentos de texto.

    Args:
        chunks (list of str): Fragmentos de texto a procesar.

    Returns:
        list of list of float: Lista de embeddings generados para cada fragmento.
    """
    embeddings = []
    for chunk in chunks:
        try:
            # Generar embeddings con el modelo text-embedding-ada-002
            response = openai.Embedding.create(
                input=chunk,
                model="text-embedding-ada-002"
            )
            embeddings.append(response['data'][0]['embedding'])
        except Exception as e:
            print(f"Error al generar embedding para un chunk: {e}")
    return embeddings
