# retrievers/embedding_utils.py

from sentence_transformers import SentenceTransformer

# Inicializa el modelo de embeddings. Aquí usamos un modelo preentrenado de Sentence Transformers.
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def generate_corpus_embeddings(corpus_chunks):
    """
    Genera embeddings para los chunks del corpus.

    Args:
        corpus_chunks (list[str]): Lista de textos (chunks) del corpus.

    Returns:
        torch.Tensor: Embeddings densos generados para los chunks.
    """
    return embedding_model.encode(corpus_chunks, convert_to_tensor=True)


def generate_query_embedding(query):
    """
    Genera un embedding para la consulta.

    Args:
        query (str): Consulta del usuario.

    Returns:
        torch.Tensor: Embedding denso generado para la consulta.
    """
    return embedding_model.encode(query, convert_to_tensor=True)
