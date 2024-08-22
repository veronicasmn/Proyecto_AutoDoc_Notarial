import os
from openai import AzureOpenAI
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import fitz  # PyMuPDF
from pdf2image import convert_from_path

# Configuración y el endpoint de GPT-4
gpt4 = AzureOpenAI(
    api_key="api key", 
    api_version="2024-02-01",
    azure_endpoint="https://enlacendpoint.com"
)

# Configuración OCR
endpoint = "https://enlacendpoint.com"
credential = AzureKeyCredential("api key")
client = DocumentAnalysisClient(endpoint, credential)

IS_DEBUG = True  # or False

def extract_text_from_document(document_path):
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-layout", document=f)
    result = poller.result()
    
    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"
    
    return extracted_text

def classify_document_with_gpt4(text):
    classification_prompt = f"""
    Por favor, clasifica el siguiente texto según el tipo de documento notarial:
    - Escritura de constitución
    - Escritura de poder
    - Estatutos de la sociedad
    si el documento no es de ninguna de estas clases responde documento no valido
    Texto:
    {text}
    
    Tipo de documento:
    """
    response = gpt4.chat.completions.create(
        model="PruebaModelo4o",
        messages=[{"role": "user", "content": classification_prompt}],
        temperature=0.1,
        max_tokens=100
    )
    
    document_type = response.choices[0].message.content.strip()
    if IS_DEBUG:
        print(f"[DEBUG] Tipo de documento clasificado: {document_type}")
    return document_type

def extract_group_info(text, prompt):
    response = gpt4.chat.completions.create(
        model="PruebaModelo4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=500
    )
    result = response.choices[0].message.content.strip()
    if IS_DEBUG:
        print(f"[DEBUG] Información extraída: {result}")
    return result

def extract_statutes_info(text, document_type):
    prompt_statutes = f"""
    Extrae la siguiente información del documento de estatutos de la sociedad:
    - Tipo de documento: {document_type}
    - Nombre de la sociedad
    
    Si alguno de estos campos no está presente en el texto, indica "No aplica".

    Documento:
    {text}
    """
    if IS_DEBUG:
        print("[DEBUG] Ejecutando extract_statutes_info")
    return extract_group_info(text, prompt_statutes)

def extract_constitution_or_power_1(text):
    prompt_1 = f"""
    Extrae la siguiente información de este documento notarial:
    - Nombre notario
    - Protocolo (número)
    - Tipo documento
    - Localidad
    - Fecha otorgamiento
    - Registro

    Si alguno de estos campos no está presente en el texto, indica "No aplica".
    (responde solo con la información solicitada)

    Documento:
    {text}
    """
    if IS_DEBUG:
        print("[DEBUG] Ejecutando extract_constitution_or_power_1")
    return extract_group_info(text, prompt_1)

def extract_constitution_or_power_2(text):
    prompt_2 = f"""    
    Extrae la siguiente información de este documento notarial:
    - Nombre sociedad
    - CIF sociedad
    - Administrador sociedad
    - Domicilio sociedad
    
    Si alguno de estos campos no está presente en el texto, indica "No aplica".
    (responde solo con la información solicitada)
    Documento:
    {text}
    """
    if IS_DEBUG:
        print("[DEBUG] Ejecutando extract_constitution_or_power_2")
    return extract_group_info(text, prompt_2)

def extract_constitution_or_power_3(text):
    prompt_3 = f"""
    Extrae la siguiente información de este documento notarial:
    - Fecha caducidad poder
    - Nombre apoderado
    - DNI apoderado
    - Domicilio apoderado
    - Cargo apoderado
    - Duración cargo
    - Tipo firma
    
    Si alguno de estos campos no está presente en el texto, indica "No aplica".
    (responde solo con la información solicitada)
    Documento:
    {text}
    """
    if IS_DEBUG:
        print("[DEBUG] Ejecutando extract_constitution_or_power_3")
    return extract_group_info(text, prompt_3)

def extract_constitution_or_power_4(text):
    prompt_4 = f"""
    Extrae la siguiente información de este documento notarial:
    - Poderes cuentas corrientes y depósitos
    - Poderes créditos préstamos
    - Poderes valores AAF y fondos
    - Límite económico
    - Límite geográfico
    
    Si alguno de estos campos no está presente en el texto, indica "No aplica", en el caso de Límite económico y Límite geográfico indica "Sin límite"
    (responde solo con la información solicitada)
    Documento:
    {text}
    """
    if IS_DEBUG:
        print("[DEBUG] Ejecutando extract_constitution_or_power_4")
    return extract_group_info(text, prompt_4)

def extract_information(text, document_type):
    document_type_clean = document_type.lower()
    if IS_DEBUG:
        print(f"[DEBUG] Document Type (cleaned): {document_type_clean}")
    if "estatutos de la sociedad" in document_type_clean:
        return extract_statutes_info(text, document_type)
    elif "escritura de constitución" in document_type_clean or "escritura de poder" in document_type_clean:
        result = []
        if IS_DEBUG:
            print("[DEBUG] Tipo Escritura identificado")
        result.append(extract_constitution_or_power_1(text))
        result.append(extract_constitution_or_power_2(text))
        result.append(extract_constitution_or_power_3(text))
        result.append(extract_constitution_or_power_4(text))
        return "\n".join(result)
    else:
        if IS_DEBUG:
            print("[DEBUG] Tipo de documento no reconocido")
        return "Tipo de documento no reconocido o no soportado."

def highlight_text_in_pdf(pdf_path, highlights):
    doc = fitz.open(pdf_path)
    highlighted_words = set()  # Para asegurar que solo se resalte la primera instancia

    for highlight in highlights:
        text = highlight['text']
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            if text not in highlighted_words:
                areas = page.search_for(text)
                if areas:
                    # Añadir un resaltado al primer área encontrada
                    page.add_highlight_annot(areas[0])
                    highlighted_words.add(text)
                    break  # Salir del bucle para solo resaltar la primera instancia

    output_path = "highlighted_temp.pdf"
    doc.save(output_path)
    doc.close()

    return output_path

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images
