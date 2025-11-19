import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# Chargement des données
file_path = 'Essai appli dashboard (1).xlsx'
df = pd.read_excel(file_path, sheet_name='2025', engine='openpyxl', header=None)

# Initialisation
mois = df.iloc[2:14, 0].tolist()
campagnes = df.iloc[1, 25:33].tolist()
pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
ruptures = int(df.iloc[1, 16])

# Taux d'adhérence global (W2)
raw_adherence = pd.to_numeric(df.iloc[1, 22], errors='coerce')
taux_adherence = (raw_adherence * 100) if pd.notna(raw_adherence) else 0

# Taux d'adhérence S-1 (T2)
adherence_s1 = pd.to_numeric(df.iloc[1, 19], errors='coerce')

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", mois)

# Données campagnes
campagne_data = df.iloc[2:14, 25:34]
campagne_data.columns = campagnes
campagne_data.index = mois
campagne_mois = campagne_data.loc[mois_selectionne].apply(pd.to_numeric, errors='coerce').fillna(0)

# Données hebdomadaires
weekly_data = df.iloc[2:51, [21, 22]]
weekly_data.columns = ["Semaine", "Taux d'adhérence"]
weekly_data.dropna(inplace=True)
weekly_data["Taux d'adhérence"] = pd.to_numeric(weekly_data["Taux d'adhérence"], errors="coerce")
weekly_data["Taux d'adhérence"] = (weekly_data["Taux d'adhérence"] * 100).round(1)
weekly_data["Semaine"] = weekly_data["Semaine"].astype(int)
semaines_completes = list(range(1, 51))
colors = ["green" if val >= 85 else "red" for val in weekly_data["Taux d'adhérence"]]

# Initialisation session
if "current_value" not in st.session_state or st.session_state.get("mois_selectionne") != mois_selectionne:
    st.session_state.current_value = pic_realise[mois_selectionne]
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}
    st.session_state.mois_selectionne = mois_selectionne

# Titre et date
st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - {uap_selection}</h1>", unsafe_allow_html=True)
date_du_jour = datetime.today().strftime('%d/%m/%Y')
st.markdown(f"<p style='text-align:right; font-size:16px; font-weight:bold;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

# Affichage des métriques
col1, col2, col3, col4 = st.columns(4)
col1.metric("PIC Réalisé", f"{pic_realise[mois_selectionne]} km²")
col2.metric("PIC Prévu", f"{pic_prevu[mois_selectionne]} km²")
col3.metric("Ruptures cette semaine", f"{ruptures}")
col4.metric("Taux d'adhérence S-1", f"{adherence_s1:.1f}%" if pd.notna(adherence_s1) else "N/A")

# Graphiques côte à côte
campagne_labels = df.iloc[1, 6:14].tolist()
campagne_values = df[df.iloc[:, 0] == mois_selectionne].iloc[0, 6:14]
campagne_values = pd.to_numeric(campagne_values, errors='coerce').fillna(0)
couleurs_personnalisees = {
    "PRIMETEX": "yellow", "TEXLINE": "green", "NERA": "blue", "MOUSSE": "red",
    "TARABUS": "lightgreen", "SPORISOL": "lightgrey", "START": "grey", "TMAX": "brown"
}
colors_pie = [couleurs_personnalisees.get(label, "white") for label in campagne_labels]

fig_pie = go.Figure(data=[
    go.Pie(labels=campagne_labels, values=campagne_values, hole=0.4, textinfo='label+percent+value', marker=dict(colors=colors_pie))
])
fig_pie.update_layout(title="Répartition par campagne", height=400)

fig_weekly = go.Figure()
fig_weekly.add_trace(go.Scatter(
    x=weekly_data["Semaine"], y=weekly_data["Taux d'adhérence"],
    mode='markers+lines+text', marker=dict(color=colors, size=10),
    name="Taux d'adhérence", text=[f"{val:.1f}%" for val in weekly_data["Taux d'adhérence"]],
    textposition="top center"
))
fig_weekly.add_trace(go.Scatter(
    x=semaines_completes, y=[85]*len(semaines_completes),
    mode='lines', name="Objectif", line=dict(dash='dash', color='blue')
))
fig_weekly.update_layout(title="Évolution hebdomadaire du taux d'adhérence", height=400, xaxis_title="Semaine", yaxis_title="% d'adhérence")

col_pie, col_weekly = st.columns(2)
with col_pie:
    st.plotly_chart(fig_pie, use_container_width=True)
with col_weekly:
    st.plotly_chart(fig_weekly, use_container_width=True)

# Campagnes restantes du mois
st.markdown("### Campagnes restantes du mois")
cols = st.columns(len(campagnes) + 1)
if cols[0].button("🔄 Instant T"):
    st.session_state.current_value = pic_realise[mois_selectionne]
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}

for i, campagne in enumerate(campagnes):
    val = campagne_mois[campagne]
    if val > 0:
        clicked = st.session_state.campagne_clicks[campagne]
        indicator = "🟢" if not clicked else "🔴"
        if cols[i + 1].button(f"{indicator} {campagne}"):
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

# Heatmap
campagne_data_heatmap = df.iloc[2:14, 6:14]
campagne_data_heatmap.columns = campagne_labels
campagne_data_heatmap.index = mois
campagne_data_heatmap = campagne_data_heatmap.apply(pd.to_numeric, errors='coerce').fillna(0)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=campagne_data_heatmap.values,
    x=campagne_data_heatmap.columns,
    y=campagne_data_heatmap.index,
    colorscale='Viridis',
    colorbar=dict(title="Valeur"),
    zmin=0,
    zmax=campagne_data_heatmap.values.max(),
    hoverongaps=False
))
annotations = []
for i, mois_val in enumerate(campagne_data_heatmap.index):
    for j, campagne_val in enumerate(campagne_data_heatmap.columns):
        value = campagne_data_heatmap.iloc[i, j]
        annotations.append(dict(
            x=campagne_val,
            y=mois_val,
            text=str(value),
            showarrow=False,
            font=dict(color="white" if value < campagne_data_heatmap.values.max()/2 else "black", size=10)
        ))
fig_heatmap.update_layout(
    title="Heatmap des campagnes (améliorée)",
    height=600,
    annotations=annotations,
    xaxis=dict(title="Campagnes", tickangle=-45),
    yaxis=dict(title="Mois")
)
st.plotly_chart(fig_heatmap, use_container_width=True)
