import streamlit as st

st.set_page_config(page_title="Planification – Tetart.Y", layout="wide")

# ----- INITIALISATION -----
if "page" not in st.session_state:
    st.session_state["page"] = "home"

page = st.session_state["page"]

# ============================
#     PAGE D’ACCUEIL DESIGN
# ============================

if page == "home":

    # --- STYLE GLOBAL + STYLE DU GROS BOUTON MENU ---
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #0D1117 0%, #1B263B 100%);
        }
        .big-title {
            font-size: 64px;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #6EC6FF, #1F8FFF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 40px;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align:center;
            font-size: 20px;
            color: #D0D6E1;
            margin-bottom: 40px;
        }

        .glass-box {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 18px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255,255,255,0.1);
        }

        /* STYLISER LE BOUTON STREAMLIT "MENU" COMME UN GROS BOUTON */
        div.stButton > button[kind="secondary"] {
            width: 100%;
            background: linear-gradient(90deg, #1F8FFF, #6EC6FF);
            padding: 22px 60px;
            border-radius: 14px;
            font-size: 32px;
            font-weight: 900;
            color: white;
            border: none;
            text-align: center;
            cursor: pointer;
            transition: 0.25s ease;
            box-shadow: 0px 0px 18px rgba(31,143,255,0.6);
        }

        div.stButton > button[kind="secondary"]:hover {
            transform: scale(1.07);
            box-shadow: 0px 0px 28px rgba(110,198,255,1);
        }

        .menu-wrapper {
            width:100%;
            display:flex;
            justify-content:center;
            margin-top:30px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- TITRE ---
    st.markdown("<div class='big-title'>Planification – Tetart.Y</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Optimisation 4M – 3M – Production PVC</div>", unsafe_allow_html=True)

    # --- CONTENEUR CENTRAL ---
    with st.container():
        st.markdown("<div class='glass-box'>", unsafe_allow_html=True)

        uap = st.selectbox(
            "Sélectionne ton UAP :",
            ["4M", "2M", "P2000", "KLAM"]
        )
        st.session_state["uap_selection"] = uap

        st.write("")
        st.markdown("</div>", unsafe_allow_html=True)

    # ================================
    #   GROS BOUTON MENU EN BAS
    # ================================
    st.markdown("<div class='menu-wrapper'>", unsafe_allow_html=True)

    # 👉 ICI c'est un vrai st.button, donc il peut changer la page
    if st.button("MENU", key="big_menu_btn"):
        st.session_state["page"] = "menu"

    st.markdown("</div>", unsafe_allow_html=True)

# ============================
#     PAGE MENU (inchangée)
# ============================
elif page == "menu":
    from pages.Menu import show_menu
    show_menu()

elif page == "dashboard_pic":
    from pages.Dashboard_PIC import show_dashboard_pic
    show_dashboard_pic()

elif page == "planning_l1":
    from pages.Planning_L1 import show_planning_l1
    show_planning_l1()

elif page == "planning_imprimerie":
    from pages.Planning_Imprimerie import show_planning_imprimerie
    show_planning_imprimerie()

elif page == "planning_l2":
    from pages.Planning_L2 import show_planning_l2
    show_planning_l2()

elif page == "planning_visitage":
    from pages.Planning_Visitage import show_planning_visitage
    show_planning_visitage()

