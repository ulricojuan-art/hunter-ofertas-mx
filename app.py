import streamlit as st
import requests

# --- TUS DATOS FIJOS (Solo para ti) ---
# Pega aquí el token que te dio @BotFather entre las comillas
TOKEN_TELEGRAM = "TU_TOKEN_DE_BOTFATHER_AQUÍ" 
CHAT_ID = "7704382386"

st.set_page_config(page_title="Mi Hunter Personal", page_icon="🚀")

st.title("🚀 Mi Hunter de Ofertas")
st.markdown("Buscando descuentos masivos en Mercado Libre México.")

# INTERFAZ DE BÚSQUEDA
productos = st.text_input("Productos a monitorear (separados por coma):", "laptop, monitor, smartphone")
descuento_objetivo = st.slider("Descuento mínimo %", 50, 95, 75)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        pass

if st.button("Buscar Ofertas"):
    lista_productos = [p.strip() for p in productos.split(",")]
    st.success(f"Escaneando {len(lista_productos)} categorías...")
    
    encontrados = 0
    for prod in lista_productos:
        url = f"https://api.mercadolibre.com/sites/MLM/search?q={prod}"
        data = requests.get(url).json()
        
        for item in data.get('results', []):
            p_hoy = item.get('price')
            p_antes = item.get('original_price')
            
            if p_antes and p_hoy:
                ahorro = 100 - (p_hoy * 100 / p_antes)
                if ahorro >= descuento_objetivo:
                    encontrados += 1
                    texto_alerta = (f"🔥 *¡OFERTA DETECTADA ({round(ahorro)}%)!*\n\n"
                                   f"📦 {item['title']}\n"
                                   f"💰 Precio actual: ${p_hoy}\n"
                                   f"🔗 [Abrir en Mercado Libre]({item['permalink']})")
                    
                    # Mostrar en la pantalla del celular
                    st.write(f"✅ **{round(ahorro)}%** - {item['title']}")
                    # Enviar mensaje automático a tu Telegram
                    enviar_telegram(texto_alerta)
    
    if encontrados == 0:
        st.info("No se encontraron ofertas nuevas con ese porcentaje.")
    else:
        st.balloons()
