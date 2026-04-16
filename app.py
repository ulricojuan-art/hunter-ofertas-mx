import streamlit as st
import requests

# --- CONFIGURACIÓN PRIVADA ---
TOKEN_TELEGRAM = "7770546100:AAG8b5B9f2AC82eyqhAtbPM_cFbXX1lGqzA"
CHAT_ID = "7704382386"

st.set_page_config(page_title="UlricSa Hunter", page_icon="🚀")

st.title("🚀 Mi Hunter de Ofertas")
st.info("Configurado para alertas automáticas a tu Telegram.")

# --- INTERFAZ ---
productos = st.text_input("¿Qué buscamos hoy? (ej: laptop, monitor):", "laptop, monitor")
descuento_objetivo = st.slider("Descuento mínimo %", 50, 95, 75)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        st.error("No se pudo enviar el mensaje a Telegram.")

if st.button("¡Rastrear Ofertas!"):
    lista_productos = [p.strip() for p in productos.split(",")]
    st.write(f"🔎 Buscando: **{', '.join(lista_productos)}**")
    
    encontrados = 0
    
    for prod in lista_productos:
        url_api = f"https://api.mercadolibre.com/sites/MLM/search?q={prod}"
        
        try:
            response = requests.get(url_api).json()
            articulos = response.get('results', [])
            
            for item in articulos:
                p_actual = item.get('price')
                p_lista = item.get('original_price')
                
                if p_lista and p_actual:
                    ahorro = 100 - (p_actual * 100 / p_lista)
                    
                    if ahorro >= descuento_objetivo:
                        encontrados += 1
                        link = item.get('permalink')
                        titulo = item.get('title')
                        
                        # Alerta para Telegram
                        msg = (f"🔥 *OFERTÓN ({round(ahorro)}%)*\n\n"
                               f"📦 {titulo}\n"
                               f"💰 *Precio: ${p_actual:,.2f}*\n"
                               f"🔗 [COMPRAR AQUÍ]({link})")
                        
                        st.success(f"✅ {round(ahorro)}% - {titulo}")
                        enviar_telegram(msg)
        except Exception as e:
            st.error(f"Error buscando {prod}: {e}")

    if encontrados > 0:
        st.balloons()
    else:
        st.warning("No encontré nada con ese descuento ahorita.")
