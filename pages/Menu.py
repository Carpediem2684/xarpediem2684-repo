import streamlit as st

def show_menu():
    uap = st.session_state.get("uap_selection", "4M")

    st.markdown(f"""
        <h1 style='text-align:center; font-size:45px; color:#34495E;'>
            Menu – UAP {uap}
        </h1>
    """, unsafe_allow_html=True)

    st.write("")

    if uap != "4M":
        st.info("Le menu détaillé est pour l'instant disponible uniquement pour l'UAP 4M.")
        st.write("---")

    st.subheader("Choisir un module :")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, _ = st.columns(2)

    # Dashboard PIC
    with col1:
        if st.button("📊 Dashboard PIC"):
    st.markdown("<meta http-equiv='refresh' content='0; url=./Dashboard_PIC'/>", unsafe_allow_html=True)

    # Planning L1
    with col2:
        if st.button("🏭 Planning Ligne 1"):
    st.markdown("<meta http-equiv='refresh' content='0; url=./Planning_L1'/>", unsafe_allow_html=True)


    # Planning Imprimerie
    with col3:
        if st.button("🖨️ Planning Imprimerie"):
    st.markdown("<meta http-equiv='refresh' content='0; url=./Planning_Imprimerie'/>", unsafe_allow_html=True)

    # Planning Ligne 2
    with col4:
        if st.button("🖨️ Planning Ligne 2"):
    st.markdown("<meta http-equiv='refresh' content='0; url=./Planning_L2'/>", unsafe_allow_html=True)

    # Planning Visitage
    with col5:
        if st.button("🖨️ Planning Imprimerie"):
    st.markdown("<meta http-equiv='refresh' content='0; url=./Planning_Visitage'/>", unsafe_allow_html=True)

    st.write("")
    if st.button("⬅️ Retour à l'accueil", use_container_width=True):
        st.session_state["page"] = "home"
        st.experimental_rerun()
``
