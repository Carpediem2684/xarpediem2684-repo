import streamlit as st
def show_planning_visitage():
    st.title("🔍 Planning visitage – UAP 4M")
    st.write("Page en cours de construction...")

    st.write("")

    if st.button("⬅️ Retour au menu principal"):
        st.session_state["page"] = "menu"

