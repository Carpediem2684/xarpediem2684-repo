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

    # --- STYLE GLOBAL ---
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

        .enter-btn {
            width:100%;
            background: linear-gradient(90deg, #1F8FFF, #6EC6FF);
            border:none;
            padding:15px;
            color:white;
            border-radius:12px;
            font-size:20px;
            font-weight:700;
            cursor:pointer;
            transition:0.2s;
        }
        .enter-btn:hover {
            transform: scale(1.03);
            box-shadow: 0 0 18px #6EC6FF;
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
        if st.button("➡️ Entrer", key="enter_btn"):
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
