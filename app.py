
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Dashboard', layout='wide')
st.title('Dashboard')

# Lecture du fichier Excel
df = pd.read_excel("Essai appli dashboard.xlsx", sheet_name="2025", engine="openpyxl", header=None)

# Extraction des données
mois = df.iloc[2:14, 0].tolist()
pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
campagnes = df.iloc[1, 7:14].tolist()
campagne_data = df.iloc[2:14, 7:14]
campagne_data.columns = campagnes
campagne_data.index = mois
ruptures = int(df.iloc[1, 16])
taux_adherence = int(df.iloc[1, 19])

# Couleurs personnalisées pour les campagnes
couleurs_personnalisees = {
    "MOUSSE": "red",
    "TEXLINE": "darkgreen",
    "PRIMETEX": "yellow",
    "NERA": "blue",
    "TMAX": "brown",
    "SPORISOL": "gray",
    "TARABUS": "lightgreen"
}

# Sélection du mois
mois_selectionne = st.selectbox("Choisir un mois :", mois)
pic_mois_realise = pic_realise.loc[mois_selectionne]
pic_mois_prevu = pic_prevu.loc[mois_selectionne]
campagne_mois = campagne_data.loc[mois_selectionne]

# Onglets
tabs = st.tabs(["KPI & Évolution", "Répartition", "Heatmap", "Ruptures", "Adhérence"])

with tabs[0]:
    col1, col2 = st.columns(2)
    col1.metric("PIC Réalisé", f"{pic_mois_realise} m²")
    col2.metric("PIC Prévu", f"{pic_mois_prevu} m²")

    st.subheader("Évolution mensuelle du PIC")
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with tabs[1]:
    st.subheader("Répartition des km² réalisés par campagne")
    fig_pie = px.pie(
        values=campagne_mois.values,
        names=campagne_mois.index,
        color=campagne_mois.index,
        color_discrete_map=couleurs_personnalisees,
        hole=0.3
    )
    fig_pie.update_traces(textinfo='label+value', textfont_size=14)
    st.plotly_chart(fig_pie, use_container_width=True)

with tabs[2]:
    st.subheader("Heatmap des m² réalisés par campagne et mois")
    fig_heatmap = px.imshow(campagne_data.T, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tabs[3]:
    st.subheader("Ruptures client")
    st.write(f"Nombre de ruptures : {ruptures}")

with tabs[4]:
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
