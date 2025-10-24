
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# CSS personnalisé
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
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])

date_du_jour = datetime.today().strftime('%d/%m/%Y')

st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - {uap_selection}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:right; font-size:16px; font-weight:bold;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

# Données fictives pour simulation
taux_adherence = 87.5
pic_realise = {mois: val for mois, val in zip([
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
    [120, 130, 110, 140, 150, 160, 170, 180, 190, 200, 210, 220])}
pic_prevu = {mois: val for mois, val in zip([
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
    [125, 135, 115, 145, 155, 165, 175, 185, 195, 205, 215, 225])}
ruptures = 5
campagne_mois = pd.Series({"Campagne A": 50, "Campagne B": 60, "Campagne C": 40, "AUTRES": 80})

# Affichage du taux d'adhérence
st.markdown(f"<h4 style='color:white;'>Taux d'adhérence S-1 : {taux_adherence:.1f}%</h4>", unsafe_allow_html=True)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=taux_adherence,
    title={'text': "Taux d'adhérence S-1"},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 85], 'color': "red"},
            {'range': [85, 100], 'color': "green"}
        ],
        'threshold': {
            'line': {'color': "blue", 'width': 4},
            'thickness': 0.75,
            'value': 85
        }
    }
))
st.plotly_chart(fig_gauge, use_container_width=True)

# Affichage des métriques
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='metric-label'>PIC Réalisé</div>", unsafe_allow_html=True)
col1.metric("", f"{pic_realise[mois_selectionne]} km²")
col2.markdown(f"<div class='metric-label'>PIC Prévu</div>", unsafe_allow_html=True)
col2.metric("", f"{pic_prevu[mois_selectionne]} km²")
col3.markdown(f"<div class='metric-label'>Ruptures cette semaine</div>", unsafe_allow_html=True)
col3.metric("", f"{ruptures}")

# Répartition par campagne
st.markdown("### Répartition par campagne")
fig_pie = go.Figure(data=[
    go.Pie(
        labels=campagne_mois.index,
        values=campagne_mois.values,
        hole=0.4,
        textinfo='label+percent+value',
        hoverinfo='label+percent+value'
    )
])
fig_pie.update_layout(height=400, legend=dict(orientation="h", y=-0.1))
st.plotly_chart(fig_pie, use_container_width=True)

# ✅ Jauge interactive Engine / Torpedo
st.markdown("### Jauge interactive")
if "engine" not in st.session_state:
    st.session_state.engine = 45
if "torpedo" not in st.session_state:
    st.session_state.torpedo = 20

col1, col2 = st.columns(2)
with col1:
    if st.button("Allez plus vite"):
        st.session_state.engine = min(st.session_state.engine + 10, 280)
        st.session_state.torpedo = min(st.session_state.torpedo + 10, 280)
with col2:
    if st.button("Ralentissements"):
        st.session_state.engine = max(st.session_state.engine - 10, 0)
        st.session_state.torpedo = max(st.session_state.torpedo - 10, 0)

fig = go.Figure()
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=st.session_state.engine,
    title={'text': "Engine"},
    gauge={'axis': {'range': [0, 280]},
           'bar': {'color': "blue"},
           'steps': [
               {'range': [0, 200], 'color': "lightgreen"},
               {'range': [200, 250], 'color': "yellow"},
               {'range': [250, 280], 'color': "red"}]}
))
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=st.session_state.torpedo,
    title={'text': "Torpedo"},
    gauge={'axis': {'range': [0, 280]},
           'bar': {'color': "orange"},
           'steps': [
               {'range': [0, 200], 'color': "lightgreen"},
               {'range': [200, 250], 'color': "yellow"},
               {'range': [250, 280], 'color': "red"}]}
))
fig.update_layout(grid={'rows': 1, 'columns': 2}, height=300)
st.plotly_chart(fig, use_container_width=True)
