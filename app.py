import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# Chargement des donnes
df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)

# Initialisation
mois = df.iloc[2:14, 0].tolist()
campagnes = df.iloc[1, 25:33].tolist()
pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
ruptures = int(df.iloc[1, 16])
raw_adherence = pd.to_numeric(df.iloc[1, 22], errors="coerce")
taux_adherence = (raw_adherence * 100) if pd.notna(raw_adherence) else 0

# Se9lection utilisateur
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Se9lection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", mois)

# Titre et date
st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - {uap_selection}</h1>", unsafe_allow_html=True)
date_du_jour = datetime.today().strftime('%d/%m/%Y')
st.markdown(f"<p style='text-align:right; font-size:16px; font-weight:bold;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color:white;'>Taux d'adhe9rence S-1 : {taux_adherence:.1f}%</h4>", unsafe_allow_html=True)

# Affichage des me9triques
col1, col2, col3 = st.columns(3)
col1.metric("PIC Re9alise9", f"{pic_realise[mois_selectionne]} kmb2")
col2.metric("PIC Pre9vu", f"{pic_prevu[mois_selectionne]} kmb2")
col3.metric("Ruptures cette semaine", f"{ruptures}")

# Donne9es campagnes
campagne_data = df.iloc[2:14, 25:33]
campagne_data.columns = campagnes
campagne_data.index = mois
campagne_mois = campagne_data.loc[mois_selectionne].apply(pd.to_numeric, errors='coerce').fillna(0)

# Donne9es hebdomadaires
weekly_data = df.iloc[2:51, [21, 22]]
weekly_data.columns = ["Semaine", "Taux d'adhe9rence"]
weekly_data.dropna(inplace=True)
weekly_data["Taux d'adhe9rence"] = pd.to_numeric(weekly_data["Taux d'adhe9rence"], errors="coerce")
weekly_data["Taux d'adhe9rence"] = (weekly_data["Taux d'adhe9rence"] * 100).round(1)
weekly_data["Semaine"] = weekly_data["Semaine"].astype(int)
semaines_completes = list(range(1, 51))
colors = ["green" if val >= 85 else "red" for val in weekly_data["Taux d'adhe9rence"]]

# Initialisation session
if "current_value" not in st.session_state:
    st.session_state.current_value = pic_realise[mois_selectionne]
if "campagne_clicks" not in st.session_state:
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}

# Bouton reset
if st.button("Instant pre9sent"):
    st.session_state.current_value = pic_realise[mois_selectionne]
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}

# Boutons horizontaux avec indicateurs
st.markdown("### Campagnes e0 venir")
cols = st.columns(len(campagnes))
for i, campagne in enumerate(campagnes):
    val = campagne_mois[campagne]
    if val > 0:
        clicked = st.session_state.campagne_clicks[campagne]
        indicator = "F7E2" if not clicked else "F534"
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

# Graphique camembert
fig_pie = go.Figure(data=[
    go.Pie(labels=campagne_mois.index, values=campagne_mois.values, hole=0.4, textinfo='label+percent+value')
])
fig_pie.update_layout(title="Re9partition par campagne", height=400)
st.plotly_chart(fig_pie, use_container_width=True)

# Graphique ligne PIC
df_evol = pd.DataFrame({"Mois": mois, "PIC Re9alise9": pic_realise.values, "PIC Pre9vu": pic_prevu.values})
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=df_evol["Mois"], y=df_evol["PIC Re9alise9"], mode='lines+markers', name="PIC Re9alise9"))
fig_line.add_trace(go.Scatter(x=df_evol["Mois"], y=df_evol["PIC Pre9vu"], mode='lines+markers', name="PIC Pre9vu"))
fig_line.update_layout(title="c9volution mensuelle du PIC", height=300, xaxis_title="Mois", yaxis_title="Surface (kmb2)")
st.plotly_chart(fig_line, use_container_width=True)

# Heatmap des campagnes
fig_heatmap = go.Figure(data=go.Heatmap(z=campagne_data.values, x=campagne_data.columns, y=campagne_data.index, colorscale='Viridis'))
fig_heatmap.update_layout(title="Heatmap des campagnes", height=300)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Graphique hebdomadaire
fig_weekly = go.Figure()
fig_weekly.add_trace(go.Scatter(
    x=weekly_data["Semaine"],
    y=weekly_data["Taux d'adhe9rence"],
    mode='markers+lines+text',
    marker=dict(color=colors, size=10),
    name="Taux d'adhe9rence",
    text=[f"{val:.1f}%" for val in weekly_data["Taux d'adhe9rence"]],
    textposition="top center"
))
fig_weekly.add_trace(go.Scatter(
    x=semaines_completes,
    y=[85]*len(semaines_completes),
    mode='lines',
    name="Objectif",
    line=dict(dash='dash', color='blue')
))
fig_weekly.update_layout(title="c9volution hebdomadaire du taux d'adhe9rence", height=400, xaxis_title="Semaine", yaxis_title="% d'adhe9rence")
st.plotly_chart(fig_weekly, use_container_width=True)
