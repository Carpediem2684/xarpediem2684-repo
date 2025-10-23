import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# CSS pour fond dégradé et réduction des marges
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
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])

st.markdown("<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - 4M</h1>", unsafe_allow_html=True)

# Lecture des données
df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)

# Données hebdomadaires
weekly_data = df.iloc[2:51, [21, 22]]
weekly_data.columns = ["Semaine", "Taux d'adhérence"]
weekly_data.dropna(inplace=True)

# Conversion en numérique et pourcentage
weekly_data["Taux d'adhérence"] = pd.to_numeric(weekly_data["Taux d'adhérence"], errors="coerce")
weekly_data["Taux d'adhérence"] = (weekly_data["Taux d'adhérence"] * 100).round(1)
weekly_data["Semaine"] = weekly_data["Semaine"].astype(int)

# Couleur dynamique pour les points
colors = ["green" if val >= 85 else "red" for val in weekly_data["Taux d'adhérence"]]

# Graphique hebdomadaire avec ligne objectif
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=weekly_data["Semaine"],
    y=weekly_data["Taux d'adhérence"],
    mode='markers+lines',
    marker=dict(color=colors, size=10),
    name="Taux d'adhérence"
))
fig.add_trace(go.Scatter(
    x=weekly_data["Semaine"],
    y=[85]*len(weekly_data),
    mode='lines',
    name="Objectif",
    line=dict(dash='dash', color='blue')
))
fig.update_layout(title="Évolution hebdomadaire du taux d'adhérence",
                  xaxis_title="Semaine",
                  yaxis_title="% d'adhérence",
                  height=400)

st.plotly_chart(fig, use_container_width=True)
