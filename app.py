import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# Chargement des données
df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)

# Initialisation
mois = df.iloc[2:14, 0].tolist()
campagnes = df.iloc[1, 25:33].tolist()
pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
ruptures = int(df.iloc[1, 16])
raw_adherence = pd.to_numeric(df.iloc[1, 22], errors="coerce")
taux_adherence = (raw_adherence * 100) if pd.notna(raw_adherence) else 0

# Sélection utilisateur
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", mois)

# Titre et date
st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - {uap_selection}</h1>", unsafe_allow_html=True)
date_du_jour = datetime.today().strftime('%d/%m/%Y')
st.markdown(f"<p style='text-align:right; font-size:16px; font-weight:bold;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color:white;'>Taux d'adhérence S-1 : {taux_adherence:.1f}%</h4>", unsafe_allow_html=True)

# Affichage des métriques
col1, col2, col3 = st.columns(3)
col1.metric("PIC Réalisé", f"{pic_realise[mois_selectionne]} km²")
col2.metric("PIC Prévu", f"{pic_prevu[mois_selectionne]} km²")
col3.metric("Ruptures cette semaine", f"{ruptures}")

# Données campagnes
campagne_data = df.iloc[2:14, 25:33]
campagne_data.columns = campagnes
campagne_data.index = mois
campagne_mois = campagne_data.loc[mois_selectionne].apply(pd.to_numeric, errors='coerce').fillna(0)

# Initialisation session
if "current_value" not in st.session_state:
    st.session_state.current_value = pic_realise[mois_selectionne]
if "campagne_clicks" not in st.session_state:
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}

# Bouton reset
if st.button("Instant présent"):
    st.session_state.current_value = pic_realise[mois_selectionne]
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}

# Boutons horizontaux avec indicateurs
st.markdown("### Campagnes à venir")
cols = st.columns(len(campagnes))
for i, campagne in enumerate(campagnes):
    val = campagne_mois[campagne]
    if val > 0:
        clicked = st.session_state.campagne_clicks[campagne]
        indicator = "🟢" if not clicked else "🔴"
        if cols[i].button(f"{indicator} {campagne}"):
            st.session_state.campagne_clicks[campagne] = True
            st.session_state.current_value += val
            if st.session_state.current_value > pic_prevu[mois_selectionne]:
                st.session_state.current_value = pic_prevu[mois_selectionne]

# Jauge dynamique
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
