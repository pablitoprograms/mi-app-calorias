import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración visual para móvil
st.set_page_config(page_title="NutriScan IA", page_icon="🥗", layout="centered")

# --- CONFIGURACIÓN DE TU API KEY ---
API_KEY = "AIzaSyAb02j--_XEA-P9pZLT4a-iihHVDXHAPz4"
genai.configure(api_key=API_KEY)

def analizar_comida(img):
    # Usamos el modelo más rápido y eficiente para fotos
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Eres un experto nutricionista. Analiza la imagen y:
    1. Identifica qué alimentos hay.
    2. Estima las calorías por cada alimento.
    3. Dame el TOTAL de calorías.
    4. Explica brevemente si es una opción saludable.
    
    Responde con un formato limpio y emojis, ideal para leer en pantalla de móvil.
    """
    
    response = model.generate_content([prompt, img])
    return response.text

# --- DISEÑO DE LA APP ---
st.title("🍎 NutriScan")
st.write("Haz una foto a tu plato para saber sus calorías.")

# El botón de cámara que funciona en el móvil
foto = st.camera_input("Capturar plato")

if foto:
    # Mostrar la imagen que se acaba de tomar
    img = Image.open(foto)
    st.image(img, caption="Imagen capturada", use_container_width=True)
    
    if st.button("🔍 ANALIZAR CALORÍAS"):
        with st.spinner("La IA está analizando tu comida..."):
            try:
                resultado = analizar_comida(img)
                st.markdown("---")
                st.markdown(resultado)
            except Exception as e:
                st.error("Error al conectar con la IA. Revisa tu conexión.")

st.markdown("---")
st.caption("Esta app usa inteligencia artificial. Las calorías son estimaciones.")
