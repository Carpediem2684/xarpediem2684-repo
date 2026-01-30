import streamlit as st

def show_menu():
    # Récupération de l'UAP choisie sur la page d'accueil
    uap = st.session_state.get("uap_selection", "4M")

    # ====== STYLE GLOBAL DU MENU ======
    st.markdown(
        """
        <style>
        /* Titre principal */
        .menu-title {
            text-align: center;
            font-size: 38px;
            font-weight: 800;
            color: #1B263B;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .menu-subtitle {
            font-size: 18px;
            color: #555;
            margin-bottom: 30px;
        }

        /* Texte "Choisir un module" */
        .menu-section-label {
            font-size: 18px;
            font-weight: 600;
            color: #2C3E50;
            margin-top: 10px;
            margin-bottom: 15px;
        }

        /* Style générique des boutons Streamlit de cette page */
        div.stButton > button {
            border-radius: 8px;
            border: 1px solid #2C3E50;
            padding-top: 10px;
            padding-bottom: 10px;
            font-size: 16px;
            font-weight: 600;
            color: #2C3E50;
            background: #F8F9FA;
        }

        div.stButton > button:hover {
            color: #FFFFFF;
            border-color: #1F8FFF;
            background: linear-gradient(90deg, #1F8FFF, #6EC6FF);
            box-shadow: 0 0 10px rgba(31,143,255,0.4);
        }

        /* Bouton retour */
        .back-btn-container {
            margin-top: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ====== TITRE ======
    st.markdown(
        f"<div class='menu-title'>Menu – UAP {uap}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='menu-subtitle' style='text-align:center;'>Sélectionne un module de planification ou de suivi.</div>",
        unsafe_allow_html=True,
    )

    # ====== LABEL SECTION ======
    st.markdown("<div class='menu-section-label'>Choisir un module :</div>", unsafe_allow_html=True)

    # ====== LIGNE 1 : Dashboard PIC (centré) ======
    top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
    with top_col2:
        if st.button("📊  Dashboard PIC", use_container_width=True):
            st.session_state["page"] = "dashboard_pic"

    st.write("")  # espace

    # ====== LIGNE 2 : Planning Global (centré) ======
    mid_col1, mid_col2, mid_col3 = st.columns([1, 2, 1])
    with mid_col2:
        # Pour l'instant, on ne sait pas encore quelle page utiliser pour le planning global.
        # Tu pourras changer la cible plus tard.
        if st.button("🗺️  Planning Global", use_container_width=True):
            # Exemple : on pourrait pointer vers dashboard_pic ou une future page planning_global
            # st.session_state["page"] = "planning_global"
            st.info("Le module 'Planning Global' est à définir.")

    st.write("")  # espace

    # ====== LIGNE 3 : 4 boutons L1 / Imprimerie / L2 / Visitage ======
    col_l1, col_imp, col_l2, col_vis = st.columns(4)

    with col_l1:
        if st.button("🏭  Planning Ligne 1", use_container_width=True):
            st.session_state["page"] = "planning_l1"

    with col_imp:
        if st.button("🖨️  Planning Imprimerie", use_container_width=True):
            st.session_state["page"] = "planning_imprimerie"

    with col_l2:
        if st.button("⚙️  Planning Ligne 2", use_container_width=True):
            st.session_state["page"] = "planning_l2"

    with col_vis:
        if st.button("🔍  Planning Visitage", use_container_width=True):
            st.session_state["page"] = "planning_visitage"

    # ====== LIGNE 4 : Retour à l'accueil (centré) ======
    st.markdown("<div class='back-btn-container'></div>", unsafe_allow_html=True)

    back_col1, back_col2, back_col3 = st.columns([1, 2, 1])
    with back_col2:
        if st.button("⬅️  Retour à l'accueil", use_container_width=True):
            st.session_state["page"] = "home"
