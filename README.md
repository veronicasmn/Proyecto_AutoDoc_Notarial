# Sistema de Automatización de Extracción y Clasificación de Documentos Notariales

Este proyecto es un sistema de automatización para la extracción y clasificación de texto de documentos notariales, utilizando tecnologías avanzadas como Azure, GPT-4 y Streamlit para la interfaz de usuario. Este sistema permite analizar documentos notariales en formato PDF, extraer texto relevante, clasificar el tipo de documento y resaltar información específica dentro del PDF.

![image](https://github.com/user-attachments/assets/cc05e0ff-136e-4555-adde-4a8a4c0bed72)


## Características

**Extracción de Texto:** Utiliza Azure Form Recognizer para extraer texto de documentos notariales en PDF. 

**Clasificación del Documento:** Utiliza GPT-4 para clasificar automáticamente el tipo de documento notarial en categorías como "Escritura de constitución", "Escritura de poder", "Estatutos de la sociedad", o determinar si el documento no es válido. 

**Extracción de Información Específica:** Dependiendo del tipo de documento, el sistema extrae detalles específicos, como nombres, fechas, cargos, etc. 

**Interfaz de Usuario:** La interfaz de usuario está desarrollada en Streamlit, permitiendo la carga de documentos, la visualización de resultados, y la edición de la información extraída. 

## Tecnologías Utilizadas 

**Azure Form Recognizer:** Para la extracción de texto desde documentos en PDF. 

**GPT-4 (OpenAI a través de Azure):** Para la clasificación de documentos y la extracción de información relevante. 

**Streamlit:** Para la creación de la interfaz de usuario. 

## Estructura del Proyecto
El proyecto está dividido en dos archivos principales:

**app.py**
Este archivo contiene el código que define la interfaz de usuario de la aplicación, implementada con Streamlit. Los usuarios pueden cargar un archivo PDF, y el sistema automáticamente:
Extrae el texto del documento usando Azure Form Recognizer.
Clasifica el documento utilizando un modelo de GPT-4.
Extrae la información relevante de acuerdo con el tipo de documento clasificado.
Resalta el texto relevante dentro del PDF para una fácil revisión.

La interfaz permite además:

Visualizar el PDF original con el texto resaltado en función de la información extraída.
Revisar y editar la información extraída desde un panel lateral, asegurando que los datos sean precisos antes de ser utilizados.

**processing.py**
Este archivo contiene las funciones clave para la extracción, clasificación, y procesamiento de la información dentro del documento:
extract_text_from_document(document_path): Extrae texto del PDF utilizando Azure Form Recognizer.
classify_document_with_gpt4(text): Clasifica el tipo de documento utilizando GPT-4.
Funciones de Extracción de Información Específica: Dependiendo del tipo de documento, se invocan diferentes funciones para extraer detalles específicos, como nombres, fechas, y otros datos relevantes.

## Uso
**Requisitos Previos** 

Azure Account: Debes tener una cuenta en Azure con acceso a los servicios de Form Recognizer y OpenAI (para GPT-4). 

API Keys: Asegúrate de tener las claves API para Azure y GPT-4 configuradas en tu entorno. 


## Instalación
Clona el repositorio:
git clone https://github.com/tu_usuario/tu_repositorio.git

Instala las dependencias:
pip install -r requirements.txt

Configura tus claves de API de Azure y GPT-4 en las variables de entorno o directamente en el código.

## Ejecución
Para ejecutar la aplicación, simplemente utiliza el comando:

streamlit run app.py  
Luego, abre tu navegador y dirígete a http://localhost:8501 para acceder a la interfaz.

## Licencia
Este proyecto está licenciado bajo la licencia CC BY-NC 4.0, lo que significa que puedes usar y modificar el código, pero no puedes utilizarlo con fines comerciales sin el permiso explícito del autor.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para sugerir mejoras o reportar problemas.

## Contacto
Para cualquier pregunta o consulta, puedes contactarme en vsanchezmunoz86@gmail.com
