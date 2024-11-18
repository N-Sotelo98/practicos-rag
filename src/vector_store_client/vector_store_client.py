import os
import uuid
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Conectar a Qdrant utilizando las credenciales desde el archivo .env


def connect_to_qdrant():
    api_key_qdrant = os.getenv("QDRANT_API_KEY")
    url_qdrant = os.getenv("QDRANT_URL")
    qdrant_client = QdrantClient(url=url_qdrant, api_key=api_key_qdrant)
    return qdrant_client

# Crear el índice en Qdrant si no existe


def create_qdrant_index(qdrant_client, index_name, dimension, metric=Distance.COSINE):
    collections_response = qdrant_client.get_collections()
    if index_name not in [collection.name for collection in collections_response.collections]:
        qdrant_client.create_collection(
            collection_name=index_name,
            vectors_config=VectorParams(size=dimension, distance=metric)
        )
        print(f"Índice '{index_name}' creado correctamente.")
    else:
        print(f"El índice '{index_name}' ya existe.")

# Función para dividir los embeddings en lotes más pequeños


def create_batches(data, batch_size):
    """Divide una lista de datos en lotes más pequeños."""
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

# Insertar los embeddings en Qdrant


def insert_embeddings(qdrant_client, index_name, embeddings_list, metadata_list, batch_size=100):
    embedding_batches = create_batches(embeddings_list, batch_size)
    metadata_batches = create_batches(metadata_list, batch_size)

    for batch_id, (batch_embeddings, batch_metadata) in enumerate(zip(embedding_batches, metadata_batches)):
        points = [
            {
                # Generar un UUID único para cada punto
                "id": str(uuid.uuid4()),
                # Convertir numpy array a lista si es necesario
                "vector": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
                "payload": {"content": metadata}  # Los metadatos del chunk
            }
            for embedding, metadata in zip(batch_embeddings, batch_metadata)
        ]
        try:
            response = qdrant_client.upsert(
                collection_name=index_name,
                points=points
            )
            print(
                f"Lot {batch_id + 1} insertado exitosamente con {len(points)} puntos.")
        except Exception as e:
            print(f"Error al insertar el lote {batch_id + 1}: {str(e)}")

# Realizar una búsqueda en Qdrant


def search_qdrant(qdrant_client, index_name, query_vector, limit=5):
    results = qdrant_client.search(
        collection_name=index_name,
        query_vector=query_vector,
        limit=limit
    )
    return results


def format_qdrant_results(query, results):
    print(f"Consulta: {query}\n")
    print(f"Total de resultados encontrados: {len(results)}\n")
    print("-" * 80)

    for match in results:
        print(f"ID: {match.id}")
        print(f"Puntaje de Similitud (score): {match.score}")
        print("Payload completo:")

        payload = match.payload

        # Intentar manejar 'content' dinámicamente
        content = payload.get("content", None)

        if content is None:
            print("  No se encontró la clave 'content' en el payload.")
        else:
            # Manejo dinámico del contenido
            if isinstance(content, str):
                # Mostrar directamente si es un string
                print(f"  Contenido relevante: {content[:700]}...")
            elif isinstance(content, dict):
                # Mostrar claves del diccionario
                print("  Contenido es un diccionario con las siguientes claves:")
                for key, value in content.items():
                    print(f"    {key}: {value}")
            elif isinstance(content, list):
                # Mostrar los primeros elementos si es una lista
                print(
                    f"  Contenido es una lista con {len(content)} elementos. Mostrando los primeros 5:")
                for i, item in enumerate(content[:5]):
                    print(f"    [{i}]: {item}")
            else:
                # Tipo desconocido, convertir a string y mostrar
                print(
                    f"  Tipo desconocido de contenido: {type(content)}. Mostrando contenido completo:")
                print(str(content))

        print("-" * 80)


def debug_format_qdrant_results(query, results):
    """
    Depura y analiza los resultados obtenidos de Qdrant, mostrando detalles de cada elemento
    para identificar el origen de cualquier error.
    """
    print(f"Consulta: {query}\n")
    print(f"Total de resultados encontrados: {len(results)}\n")
    print("-" * 80)

    for i, match in enumerate(results):
        print(f"--- Resultado {i + 1} ---")
        print(f"ID: {getattr(match, 'id', 'ID no encontrado')}")
        print(
            f"Puntaje de Similitud (score): {getattr(match, 'score', 'Score no encontrado')}")

        # Intentar imprimir el payload completo
        try:
            print("Payload completo:")
            print(match.payload)
        except Exception as e:
            print(f"Error al acceder al payload: {e}")
            continue

        # Inspeccionar contenido del payload
        payload = getattr(match, 'payload', None)

        if payload is None:
            print("Payload no está disponible para este resultado.")
        else:
            print("Estructura del Payload:")
            print(f"Tipo del payload: {type(payload)}")
            if isinstance(payload, dict):
                for key, value in payload.items():
                    print(f"  {key}: {type(value)} -> {value}")
                    # Si la clave es 'content', analizar su contenido
                    if key == "content":
                        content = value
                        print("  Analizando 'content':")
                        if isinstance(content, str):
                            print(f"    Es un string: {content[:700]}")
                        elif isinstance(content, list):
                            print(
                                f"    Es una lista con {len(content)} elementos.")
                            print(f"    Primeros 5 elementos: {content[:5]}")
                        elif isinstance(content, dict):
                            print(
                                f"    Es un diccionario con claves: {list(content.keys())}")
                        else:
                            print(
                                f"    Tipo desconocido: {type(content)} -> {content}")
            else:
                print("Payload no es un diccionario, no se puede analizar más.")
        print("-" * 80)
