import streamlit as st

st.set_page_config(page_title="Menu", layout="wide")

uap = st.session_state.get("uap", "4M")

st.markdown(f"""
    <h1 style='text-align:center; font-size:50px; color:#34495E;'>
        Menu – UAP {uap}
    </h1>
""", unsafe_allow_html=True)

# Si UAP = 4M → on montre les boutons
if uap == "4M":
    st.write("## ")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, _ = st.columns(2)

    with col1:
        if st.button("📊 Dashboard PIC", use_container_width=True):
            st.switch_page("pages/1_Dashboard_PIC.py")

    with col2:
        if st.button("🏭 Planning L1", use_container_width=True):
            st.switch_page("pages/2_L1_Planning.py")

    with col3:
        if st.button("🖨️ Planning Imprimerie", use_container_width=True):
            st.switch_page("pages/3_Imprimerie_Planning.py")

    with col4:
        if st.button("⚙️ Planning Ligne 2", use_container_width=True):
            st.switch_page("pages/4_L2_Planning.py")

    with col5:
        if st.button("🔍 Planning Visitage", use_container_width=True):
            st.switch_page("pages/5_Visitage_Planning.py")
