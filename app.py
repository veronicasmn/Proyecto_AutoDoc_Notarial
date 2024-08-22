
import streamlit as st
import tempfile
from processing import extract_text_from_document, classify_document_with_gpt4, extract_information, highlight_text_in_pdf, pdf_to_images

def main():
    st.title("Extracción de Datos de Documentos Notariales")

    uploaded_file = st.file_uploader("Carga un archivo PDF", type=["pdf"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_pdf_path = temp_file.name

        # Extraer texto del documento
        text = extract_text_from_document(temp_pdf_path)
        document_type = classify_document_with_gpt4(text)

        # Extraer información específica según el tipo de documento
        extracted_info = extract_information(text, document_type)
        
        if extracted_info:
            st.sidebar.header("Resultados de la extracción")

            info_dict = {}
            highlights = []
            lines = extracted_info.split("\n")
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    info_dict[key.strip()] = value.strip()
                    highlights.append({'text': value.strip()})

            # Mostrar formulario en el sidebar para editar la información
            with st.sidebar.form(key="info_form"):
                updated_info_dict = {}
                for key in info_dict.keys():
                    updated_info_dict[key] = st.text_input(label=key, value=info_dict[key])
                st.form_submit_button("Actualizar Información")

            # Resaltar texto en el PDF
            highlighted_pdf_path = highlight_text_in_pdf(temp_pdf_path, highlights)

            # Convertir el PDF resaltado a imágenes
            images = pdf_to_images(highlighted_pdf_path)

            # Mostrar imágenes del PDF en la página principal
            st.header("Visualización del PDF")
            for img in images:
                st.image(img, use_column_width=True)
        else:
            st.sidebar.write("No se pudo extraer información del documento.")

if __name__ == "__main__":
    main()
