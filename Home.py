import streamlit as st

st.set_page_config(page_title="Accueil", layout="centered")

st.markdown("""
    <h1 style='text-align:center; font-size:60px; color:#2E86C1;'>
        Planification – Tetart.Y
    </h1>
""", unsafe_allow_html=True)

st.write("## ")

# Sélection UAP
uap = st.selectbox("Sélectionner une UAP :", ["4M", "3M", "2M", "KLAM"])

# Stocker l'UAP
st.session_state["uap"] = uap

# Bouton entrer
if st.button("➡️ Entrer", use_container_width=True):
    st.switch_page("Menu.py")
