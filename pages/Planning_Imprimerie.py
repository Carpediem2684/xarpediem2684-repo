import streamlit as st

def show_planning_Imprimerie():
    st.title("🏭 Planning Ligne Imprimerie – UAP 4M")
    st.write("Page en cours de construction...")

    st.write("")

    if st.button("⬅️ Retour au menu principal"):
        st.session_state["page"] = "menu"
