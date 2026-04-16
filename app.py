import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="UlricSa Hunter", page_icon="🚀")

st.title("🚀 Hunter de Ofertas México")
st.subheader("Configuración de Alertas")

# Interfaz de usuario
productos = st.text_input("Productos a buscar (separados por coma):", "laptop, monitor, celular")
descuento_objetivo = st.slider("Descuento mínimo %", 50, 95, 75)

if st.button("Actualizar Búsqueda y Activar"):
    lista_productos = [p.strip() for p in productos.split(",")]
    st.success(f"Buscando {len(lista_productos)} categorías con >{descuento_objetivo}% de descuento")
    
    # Aquí el código busca una vez para mostrarte resultados inmediatos
    for prod in lista_productos:
        url = f"https://api.mercadolibre.com/sites/MLM/search?q={prod}"
        data = requests.get(url).json()
        
        for item in data.get('results', []):
            p_hoy = item.get('price')
            p_antes = item.get('original_price')
            if p_antes and p_hoy:
                ahorro = 100 - (p_hoy * 100 / p_antes)
                if ahorro >= descuento_objetivo:
                    st.write(f"🔥 **{round(ahorro)}%** - {item['title']}")
                    st.write(f"Link: {item['permalink']}")
