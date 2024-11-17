import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las claves de API y la URL desde las variables de entorno
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

# Función para conectar a Qdrant usando la URL y la clave de API


def connect_qdrant():
    """
    Establece una conexión con el servidor Qdrant en la nube.
    """
    return QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

# Función para crear una colección en Qdrant


def create_collection(client, collection_name, vector_size, distance_metric="COSINE"):
    """
    Crea o actualiza una colección en Qdrant.
    """
    # Usar el enum de Distance para obtener el valor correcto
    distance_enum = getattr(Distance, distance_metric.upper(), None)

    if distance_enum is None:
        raise ValueError(f"Distance metric '{distance_metric}' no es válido.")

    # Crear o actualizar la colección en Qdrant
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance_enum)
    )
    print(f"Colección '{collection_name}' creada o actualizada con éxito.")


# Ahora puedes usar la conexión
client = connect_qdrant()

# Crear una colección
collection_name = "document_embeddings"
vector_size = 1536  # Tamaño del vector generado por 'text-embedding-ada-002'
create_collection(client, collection_name, vector_size,
                  distance_metric="COSINE")
