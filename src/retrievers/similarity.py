# retrievers/similarity.py

from sentence_transformers import util


def calculate_similarity(query_embedding, corpus_embeddings):
    """
    Calcula la similitud coseno entre el embedding de una consulta y los embeddings del corpus.

    Args:
        query_embedding (torch.Tensor): Embedding de la consulta.
        corpus_embeddings (torch.Tensor): Embeddings de los chunks del corpus.

    Returns:
        numpy.ndarray: Matriz de similitud coseno (query vs. cada chunk del corpus).
    """
    similarities = util.pytorch_cos_sim(query_embedding, corpus_embeddings)
    return similarities.cpu().numpy()
