import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import requests

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# CSS pour fond dégradé bleu et blanc
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ffffff, #3498db);
        color: black;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar : sélection UAP et mois
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_options = ["Depuis Janvier", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
mois_selectionne = st.sidebar.selectbox("Choisir un mois", mois_options)

# Bouton de rafraîchissement
if st.sidebar.button("🔄 Rafraîchir les données"):
    st.cache_data.clear()

# Affichage date du jour
date_du_jour = datetime.today().strftime('%d/%m/%Y')

if uap_selection != "4M":
    st.markdown(f"<h2 style='text-align:center;'>Dashboard PIC - {uap_selection}</h2>", unsafe_allow_html=True)
    st.warning("Données non disponibles pour cette UAP.")
else:
    @st.cache_data(ttl=60)
    def load_data():
        return pd.read_excel("donnees_pic.xlsx", sheet_name="2025", engine="openpyxl", header=None)

    df = load_data()
    mois = df.iloc[2:14, 0].tolist()
    pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
    pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
    campagnes = df.iloc[1, 7:14].tolist()
    campagne_data = df.iloc[2:14, 7:14]
    campagne_data.columns = campagnes
    campagne_data.index = mois
    ruptures = int(df.iloc[1, 16])
    taux_adherence = int(df.iloc[1, 19])

    couleurs_personnalisees = {
        "MOUSSE": "#e74c3c",
        "TEXLINE": "#145A32",
        "PRIMETEX": "#F4D03F",
        "NERA": "#3498db",
        "TMAX": "#6E2C00",
        "SPORISOL": "#7f8c8d",
        "TARABUS": "#27ae60"
    }

    st.markdown("<h1 style='text-align:center; color:#000000;'>Dashboard PIC - 4M</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:right; font-size:14px;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    if mois_selectionne != "Depuis Janvier":
        col1.metric("PIC Réalisé", f"{pic_realise[mois_selectionne]} m²")
        col2.metric("PIC Prévu", f"{pic_prevu[mois_selectionne]} m²")
    else:
        col1.metric("PIC Réalisé", f"{pic_realise.sum()} m²")
        col2.metric("PIC Prévu", f"{pic_prevu.sum()} m²")
    col3.metric("Ruptures", f"{ruptures}")
    col4.metric("Adhérence S-1", f"{taux_adherence}%")

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Évolution mensuelle du PIC")
        df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
        fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True)
        fig_line.update_layout(height=300)
        st.plotly_chart(fig_line, use_container_width=True)

    with col6:
        st.markdown("### Répartition par campagne")
        if mois_selectionne != "Depuis Janvier":
            campagne_mois = campagne_data.loc[mois_selectionne]
        else:
            campagne_mois = campagne_data.sum()
        fig_pie = px.pie(values=campagne_mois.values, names=campagne_mois.index, color=campagne_mois.index,
                         color_discrete_map=couleurs_personnalisees, hole=0.4)
        fig_pie.update_traces(textinfo='label+value')
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### Heatmap des campagnes")
    if mois_selectionne == "Depuis Janvier":
        fig_heatmap = px.imshow(campagne_data.T, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
    else:
        campagne_mois_unique = pd.DataFrame(campagne_data.loc[mois_selectionne]).T
        fig_heatmap = px.imshow(campagne_mois_unique.T, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
    fig_heatmap.update_layout(height=300)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("### Taux d'adhérence S-1")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=taux_adherence,
        title=dict(text="Taux d'adhérence S-1"),
        gauge=dict(
            axis=dict(range=[0, 100]),
            bar=dict(color="#e84393"),
            steps=[
                dict(range=[0, 50], color="#f8c6d8"),
                dict(range=[50, 80], color="#f39cbb"),
                dict(range=[80, 100], color="#e84393")
            ]
        )
    ))
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)
