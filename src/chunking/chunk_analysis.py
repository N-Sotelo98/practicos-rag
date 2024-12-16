# src/chunking/chunk_analysis.py

from statistics import mean, stdev

# Análisis de Chunks Narrativos


def analizar_chunks_narrativos(chunks_narrativos):
    """
    Calcula estadísticas generales de los chunks narrativos.
    Args:
        chunks_narrativos (list): Lista de chunks narrativos.
    Returns:
        dict: Estadísticas de los chunks narrativos.
    """
    total_chunks = len(chunks_narrativos)
    total_caracteres = sum(len(chunk["texto"]) for chunk in chunks_narrativos)

    return {
        "total_chunks": total_chunks,
        "total_caracteres": total_caracteres,
        "promedio_caracteres": total_caracteres / total_chunks if total_chunks > 0 else 0
    }

# Análisis de Chunks de Tablas


def analizar_chunks_tablas(chunks_tablas):
    """
    Calcula estadísticas generales de los chunks de tablas.
    Args:
        chunks_tablas (list): Lista de chunks de tablas.
    Returns:
        dict: Estadísticas de los chunks de tablas.
    """
    total_chunks = len(chunks_tablas)
    total_filas = sum(chunk["metadatos"]["filas"] for chunk in chunks_tablas)
    total_columnas = sum(chunk["metadatos"]["columnas"]
                         for chunk in chunks_tablas)

    return {
        "total_chunks": total_chunks,
        "total_filas": total_filas,
        "promedio_filas": total_filas / total_chunks if total_chunks > 0 else 0,
        "promedio_columnas": total_columnas / total_chunks if total_chunks > 0 else 0
    }

# Estadísticas por Capítulo


def calcular_estadisticas_chunks_por_capitulo(chunks_narrativos):
    """
    Calcula estadísticas descriptivas de los chunks narrativos agrupados por capítulo.
    Args:
        chunks_narrativos (list): Lista de chunks narrativos.
    Returns:
        dict: Estadísticas descriptivas agrupadas por capítulo.
    """
    estadisticas = {}

    for chunk in chunks_narrativos:
        capitulo = chunk["capitulo"]
        total_caracteres = chunk["metadatos"]["total_caracteres"]
        paginas_inicial = chunk["metadatos"]["paginas_inicial"]
        paginas_final = chunk["metadatos"]["paginas_final"]

        if capitulo not in estadisticas:
            estadisticas[capitulo] = {
                "total_chunks": 0,
                "total_caracteres": [],
                "rango_paginas": set()
            }

        estadisticas[capitulo]["total_chunks"] += 1
        estadisticas[capitulo]["total_caracteres"].append(total_caracteres)
        estadisticas[capitulo]["rango_paginas"].update(
            range(paginas_inicial, paginas_final + 1))

    estadisticas_descriptivas = {}
    for capitulo, data in estadisticas.items():
        estadisticas_descriptivas[capitulo] = {
            "total_chunks": data["total_chunks"],
            "promedio_caracteres": mean(data["total_caracteres"]),
            "desviacion_caracteres": stdev(data["total_caracteres"]) if len(data["total_caracteres"]) > 1 else 0,
            "rango_paginas": f"{min(data['rango_paginas'])}-{max(data['rango_paginas'])}"
        }

    return estadisticas_descriptivas
