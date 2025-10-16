
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Dashboard PIC', layout='wide')

st.title('Dashboard PIC')

# === Filtres ===
filtre = st.radio("Filtrer par :", ["Semaine", "Mois"], horizontal=True)

semaines_disponibles = ['S-4', 'S-3', 'S-2', 'S-1']
mois_disponibles = ['Janvier', 'Février', 'Mars']

if filtre == "Semaine":
    semaine_selectionnee = st.selectbox("Choisir une semaine :", semaines_disponibles)
else:
    mois_selectionne = st.selectbox("Choisir un mois :", mois_disponibles)

# === Données fictives ===
pic_realise = 5878
pic_prevu = 6411
ruptures = 9
taux_adherence = 45

campagnes_sum = {
    'MOUSSE': 405,
    'TEXLINE': 742,
    'PRIMETEX': 3734,
    'NERA': 1731,
    'TMAX': 413,
    'SPORISOL': 335,
    'TARABUS': 506
}

# Données hebdomadaires fictives
semaine_data = {
    'Semaine': ['S-4', 'S-4', 'S-3', 'S-3', 'S-2', 'S-2', 'S-1', 'S-1'],
    'Campagne': ['MOUSSE', 'TEXLINE', 'MOUSSE', 'TEXLINE', 'MOUSSE', 'TEXLINE', 'MOUSSE', 'TEXLINE'],
    'm² Réalisés': [100, 150, 120, 180, 130, 200, 140, 220]
}
df_semaine = pd.DataFrame(semaine_data)

# Données mensuelles fictives pour heatmap
mois_data = {
    'Campagne': ['MOUSSE', 'TEXLINE', 'PRIMETEX', 'NERA', 'TMAX'],
    'Janvier': [120, 200, 500, 300, 100],
    'Février': [130, 220, 550, 320, 110],
    'Mars': [140, 240, 600, 340, 120]
}
df_mois = pd.DataFrame(mois_data)
df_mois.set_index('Campagne', inplace=True)

# === Onglets pour les graphiques ===
tabs = st.tabs(["KPI", "Répartition", "Évolution", "Heatmap", "Ruptures", "Adhérence"])

# KPI
with tabs[0]:
    col1, col2 = st.columns(2)
    col1.metric("PIC Réalisé", f"{pic_realise} m²")
    col2.metric("PIC Prévu", f"{pic_prevu} m²")

# Répartition
with tabs[1]:
    st.subheader("Répartition des m² réalisés par campagne")
    fig_pie = px.pie(values=list(campagnes_sum.values()), names=list(campagnes_sum.keys()))
    st.plotly_chart(fig_pie, use_container_width=True)

# Évolution
with tabs[2]:
    st.subheader("Évolution des m² réalisés par semaine et par campagne")
    if filtre == "Semaine":
        df_filtre = df_semaine[df_semaine['Semaine'] == semaine_selectionnee]
    else:
        df_filtre = df_semaine
    fig_bar = px.bar(df_filtre, x='Campagne', y='m² Réalisés', color='Campagne')
    st.plotly_chart(fig_bar, use_container_width=True)

# Heatmap
with tabs[3]:
    st.subheader("Heatmap des m² réalisés par campagne et par mois")
    if filtre == "Mois":
        df_heat = df_mois[[mois_selectionne]]
    else:
        df_heat = df_mois
    fig_heatmap = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Ruptures
with tabs[4]:
    st.subheader("Ruptures client")
    st.write("Nombre de ruptures : " + str(ruptures))

# Adhérence
with tabs[5]:
    st.subheader("Taux d'adhérence S-1")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=taux_adherence,
        title=dict(text="Taux d'adhérence S-1"),
        gauge=dict(
            axis=dict(range=[0, 100]),
            bar=dict(color="darkblue"),
            steps=[
                dict(range=[0, 50], color="lightgray"),
                dict(range=[50, 80], color="gray"),
                dict(range=[80, 100], color="green")
            ]
        )
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)
