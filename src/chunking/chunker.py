import re
from nltk.tokenize import sent_tokenize
from typing import List, Dict, Any
import logging

"""
   Clase encargada de manejar y aplicar las distintas estrategias de chunking estrategia implementadas:
   - Chunking hibrido: Divide el texto en chunks híbridos (narrativos y tablas).
 """
logger=logging.getLogger(__name__)
class Chunker:
    def __init__(self,data,max_chunk_size=600):
        self.data=data
        self.chunk_size=max_chunk_size


    def chunking_hybrid(self) -> Dict[str, Any]:
        """
        Divide el texto en chunks híbridos (narrativos y tablas).

        Returns:
            List[Dict[str, Any]]: Lista de chunks con el tipo y contenido.
        """
        chunks = []
        current_chunk = ""

        # Separar tablas explícitamente (se asume que están delimitadas por "\n")
        sections = re.split(
            r'\[TABLE START\](.*?)\[TABLE END\]', self.data.get('contenido'), flags=re.DOTALL)

        for i, section in enumerate(sections):
            section = section.strip()
            logger.info(f"tamaño de la seccion {len(section)}")
            if i % 2 == 1:  # Es una tabla (índices impares en el split)
                if current_chunk:
                    # Guardar el chunk narrativo acumulado antes de la tabla
                    chunks.append(
                       {"metadata":{ 'type':"narrative",'filename':self.data.get('filename')}, "contenido": current_chunk.strip()})
                    current_chunk = ""
                # Guardar la tabla como un chunk separado
                chunks.append({"metadata":{ 'type':"narrative",'filename':self.data.get('filename')}, "contenido": current_chunk.strip()})
            else:  # Es texto narrativo
                sentences = sent_tokenize(section)  # Dividir el texto en oraciones
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) <= self.chunk_size:
                        current_chunk += sentence + " "
                    else:
                        chunks.append(
                            {"metadata":{ 'type':"narrative",'filename':self.data.get('filename')}, "contenido": current_chunk.strip()})
                        current_chunk = sentence + " "

        # Guardar cualquier chunk narrativo restante
        if current_chunk:
            chunks.append({"metadata":{ 'type':"narrative",'filename':self.data.get('filename')}, "contenido": current_chunk.strip()})

        chunks = [chunk for chunk in chunks if len(chunk['contenido']) > 30]
        for chunk in chunks:
            logger.info(f"Chunk: {chunk['contenido']}")
        return chunks
    

        