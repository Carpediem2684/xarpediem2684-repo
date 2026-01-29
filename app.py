import streamlit as st

st.set_page_config(page_title="Planification", layout="centered")

# Titre principal
st.markdown("""
    <h1 style='text-align:center; font-size:50px; color:#2E86C1;'>
        Planification – Tetart.Y
    </h1>
""", unsafe_allow_html=True)

st.write("")  # petit espace

# Sélection UAP
uap = st.selectbox(
    "Sélectionner une UAP :", 
    ["4M", "2M", "P2000", "KLAM"]  # adapte si besoin
)

# On stocke l'UAP en session pour la suite
st.session_state["uap_selection"] = uap

st.write("")

# Bouton Entrer
if st.button("➡️ Entrer", use_container_width=True):
    st.switch_page("Menu")
