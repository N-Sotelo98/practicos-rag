# loaders.py
import os
import pdfplumber
from langchain.document_loaders import PyPDFLoader


def load_pdf(filepath):
    """
    Carga un archivo PDF y extrae su contenido como una lista de documentos.
    Si PyPDFLoader falla, intenta procesarlo con pdfplumber.

    Args:
        filepath (str): Ruta completa al archivo PDF.

    Returns:
        list: Lista de documentos (o texto bruto si se usa pdfplumber).
    """
    try:
        # Intentar cargar el PDF con PyPDFLoader
        loader = PyPDFLoader(filepath)
        documents = loader.load()
        print(f"Se cargó correctamente el archivo con PyPDFLoader: {filepath}")
        return documents
    except Exception as e:
        print(f"Error con PyPDFLoader, intentando con pdfplumber: {filepath}")
        try:
            # Cargar el PDF con pdfplumber como respaldo
            with pdfplumber.open(filepath) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text() if page.extract_text() else ''
                print(
                    f"Se cargó correctamente el archivo con pdfplumber: {filepath}")
                return [{'page_content': text}]
        except Exception as fallback_error:
            print(f"Error al cargar con pdfplumber: {fallback_error}")
            return []


def load_pdfs_from_folder(folder_path):
    """
    Carga y procesa todos los archivos PDF de una carpeta.

    Args:
        folder_path (str): Ruta de la carpeta que contiene los archivos PDF.

    Returns:
        list: Lista combinada de documentos procesados de todos los PDFs.
    """
    all_documents = []
    try:
        # Iterar sobre los archivos de la carpeta
        for file in os.listdir(folder_path):
            if file.endswith('.pdf'):  # Verificamos que sea un archivo PDF
                file_path = os.path.join(folder_path, file)
                # Cargar y procesar cada PDF
                documents = load_pdf(file_path)
                # Agregamos los documentos al resultado
                all_documents.extend(documents)
        print(f"Se procesaron {len(all_documents)} documentos en total.")
    except Exception as e:
        print(f"Error al procesar la carpeta {folder_path}: {e}")
    return all_documents


if __name__ == "__main__":
    # Código de prueba: Cambia "ruta_de_prueba" por la carpeta donde tengas los PDFs
    prueba_carpeta = "./data"  # Carpeta donde estarán los PDFs
    documentos = load_pdfs_from_folder(prueba_carpeta)
    print(f"Documentos cargados: {len(documentos)}")
