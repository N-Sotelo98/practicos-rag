from typing import List,Any
import time
class Formater:
    """
    Clase utilizada para el formateo de los mensajes de entrada y salida
    """    
    # how to ald yield
    @staticmethod
    def format_data(query,lista:List[Any]):
        n_documentos = len(lista)
        yield f"Pregunta: {query}"
        yield f"Tamaño de respuestas encontradas: {n_documentos}"
        time.sleep(1)

        if n_documentos == 0:
            yield "No se encontraron resultados"
        else:
            for documento in lista:
                contenido=documento.get('content')

                template = f"""
                ID: {documento.get('id')} \n
                Score: {documento.get('score')} \n
                Contenido: {contenido}
                ------------------------------------------
                """
                yield template
                time.sleep(1)

        