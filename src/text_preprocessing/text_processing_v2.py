import re


def preprocess_text_v2(raw_text: str) -> str:
    """
    Preprocesa texto crudo con énfasis en la detección de tablas,
    basado en patrones generales observados en varios documentos.

    Args:
        raw_text (str): Texto crudo extraído del PDF.

    Returns:
        str: Texto preprocesado con tablas identificadas.
    """
    # Limpieza inicial
    clean_text = re.sub(r'\n+', '\n', raw_text)  # Consolidar saltos de línea
    # Eliminar espacios innecesarios
    clean_text = re.sub(r'^\s+|\s+$', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'[^\w\s.,;:()\-/%\[\]|]', '',
                        clean_text)  # Normalizar caracteres

    # Unir líneas rotas
    # Unir palabras cortadas
    clean_text = re.sub(r'(\w)-\n(\w)', r'\1\2', clean_text)
    # Combinar líneas no finales de párrafo
    clean_text = re.sub(r'(?<![.!?])\n(?![A-Z])', ' ', clean_text)

    # Detectar encabezados importantes
    clean_text = re.sub(
        r'(?i)(cap[ií]tulo \d+|secci[oó]n \d+)', r'\n### \1 ###\n', clean_text)

    # Detectar tablas
    lines = clean_text.split('\n')
    processed_lines = []
    inside_table = False

    for i, line in enumerate(lines):
        # Detectar líneas que parecen parte de tablas
        is_table_line = bool(re.match(r'^\s*\S+(\s{2,}|\t)\S+', line))
        is_numeric_line = bool(
            re.search(r'\d+(\.\d+)?', line)) and len(line.split()) > 2
        is_next_line_table = (
            i +
            1 < len(lines) and bool(
                re.match(r'^\s*\S+(\s{2,}|\t)\S+', lines[i + 1]))
        )

        if is_table_line or is_numeric_line or (inside_table and is_next_line_table):
            if not inside_table:
                processed_lines.append('[TABLE START]')
                inside_table = True
            processed_lines.append(line)
        else:
            if inside_table:
                processed_lines.append('[TABLE END]')
                inside_table = False
            processed_lines.append(line)

    # Cerrar tabla abierta al final del documento
    if inside_table:
        processed_lines.append('[TABLE END]')

    # Marcar posibles tablas
    for i, line in enumerate(processed_lines):
        if not line.startswith('[TABLE') and bool(re.search(r'[\d\w]\s{2,}[\d\w]', line)):
            processed_lines[i] = '[POSSIBLE TABLE START]\n' + \
                line + '\n[POSSIBLE TABLE END]'

    return '\n'.join(processed_lines).strip()
