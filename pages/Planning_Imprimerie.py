import streamlit as st
def show_planning_Imprimerie():
    st.title("🖨️ Planning Imprimerie – UAP 4M")
    st.write("Page en cours de construction...")

    
st.write("")  # petite marge

    # Bouton retour menu
    if st.button("⬅️ Retour au menu principal"):
        # On change la page dans la session
        st.session_state["page"] = "menu"

