from ragas import evaluate
from datasets import Dataset


def evaluate_with_ragas(questions, ground_truths, retrieved_documents, metrics=["faithfulness", "answer_relevance", "context_utilization"]):
    """
    Evalúa el sistema de recuperación usando RAGAS.

    Args:
        questions (list of str): Preguntas generadas.
        ground_truths (list of list of str): Ground truths aproximados para cada pregunta.
        retrieved_documents (list of str): Documentos recuperados para las preguntas.
        metrics (list of str): Lista de métricas de evaluación soportadas por RAGAS.

    Returns:
        dict: Resultados de las métricas calculadas.
    """
    # Crear el dataset en el formato esperado por RAGAS
    data = {
        "question": questions,
        "ground_truth": ["\n".join(gt) for gt in ground_truths],
        # Opcional: ajustar si es diferente
        "contexts": ["\n".join(retrieved_documents)] * len(questions),
    }
    ragas_dataset = Dataset.from_dict(data)

    # Evaluar con RAGAS
    results = evaluate(
        dataset=ragas_dataset,
        metrics=metrics
    )
    return results
