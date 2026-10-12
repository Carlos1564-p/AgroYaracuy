import streamlit as st
import pandas as pd
import urllib.parse

# Configuración de la aplicación
st.set_page_config(
    page_title="AgroYaracuy | Mercado Digital Agrícola",
    page_icon="🌾",
    layout="wide"
)

# Datos oficiales de la empresa para la pasarela de pago
EMPRESA_NOMBRE = "COMPANIA HCHFA CA"
EMPRESA_RIF = "J404509216"
EMPRESA_BANCO = "Banco de Venezuela (0102)"
EMPRESA_TELEFONO = "04120582064"

# Base de datos temporal en memoria
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []
if "ofertas" not in st.session_state:
    st.session_state.ofertas = []

# Encabezado principal
st.title("🌾 AgroYaracuy: Mercado Agrícola Digital")
st.markdown("Plataforma de subasta e insumos agrícolas para el estado Yaracuy.")

# Menú lateral
menu = st.sidebar.selectbox("Seleccione su Rol:", [
    "🚜 Productor (Publicar Solicitud)", 
    "🏪 Agrotienda (Cotizar y Competir)", 
    "💳 Pasarela de Pago Móvil BDV"
])

# ----------------------------------------------------
# 1. MODULO PRODUCTOR
# ----------------------------------------------------
if menu == "🚜 Productor (Publicar Solicitud)":
    st.header("🚜 Publicar Requerimiento de Insumo")
    st.markdown("Publica qué insumo necesitas para que las agrotiendas de Yaracuy compitan ofreciéndote el mejor precio.")
    
    with st.form("form_productor"):
        nombre = st.text_input("Nombre del Productor / Finca:")
        municipio = st.selectbox("Municipio:", ["San Felipe", "Independencia", "Cocorote", "Bruzual", "Nirgua", "Urachiche", "Páez", "Veroes"])
        insumo = st.text_input("Insumo Requerido (Ej: Urea 50kg, Vacuna Aftosa, Repuesto Tractor):")
        cantidad = st.text_input("Cantidad necesaria:")
        telefono = st.text_input("WhatsApp de Contacto (Ej: 04121234567):")
        
        btn_publicar = st.form_submit_button("🚀 Lanzar Subasta")
        
        if btn_publicar and nombre and insumo and telefono:
            nuevo_id = len(st.session_state.pedidos) + 1
            st.session_state.pedidos.append({
                "id": nuevo_id,
                "nombre": nombre,
                "municipio": municipio,
                "insumo": insumo,
                "cantidad": cantidad,
                "telefono": telefono
            })
            st.success(f"¡Solicitud #{nuevo_id} creada! Las agrotiendas en {municipio} podrán enviarte cotizaciones.")

    st.divider()
    st.subheader("📊 Cotizaciones Recibidas")
    if not st.session_state.pedidos:
        st.info("No hay solicitudes registradas aún.")
    else:
        for p in st.session_state.pedidos:
            st.markdown(f"**Solicitud #{p['id']}:** {p['insumo']} ({p['cantidad']}) - *{p['municipio']}*")
            ofertas_p = [o for o in st.session_state.ofertas if o["pedido_id"] == p["id"]]
            if not ofertas_p:
                st.caption("Aún no hay ofertas para este requerimiento.")
            else:
                for o in sorted(ofertas_p, key=lambda x: x["precio"]):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1:
                        st.write(f"🏪 **{o['tienda']}**")
                    with c2:
                        st.write(f"💲 **${o['precio']:.2f} USD** ({o['tiempo']})")
                    with c3:
                        msg = f"Hola {o['tienda']}, quiero comprar el insumo {p['insumo']} a ${o['precio']:.2f} ofertado en AgroYaracuy."
                        url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                        st.markdown(f"[💬 Contactar por WhatsApp]({url_wa})", unsafe_allow_html=True)
            st.divider()

# ----------------------------------------------------
# 2. MODULO AGROTIENDA
# ----------------------------------------------------
elif menu == "🏪 Agrotienda (Cotizar y Competir)":
    st.header("🏪 Panel para Agrotiendas")
    st.markdown("Revisa las necesidades de los productores locales y compite ofreciendo tu mejor oferta.")
    
    if not st.session_state.pedidos:
        st.info("No hay solicitudes activas de productores por el momento.")
    else:
        for p in st.session_state.pedidos:
            with st.expander(f"🔔 Solicitud #{p['id']}: {p['insumo']} en {p['municipio']}"):
                st.write(f"**Productor:** {p['nombre']} | **Cantidad:** {p['cantidad']}")
                with st.form(f"form_oferta_{p['id']}"):
                    tienda = st.text_input("Nombre de tu Agrotienda:")
                    precio = st.number_input("Precio Oferta en USD ($):", min_value=0.0, format="%.2f")
                    tiempo = st.text_input("Disponibilidad / Tiempo de Entrega:")
                    tel_tienda = st.text_input("Tu WhatsApp (Ej: 04149998877):")
                    
                    btn_enviar = st.form_submit_button("💡 Enviar Cotización")
                    if btn_enviar and tienda and precio > 0:
                        st.session_state.ofertas.append({
                            "pedido_id": p['id'],
                            "tienda": tienda,
                            "precio": precio,
                            "tiempo": tiempo,
                            "telefono_tienda": tel_tienda
                        })
                        st.success("¡Cotización enviada al productor!")

# ----------------------------------------------------
# 3. PASARELA DE PAGO MÓVIL
# ----------------------------------------------------
elif menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil BDV")
    st.markdown("Reporta tu pago o reserva directamente a la cuenta del comercio.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info(f"""
        ### 🏦 Datos Oficiales de Pago:
        * **Comercio:** {EMPRESA_NOMBRE}
        * **RIF:** {EMPRESA_RIF}
        * **Banco:** {EMPRESA_BANCO}
        * **Teléfono Pago Móvil:** {EMPRESA_TELEFONO}
        """)
    
    with col2:
        st.markdown("### 📋 Confirmación de Pago")
        with st.form("form_pago"):
            monto = st.number_input("Monto Pagado:", min_value=0.0, format="%.2f")
            referencia = st.text_input("Número de Referencia:")
            banco_origen = st.text_input("Banco Emisor:")
            
            btn_reportar = st.form_submit_button("Confirmar y Validar Pago")
            
            if btn_reportar:
                if referencia and monto > 0:
                    st.success("¡Pago recibido y registrado con éxito!")
                    msg_pago = f"Hola, he realizado un PagomóvilBDV a {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF}) por ${monto:.2f}. Ref: {referencia}."
                    url_pago_wa = f"https://wa.me/58{EMPRESA_TELEFONO[1:]}?text={urllib.parse.quote(msg_pago)}"
                    st.markdown(f"[📲 Enviar Comprobante a WhatsApp]({url_pago_wa})", unsafe_allow_html=True)
                else:
                    st.error("Por favor completa el monto y número de referencia.")