import os
import sys


def setup_project_paths():
    """
    Configura y verifica las rutas principales del proyecto.

    - Encuentra el directorio raíz del proyecto (`BASE_DIR`).
    - Agrega el directorio `src` a `sys.path` para asegurar que los módulos del proyecto sean accesibles.
    - Verifica que las rutas esenciales (e.g., `data/capitulos`) existan.

    Returns:
        dict: Un diccionario con las rutas principales del proyecto:
              - BASE_DIR: Ruta base del proyecto.
              - SRC_PATH: Ruta al directorio `src`.
              - PDF_PROCESSING_PATH: Ruta para procesar PDFs.
              - CAPITULOS_DIR: Ruta a los archivos PDF.
    Raises:
        FileNotFoundError: Si no se encuentra `src` o `data/capitulos`.
    """
    # Determinar la ruta base del proyecto automáticamente
    current_dir = os.path.abspath(os.getcwd())
    while not os.path.exists(os.path.join(current_dir, "src")):
        current_dir = os.path.dirname(current_dir)  # Subir un nivel
        if current_dir == "/":  # Llegamos a la raíz del sistema sin encontrar 'src'
            raise FileNotFoundError(
                "No se encontró el directorio 'src' en la estructura del proyecto. "
                "Asegúrate de estar ejecutando el script desde un entorno correcto."
            )

    base_dir = current_dir
    src_path = os.path.join(base_dir, "src")

    # Agregar SRC a sys.path si no está ya agregado
    if src_path not in sys.path:
        sys.path.append(src_path)
        print(f"'src' agregado a sys.path: {src_path}")

    # Confirmar la existencia de `src`
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"El directorio 'src' no existe en {src_path}")

    # Mostrar contenido del directorio `src` para depuración
    print("\nArchivos en el directorio 'src':")
    print(os.listdir(src_path))

    # Configurar rutas importantes
    capitulos_dir = os.path.join(base_dir, "data/capitulos")
    if not os.path.exists(capitulos_dir):
        raise FileNotFoundError(
            f"El directorio 'data/capitulos' no existe en {capitulos_dir}. "
            "Verifica la estructura de tu proyecto."
        )

    return {
        "BASE_DIR": base_dir,
        "SRC_PATH": src_path,
        "PDF_PROCESSING_PATH": os.path.join(src_path, "pdf_processing"),
        "CAPITULOS_DIR": capitulos_dir,
    }
