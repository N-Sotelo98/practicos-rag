from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Inicializar el modelo T5 Large
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")


def generate_questions_from_chunks(corpus_chunks):
    """
    Genera preguntas basadas en los chunks de texto proporcionados.

    Args:
        corpus_chunks (list of str): Lista de textos para los que se generarán preguntas.

    Returns:
        list of str: Lista de preguntas generadas, una por cada chunk.
    """
    questions = []

    for chunk in corpus_chunks:
        # Prompt básico y directo
        input_text = f"{chunk}\nGenera una pregunta clara y específica basada únicamente en este texto."

        # Codificar el texto para el modelo
        input_ids = tokenizer.encode(
            input_text, return_tensors="pt", max_length=512, truncation=True)

        # Generar la pregunta
        outputs = model.generate(
            input_ids, max_length=50, num_beams=4, early_stopping=True)

        # Decodificar la pregunta generada
        question = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Agregar la pregunta a la lista
        questions.append(question)

    return questions
