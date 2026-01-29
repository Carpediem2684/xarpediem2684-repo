import streamlit as st

# ----- CONFIG GLOBALE -----
st.set_page_config(page_title="Planification – Tetart.Y", layout="wide")

# ----- INITIALISATION DE LA PAGE COURANTE -----
if "page" not in st.session_state:
    st.session_state["page"] = "home"   # page d'accueil par défaut

page = st.session_state["page"]

# ================== PAGE ACCUEIL ==================
if page == "home":
    st.markdown("""
        <h1 style='text-align:center; font-size:50px; color:#2E86C1;'>
            Planification – Tetart.Y
        </h1>
    """, unsafe_allow_html=True)

    st.write("")

    uap = st.selectbox(
        "Sélectionner une UAP :",
        ["4M", "2M", "P2000", "KLAM"]
    )
    st.session_state["uap_selection"] = uap

    st.write("")

    # 👉 IMPORTANT : ici on se contente de changer l'état,
    # Streamlit relance le script automatiquement
    if st.button("➡️ Entrer", use_container_width=True):
        st.session_state["page"] = "menu"

# ================== PAGE MENU ==================
elif page == "menu":
    from pages.Menu import show_menu
    show_menu()

# ================== PAGE DASHBOARD PIC ==================
elif page == "dashboard_pic":
    from pages.Dashboard_PIC import show_dashboard_pic
    show_dashboard_pic()

# ================== PAGE PLANNING L1 ==================
elif page == "planning_l1":
    from pages.Planning_L1 import show_planning_l1
    show_planning_l1()

# ================== PAGE PLANNING IMPRIMERIE ==========
elif page == "planning_imprimerie":
    from pages.Planning_Imprimerie import show_planning_imprimerie
    show_planning_imprimerie()

# ================== PAGE PLANNING L2 ==================
elif page == "planning_l2":
    from pages.Planning_L2 import show_planning_l2
    show_planning_l2()

# ================== PAGE PLANNING VISITAGE ============
elif page == "planning_visitage":
    from pages.Planning_Visitage import show_planning_visitage
    show_planning_visitage()
