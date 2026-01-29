import streamlit as st

def show_planning_l1():
    st.title("🏭 Planning Ligne 1 – UAP 4M")
    st.write("Page en cours de construction...")
    
st.write("")  # petite marge

    # Bouton retour menu
    if st.button("⬅️ Retour au menu principal"):
        # On change la page dans la session
        st.session_state["page"] = "menu"

