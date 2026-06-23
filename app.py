# ==================================
# CONTACTO
# ==================================
st.markdown("---")
st.subheader("📲 Contacto profesional")

col1, col2 = st.columns(2)

with col1:
    # MENSAJE OPTIMIZADO Y MÁS CORTO
    mensaje_wa = "Hola%20Kely,%20vi%20tu%20Simulador%20Inmobiliario%20con%20IA%20y%20me%20interesa%20conocer%20m%C3%A1s%20sobre%20tu%20enfoque%20t%C3%A9cnico%20para%20empresas."
    
    st.markdown(f"""
    <a href="https://wa.me/573015704518?text={mensaje_wa}"
    target="_blank">
    <button style="background:#25D366;color:white;padding:10px 18px;border-radius:8px;border:none;cursor:pointer;font-weight:bold;">
    Establishment 💬 WhatsApp Business
    </button>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="https://www.linkedin.com/in/kely-jhojana-hincapi%C3%A9-zapata-502587130/"
    target="_blank">
    <button style="background:#0077B5;color:white;padding:10px 18px;border-radius:8px;border:none;cursor:pointer;font-weight:bold;">
    🔗 LinkedIn
    </button>
    </a>
    """, unsafe_allow_html=True)
