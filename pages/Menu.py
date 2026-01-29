import streamlit as st

def show_menu():
    uap = st.session_state.get("uap_selection", "4M")

    st.markdown(f"""
        <h1 style='text-align:center; font-size:45px; color:#34495E;'>
            Menu – UAP {uap}
        </h1>
    """, unsafe_allow_html=True)

    st.write("")
    st.subheader("Choisir un module :")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, _ = st.columns(2)

    # ---- BOUTONS ----

    with col1:
        if st.button("📊 Dashboard PIC", use_container_width=True):
            st.session_state["page"] = "dashboard_pic"

    with col2:
        if st.button("🏭 Planning Ligne 1", use_container_width=True):
            st.session_state["page"] = "planning_l1"

    with col3:
        if st.button("🖨️ Planning Imprimerie", use_container_width=True):
            st.session_state["page"] = "planning_imprimerie"

    with col4:
        if st.button("⚙️ Planning Ligne 2", use_container_width=True):
            st.session_state["page"] = "planning_l2"

    with col5:
        if st.button("🔍 Planning Visitage", use_container_width=True):
            st.session_state["page"] = "planning_visitage"

    st.write("")
    if st.button("⬅️ Retour à l'accueil", use_container_width=True):
        st.session_state["page"] = "home"
