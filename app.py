
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #8e44ad, #e84393);
        color: white;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h4, h3, h2, p, div {
        font-weight: bold !important;
    }
    .metric-label {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    button {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])

date_du_jour = datetime.today().strftime('%d/%m/%Y')

st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - {uap_selection}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:right; font-size:16px; font-weight:bold;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

if uap_selection == "4M":
    df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)

    mois = df.iloc[2:14, 0].tolist()
    pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
    pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
    ruptures = int(df.iloc[1, 16])

    raw_adherence = pd.to_numeric(df.iloc[1, 22], errors="coerce")
    taux_adherence = (raw_adherence * 100) if pd.notna(raw_adherence) else 0

    st.markdown(f"<h4 style='color:white;'>Taux d'adhérence S-1 : {taux_adherence:.1f}%</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-label'>PIC Réalisé</div>", unsafe_allow_html=True)
    col1.metric("", f"{pic_realise[mois_selectionne]} km²")
    col2.markdown(f"<div class='metric-label'>PIC Prévu</div>", unsafe_allow_html=True)
    col2.metric("", f"{pic_prevu[mois_selectionne]} km²")
    col3.markdown(f"<div class='metric-label'>Ruptures cette semaine</div>", unsafe_allow_html=True)
    col3.metric("", f"{ruptures}")

    # ✅ Lecture du tableau des campagnes à venir (Z2:AH14)
    campagnes_avenir = df.iloc[1, 25:34].tolist()
    campagne_avenir_data = df.iloc[2:14, 25:34]
    campagne_avenir_data.columns = campagnes_avenir
    campagne_avenir_data.index = mois
    campagne_mois = campagne_avenir_data.loc[mois_selectionne]

    st.markdown("### Simulation des campagnes à venir")
    if "current_value" not in st.session_state:
        st.session_state.current_value = pic_realise[mois_selectionne]
    if "selected_campaigns" not in st.session_state:
        st.session_state.selected_campaigns = []

    if st.button("Instant présent"):
        st.session_state.current_value = pic_realise[mois_selectionne]
        st.session_state.selected_campaigns = []

    cols = st.columns(len(campagne_mois))
    for i, (campagne, val) in enumerate(campagne_mois.items()):
        if val > 0:
            color = "red" if campagne in st.session_state.selected_campaigns else "green"
        else:
            color = "gray"
        button_html = f"""
        <button style='background-color:{color}; color:white; padding:8px; border:none; border-radius:5px; width:100%;'>
            {campagne}
        </button>
        """
        cols[i].markdown(button_html, unsafe_allow_html=True)
        if cols[i].button(campagne):
            if campagne in st.session_state.selected_campaigns:
                st.session_state.selected_campaigns.remove(campagne)
                st.session_state.current_value -= val
            else:
                st.session_state.selected_campaigns.append(campagne)
                st.session_state.current_value += val
            if st.session_state.current_value > pic_prevu[mois_selectionne]:
                st.session_state.current_value = pic_prevu[mois_selectionne]

    st.markdown(f"<p style='font-size:18px; font-weight:bold;'>Campagnes sélectionnées : {len(st.session_state.selected_campaigns)}</p>", unsafe_allow_html=True)

    fig_dynamic = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.current_value,
        title={'text': f"Progression PIC ({mois_selectionne})"},
        gauge={
            'axis': {'range': [0, pic_prevu[mois_selectionne]]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, pic_prevu[mois_selectionne]*0.85], 'color': "lightgreen"},
                {'range': [pic_prevu[mois_selectionne]*0.85, pic_prevu[mois_selectionne]], 'color': "yellow"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': pic_prevu[mois_selectionne]
            }
        }
    ))
    st.plotly_chart(fig_dynamic, use_container_width=True)
