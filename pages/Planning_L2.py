import streamlit as st

def show_planning_l2():
    st.title("🏭 Planning Ligne 2 – UAP 4M")
    st.write("Page en cours de construction...")

    st.write("")

    if st.button("⬅️ Retour au menu principal"):
        st.session_state["page"] = "menu"

