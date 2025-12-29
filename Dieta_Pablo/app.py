import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Configuración de la Página
st.set_page_config(page_title="NutriScan - IA de Calorías", page_icon="🍎")

# 2. Configura tu API KEY (Reemplaza con tu clave real)
# Puedes obtenerla en: https://aistudio.google.com/
os.environ["GOOGLE_API_KEY"] = "TU_API_KEY_AQUI"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_gemini_response(image, prompt):
    """Función para llamar a la IA de Gemini"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, image])
    return response.text

# 3. Interfaz de Usuario
st.header("🍎 NutriScan: Detector de Calorías")
st.write("Sube una foto de tu plato y la IA estimará el contenido nutricional.")

# Selector de entrada: Cámara o Archivo
option = st.radio("Selecciona origen de la imagen:", ("Cámara", "Subir archivo"))

uploaded_file = None
if option == "Cámara":
    uploaded_file = st.camera_input("Toma una foto de tu comida")
else:
    uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen cargada', use_container_width=True)
    
    submit = st.button("Analizar Calorías")

    # 4. El "Prompt" (Las instrucciones para la IA)
    input_prompt = """
    Actúa como un experto nutricionista con visión artificial. 
    Analiza la imagen de la comida e identifica cada alimento presente.
    Proporciona un desglose detallado en el siguiente formato:
    
    1. Lista de alimentos identificados con su peso estimado (en gramos).
    2. Calorías estimadas por cada alimento.
    3. Cálculo total de calorías del plato.
    4. Breve consejo sobre si el plato es balanceado o no.
    
    Sé lo más preciso posible basándote en el tamaño visual de las porciones.
    """

    if submit:
        with st.spinner('Analizando tu plato... 🥗'):
            try:
                response = get_gemini_response(image, input_prompt)
                st.subheader("Resultado del Análisis:")
                st.write(response)
            except Exception as e:
                st.error(f"Hubo un error: {e}")