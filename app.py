import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Cazador de Ofertas MX", page_icon="🚀")

st.title("🚀 Cazador de Ofertas México")
st.markdown("Busca descuentos masivos en Mercado Libre y recibe alertas en tu Telegram.")

# --- SECCIÓN DE CONFIGURACIÓN ---
with st.sidebar:
    st.header("🔧 Configuración de Alertas")
    user_token = st.text_input("Token de tu Bot (de @BotFather):", type="password")
    user_chat_id = st.text_input("Tu ID de Telegram (de @userinfobot):")
    st.info("Estos datos son necesarios para enviarte las alertas a tu celular.")

# --- INTERFAZ DE BÚSQUEDA ---
productos = st.text_input("¿Qué quieres buscar? (separa con comas):", "laptop, consola, smartphone")
descuento_objetivo = st.slider("Descuento mínimo %", 50, 95, 75)

def enviar_telegram(token, chat_id, mensaje):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except:
        st.error("Error al enviar la alerta a Telegram. Revisa tu Token e ID.")

if st.button("Buscar y Activar Alertas"):
    if not user_token or not user_chat_id:
        st.warning("⚠️ Por favor, ingresa tu Token e ID en la barra lateral para recibir alertas.")
    else:
        lista_productos = [p.strip() for p in productos.split(",")]
        st.success(f"Buscando {len(lista_productos)} categorías...")
        
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
                        msg = (f"🔥 *¡OFERTA ENCONTRADA ({round(ahorro)}%)!*\n\n"
                               f"📦 {item['title']}\n"
                               f"💰 Precio: ${p_hoy}\n"
                               f"🔗 [Ver producto]({item['permalink']})")
                        
                        # Mostrar en pantalla
                        st.write(f"✅ **{round(ahorro)}%** - {item['title']} - [Link]({item['permalink']})")
                        # Enviar a Telegram
                        enviar_telegram(user_token, user_chat_id, msg)
        
        if encontrados == 0:
            st.info("No se encontraron descuentos tan altos en este momento. Intenta con otros productos.")
        else:
            st.balloons()
