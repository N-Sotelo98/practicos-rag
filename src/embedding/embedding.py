from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Cargar el modelo preentrenado
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Modelo 'all-MiniLM-L6-v2' cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None


def generate_embeddings(chunks):
    """
    Genera embeddings para una lista de fragmentos de texto.

    Args:
        chunks (list of str): Fragmentos de texto a procesar.

    Returns:
        list of list of float: Lista de embeddings generados para cada fragmento.
    """
    if model is None:
        raise ValueError(
            "El modelo no está cargado. No se pueden generar embeddings.")

    embeddings = []
    try:
        print(f"Generando embeddings para {len(chunks)} chunks...")

        # Usar tqdm para la barra de progreso
        for chunk in tqdm(chunks, desc="Generando embeddings", unit="chunk"):
            embedding = model.encode(chunk, convert_to_numpy=True)
            embeddings.append(embedding)

        print(f"Total de embeddings generados: {len(embeddings)}")
    except Exception as e:
        print(f"Error al generar los embeddings: {e}")
    return embeddings
