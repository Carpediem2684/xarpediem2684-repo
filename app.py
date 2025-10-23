import streamlit as st
import pandas as pd
import plotly.express as px
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

# Sidebar : sélection UAP et mois
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])

# Affichage date du jour
date_du_jour = datetime.today().strftime('%d/%m/%Y')

if uap_selection != "4M":
    st.markdown(f"<h2 style='text-align:center;'>Dashboard PIC - {uap_selection}</h2>", unsafe_allow_html=True)
    st.warning("Données non disponibles pour cette UAP.")
else:
    df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)
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

    st.markdown("<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - 4M</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:right; font-size:14px;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PIC Réalisé", f"{pic_realise[mois_selectionne]} km²")
    col2.metric("PIC Prévu", f"{pic_prevu[mois_selectionne]} km²")
    col3.metric("Ruptures cette semaine", f"{ruptures}")
    col4.metric("Adhérence S-1", f"{taux_adherence}%")

    # Nouveau graphique comparatif taux d'adhérence vs objectif
    adherence_data = df.iloc[2:14, [22, 23]]
    adherence_data.columns = ["Taux d'adhérence", "Objectif"]
    adherence_data.index = mois

    st.markdown("### Taux d'adhérence hebdomadaire vs Objectif")
    st.dataframe(adherence_data)

    fig_bar = px.bar(adherence_data, x=adherence_data.index, y=["Taux d'adhérence", "Objectif"],
                     barmode="group", title="Comparaison du taux d'adhérence par mois")
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

    # KPI écart à l'objectif avec couleur dynamique
    ecart = adherence_data.loc[mois_selectionne, "Taux d'adhérence"] - adherence_data.loc[mois_selectionne, "Objectif"]
    ecart_percent = round(ecart * 100, 1)
    couleur_ecart = "green" if ecart >= 0 else "red"
    st.markdown(f"<h4 style='color:{couleur_ecart};'>Écart à l'objectif : {ecart_percent}%</h4>", unsafe_allow_html=True)

    # Graphiques en grille
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Répartition par campagne")
        campagne_mois = campagne_data.loc[mois_selectionne]
        fig_pie = px.pie(values=campagne_mois.values, names=campagne_mois.index, color=campagne_mois.index,
                         color_discrete_map=couleurs_personnalisees, hole=0.4)
        fig_pie.update_traces(textinfo='label+value')
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col6:
        st.markdown("### Heatmap des campagnes")
        fig_heatmap = px.imshow(campagne_data.T, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
        fig_heatmap.update_layout(height=300)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Graphique PIC déplacé à la fin
    st.markdown("### Évolution mensuelle du PIC")
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True)
    fig_line.update_layout(height=300)
    st.plotly_chart(fig_line, use_container_width=True)
