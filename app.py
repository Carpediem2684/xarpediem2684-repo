import streamlit as st
import pandas as pd
import plotly.express as px
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
    # Lecture du fichier Excel
    df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)
    mois = df.iloc[2:14, 0].tolist()
    pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
    pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
    ruptures = int(df.iloc[1, 16])

    st.markdown("<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - 4M</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:right; font-size:14px;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("PIC Réalisé", f"{pic_realise[mois_selectionne]} km²")
    col2.metric("PIC Prévu", f"{pic_prevu[mois_selectionne]} km²")
    col3.metric("Ruptures cette semaine", f"{ruptures}")

    # ✅ Graphique hebdomadaire du taux d'adhérence
    weekly_data = df.iloc[2:51, [22]]
    weekly_data.columns = ["Taux d'adhérence"]
    weekly_data.index = [f"Semaine {int(df.iloc[i, 21])}" for i in range(2, 51)]
    weekly_data["Taux d'adhérence"] = (weekly_data["Taux d'adhérence"] * 100).round(1)

    st.markdown("### Évolution hebdomadaire du taux d'adhérence")
    fig_weekly = px.line(weekly_data, x=weekly_data.index, y="Taux d'adhérence",
                         title="Évolution hebdomadaire du taux d'adhérence",
                         markers=True)
    fig_weekly.update_layout(height=400, yaxis_title="% d'adhérence")
    st.plotly_chart(fig_weekly, use_container_width=True)

    # ✅ Graphique PIC en bas
    st.markdown("### Évolution mensuelle du PIC")
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True)
    fig_line.update_layout(height=300)
    st.plotly_chart(fig_line, use_container_width=True)
