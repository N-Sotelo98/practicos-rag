# Building an End-to-End Retrieval-Augmented Generation System

Welcome to the **Building an End-to-End Retrieval-Augmented Generation System** repository. This repository is designed to guide you through the process of creating a complete Retrieval-Augmented Generation (RAG) system from scratch, following a structured curriculum.

## Setup Instructions

To get started with the course:

1. Clone this repository:
   ```bash
   git clone https://github.com/CarlosCaris/practicos-rag.git
2. Create a virtual environment
    ```bash
    python -m venv .venv
3. Activate the environment
   ```bash
    # On Mac
    .venv/bin/activate
    # On Windows
    .venv\Scripts\activate
4. Install requirements
    ```bash
    pip install -r requirements.txt
## Table of Contents

- [Building an End-to-End Retrieval-Augmented Generation System](#building-an-end-to-end-retrieval-augmented-generation-system)
  - [Setup Instructions](#setup-instructions)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Course Outline](#course-outline)
    - [Lesson 1: Introduction to Retrieval-Augmented Generation (RAG)](#lesson-1-introduction-to-retrieval-augmented-generation-rag)
    - [Lesson 2: Document Chunking Strategies](#lesson-2-document-chunking-strategies)

## Introduction

This repository contains the materials and code needed to build a complete Retrieval-Augmented Generation (RAG) system. A RAG system combines the strengths of large language models with an external knowledge base to improve the accuracy and relevance of generated responses. Throughout this course, you'll gain hands-on experience with the various components of a RAG system, from document chunking to deployment in the cloud.

## Course Outline

### Lesson 1: Introduction to Retrieval-Augmented Generation (RAG)
- **Objective:** Understand the fundamentals of RAG and its applications.
- **Topics:**
  - Overview of RAG systems
  - Challenges in large language models (e.g., hallucinations, outdated information)
  - Basic components of a RAG system
- **Practical Task:** Set up your development environment and familiarize yourself with the basic concepts.
- **Resources:** 
  - Basics
  - More concepts

### Lesson 2: Document Chunking Strategies
- **Objective:** Learn how to effectively segment documents for better retrieval performance.
- **Topics:**
  - Chunking techniques: token-level, sentence-level, semantic-level
  - Balancing context preservation with retrieval precision
  - Small2Big and sliding window techniques
- **Practical Task:** Implement chunking strategies on a sample dataset.
- **Resources:**
  - The five levels of chunking
  - A guide to chunking
 
---
### Entrega 1: Implementacion de sistema de ingestion
- **Objetivos**
- **Diseñar y desarrollar un sistema modular**: Crear una solución que permita refinar, estructurar y enriquecer un conjunto de datos, asegurando su calidad y consistencia antes de su almacenamiento.

- **Implementar procesos de obtención y preprocesamiento de datos**: Diseñar flujos que incluyan la limpieza, normalización y transformación de las fuentes de información, optimizando los datos para su uso en etapas posteriores.

- **Aplicar estrategias avanzadas de chunking**: Dividir documentos en segmentos manejables y coherentes, facilitando su análisis, procesamiento y almacenamiento de manera eficiente.

- **Almacenar los datos en una base vectorizada**: Estructurar los datos refinados en un formato optimizado para consultas rápidas y eficientes, garantizando su integración con sistemas de análisis y consumo.
---
### Diseño de la solcuion
![RAG drawio-3](https://github.com/user-attachments/assets/be0a436d-ac39-4f8d-a44f-25e868994c86)

**Componentes**
- **Control**: Orquesta toda la ejecución del sistema y actúa como punto de comunicación entre la lógica del programa y la interfaz gráfica, asegurando la integración y el correcto flujo de operaciones.

- **Procesador**: Aplica reglas de segmentación al conjunto de datos utilizando expresiones regulares, garantizando que los datos estén estructurados y listos para su procesamiento posterior.

- **Chunker**: Responsable de aplicar diversas estrategias para la fragmentación de datos. En esta iteración, se implementaron estrategias de *chunking* recurrente y *chunking* híbrido, lo que permite separar componentes tabulares mientras se preserva la semántica del texto.

- **Embedder**: Para la generación de *embeddings*, utilizamos el modelo de Hugging Face `all-MiniLM-L6-v2`, que produce representaciones vectoriales de 384 dimensiones, optimizadas para tareas semánticas.

- **VectorClient**: Gestiona la comunicación con el servicio de almacenamiento (*Qdrant*), facilitando la creación de colecciones y la inserción de puntos, lo que permite un acceso rápido y eficiente a los datos vectorizados.

- **UI**: Componente visual desarrollado en *Streamlit*, que permite realizar consultas interactivas sobre la base vectorizada, proporcionando una experiencia de usuario intuitiva y funcional.
----
## Ejecución del Programa

La aplicación fue compartida en un contenedor Docker para garantizar el encapsulamiento de las dependencias. Sin embargo, es necesario obtener credenciales de **Qdrant** antes de iniciar. Una vez obtenidas la `API_KEY` y el `URL_ENDPOINT`, estas deben almacenarse en el archivo `custom.env`.

### Pasos para la ejecución:

1. **Montar la imagen**:  
   ```bash
   docker compose build
   ```

2. **Ejecutar la aplicación**:  
   ```bash
   docker compose up
   ```

> **Nota:**  
> - La construcción de la imagen puede demorar aproximadamente **10 minutos**.  
> - Si es la primera vez que ejecutas el programa, el tiempo promedio de ejecución es de **30 minutos**.
> - Para ver la ejecucion completa del pipeline modificar el archivo `compose.yaml` la entrada:
  ``` bash
    - PIPE_COLLECTION_NAME=<poner_nombre_coleccion>
   ```





  

  
