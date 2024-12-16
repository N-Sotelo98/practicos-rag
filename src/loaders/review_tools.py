# src/loaders/review_tools.py

def revisar_estructuras_generadas(processed_data, num_ejemplos=5):
    """
    Revisa ejemplos de las estructuras generadas tras procesar los PDFs.
    Incluye verificaciones detalladas de las llaves y valores presentes.
    """
    print("\n--- Ejemplo de estructuras generadas tras procesar los PDFs ---\n")

    for archivo, archivo_data in processed_data.items():
        print(f"\nArchivo: {archivo.split('/')[-1]}")
        total_paginas = len(archivo_data.get("paginas", []))
        print(f"Total de páginas procesadas: {total_paginas}")

        ejemplos_texto = 0
        ejemplos_tablas = 0

        for pagina in archivo_data.get("paginas", []):
            print(f"\n--- Página {pagina.get('numero', 'Desconocida')} ---")

            for item in pagina.get("contenido", []):
                print("\n--- Verificando bloque de contenido ---")
                # Imprimir todas las llaves disponibles en el bloque
                print("Llaves encontradas:", list(item.keys()))

                tipo = item.get("tipo", "No especificado")
                capitulo = item.get("capitulo", "No especificado")
                articulo = item.get("articulo", "No especificado")
                pagina_num = item.get("pagina", "Desconocida")

                if not tipo:
                    print("Advertencia: Bloque sin tipo especificado.")
                    continue

                if tipo == "texto" and ejemplos_texto < num_ejemplos:
                    print("\nEjemplo de texto narrativo:")
                    print(f"Capítulo: {capitulo}")
                    print(f"Artículo: {articulo}")
                    print(f"Página: {pagina_num}")
                    print(
                        f"Longitud: {item.get('longitud', 'Desconocida')} caracteres")
                    # Hasta 500 caracteres
                    print(f"Contenido: {item.get('texto', '')[:500]}")
                    ejemplos_texto += 1

                elif tipo == "tabla" and ejemplos_tablas < num_ejemplos:
                    print("\nEjemplo de tabla:")
                    print(f"Capítulo: {capitulo}")
                    print(f"Artículo: {articulo}")
                    print(f"Página: {pagina_num}")
                    try:
                        print(
                            f"Dimensiones: {len(item['tabla'])} filas x {len(item['tabla'][0])} columnas")
                        print("Primera fila de la tabla:", item["tabla"][0])
                    except (KeyError, IndexError):
                        print("Advertencia: Error al procesar la tabla.")
                    ejemplos_tablas += 1

            if ejemplos_texto >= num_ejemplos and ejemplos_tablas >= num_ejemplos:
                break


def revisar_paginas_especificas(processed_data, archivo_parcial_nombre, paginas_deseadas):
    """
    Revisa páginas específicas de un archivo procesado basado en un nombre parcial.
    Incluye verificaciones detalladas de las llaves y valores presentes.
    """
    archivo_nombre = None
    for key in processed_data.keys():
        if archivo_parcial_nombre in key:
            archivo_nombre = key
            break

    if not archivo_nombre:
        print(
            f"Archivo {archivo_parcial_nombre} no encontrado en los datos procesados.")
        return

    print(
        f"\n--- Revisando páginas específicas ({paginas_deseadas}) del archivo: {archivo_nombre} ---\n")

    archivo_data = processed_data[archivo_nombre]
    paginas = archivo_data.get("paginas", [])

    for pagina in paginas:
        numero_pagina = pagina.get("numero", None)
        if numero_pagina in paginas_deseadas:
            print(f"\n--- Página {numero_pagina} ---")

            for item in pagina.get("contenido", []):
                print("\n--- Verificando bloque de contenido ---")
                print("Llaves encontradas:", list(item.keys()))

                tipo = item.get("tipo", "No especificado")
                capitulo = item.get("capitulo", "No especificado")
                articulo = item.get("articulo", "No especificado")
                pagina_num = item.get("pagina", "Desconocida")

                if not tipo:
                    print("Advertencia: Bloque sin tipo especificado.")
                    continue

                if tipo == "texto":
                    print("\nEjemplo de texto narrativo:")
                    print(f"Capítulo: {capitulo}")
                    print(f"Artículo: {articulo}")
                    print(f"Página: {pagina_num}")
                    print(
                        f"Longitud: {item.get('longitud', 'Desconocida')} caracteres")
                    print(f"Contenido: {item.get('texto', '')[:500]}")
                    if capitulo == "No especificado" or articulo == "No especificado":
                        print("Advertencia: Metadatos incompletos.")

                elif tipo == "tabla":
                    print("\nEjemplo de tabla:")
                    try:
                        print(
                            f"Dimensiones: {len(item['tabla'])} filas x {len(item['tabla'][0])} columnas")
                        print("Primera fila de la tabla:", item["tabla"][0])
                    except (KeyError, IndexError):
                        print("Advertencia: Error al procesar la tabla.")
                    if capitulo == "No especificado" or articulo == "No especificado":
                        print("Advertencia: Metadatos incompletos.")
