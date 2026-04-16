import streamlit as st
import requests

# --- CONFIGURACIÓN PRIVADA (UlricSa Hunter) ---
TOKEN_TELEGRAM = "7770546100:AAG8b5B9f2AC82eyqhAtbPM_cFbXX1lGqzA"
CHAT_ID = "7704382386"

st.set_page_config(page_title="UlricSa Hunter", page_icon="🚀", layout="centered")

# Estilo visual simple
st.title("🚀 Mi Hunter de Ofertas")
st.markdown("---")
st.info("Configurado para enviar alertas automáticas a tu Telegram.")

# --- INTERFAZ DE USUARIO ---
productos = st.text_input("¿Qué buscamos hoy? (ej: laptop, monitor, taladro):", "laptop, monitor")
descuento_objetivo = st.slider("Descuento mínimo deseado %", 50, 95, 75)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        st.error(f"Error al enviar a Telegram: {e}")

# --- LÓGICA DE BÚSQUEDA ---
if st.button("¡Rastrear Ofertas Ahora!"):
    lista_productos = [p.strip() for p in productos.split(",")]
    st.write(f"🔎 Escaneando Mercado Libre México para: **{', '.join(lista_productos)}**")
    
    encontrados = 0
    barra_progreso = st.progress(0)
    
    for idx, prod in enumerate(lista_productos):
        # Llamada a la API de Mercado Libre México
        url_api = f"https://api.mercadolibre.com/sites/MLM/search?q={prod}"
        try:
            response = requests.get(url_api).json()
            articulos = response.get('results', [])
            
            for item in articulos:
                precio_actual = item.get('price')
                precio_lista = item.get('original_price')
                
                if precio_lista and precio_actual:
                    ahorro = 100 - (precio_actual * 100 / precio_lista)
                    
                    if ahorro >= descuento_objetivo:
                        encontrados += 1
                        link = item.get('permalink')
