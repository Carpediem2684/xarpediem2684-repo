
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Dashboard PIC', layout='wide')

st.title('Dashboard PIC')

# Données extraites du fichier Excel
pic_realise = 5878
pic_prevu = 6411
ruptures = 9
taux_adherence = 45

# KPI
col1, col2 = st.columns(2)
col1.metric("PIC Réalisé", f"{pic_realise} m²")
col2.metric("PIC Prévu", f"{pic_prevu} m²")

# Graphique en camembert
st.subheader("Répartition des m² réalisés par campagne")
campagnes_sum = {
    'MOUSSE': 405,
    'TEXLINE': 742,
    'PRIMETEX': 3734,
    'NERA': 1731,
    'TMAX': 413,
    'SPORISOL': 335,
    'TARABUS': 506
}
fig_pie = px.pie(values=list(campagnes_sum.values()), names=list(campagnes_sum.keys()))
st.plotly_chart(fig_pie, use_container_width=True)

# Ruptures
st.subheader("Ruptures client")
st.write("Nombre de ruptures : " + str(ruptures))

# Jauge pour taux d'adhérence
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

# Nouveau graphique : Histogramme par semaine
st.subheader("Évolution des m² réalisés par semaine et par campagne")
data = {
    'Semaine': ['S-4', 'S-4', 'S-3', 'S-3', 'S-2', 'S-2', 'S-1', 'S-1'],
    'Campagne': ['MOUSSE', 'TEXLINE', 'MOUSSE', 'TEXLINE', 'MOUSSE', 'TEXLINE', 'MOUSSE', 'TEXLINE'],
    'm² Réalisés': [100, 150, 120, 180, 130, 200, 140, 220]
}
df_semaine = pd.DataFrame(data)
fig_bar = px.bar(df_semaine, x='Semaine', y='m² Réalisés', color='Campagne', barmode='group')
st.plotly_chart(fig_bar, use_container_width=True)
