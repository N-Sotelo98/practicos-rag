# preprocessing.py
"""
Módulo para preprocesar texto extraído de documentos PDF.

Incluye funciones para limpiar, normalizar y estructurar texto de manera eficiente.
"""

import re


def preprocess_text(raw_text):
    """
    Preprocesa texto extraído de un documento PDF.
    Limpia, normaliza y estructura el texto para chunking posterior.

    Args:
        raw_text (str): Texto crudo extraído del PDF.

    Returns:
        str: Texto preprocesado, limpio y estructurado.
    """
    # 1. Eliminar saltos de línea repetidos
    clean_text = re.sub(r'\n+', '\n', raw_text)

    # 2. Eliminar espacios innecesarios al inicio y final de líneas
    clean_text = re.sub(r'^\s+|\s+$', '', clean_text, flags=re.MULTILINE)

    # 3. Normalización de caracteres especiales
    clean_text = re.sub(r'[^\w\s.,;:()\-/%]', '', clean_text)

    # 4. Consolidar líneas rotas
    # Unir palabras cortadas por salto de línea
    clean_text = re.sub(r'(\w)-\n(\w)', r'\1\2', clean_text)
    # Combinar líneas que no son finales de párrafo
    clean_text = re.sub(r'(?<![.!?])\n(?![A-Z])', ' ', clean_text)

    # 5. Detectar y mantener encabezados
    clean_text = re.sub(
        r'(?i)(cap[ií]tulo \d+|secci[oó]n \d+)', r'\n### \1 ###\n', clean_text)

    # 6. Identificar patrones de tablas
    clean_text = re.sub(
        r'(\S+)\s{2,}(\S+)', r'[TABLE START]\n\1\t\2\n[TABLE END]', clean_text)

    # 7. Eliminar espacios adicionales finales
    clean_text = clean_text.strip()

    return clean_text
