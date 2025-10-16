
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration moderne et centrée
st.set_page_config(page_title='Dashboard PIC', layout='centered')

# Titre stylisé
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50;'>📊 Dashboard PIC 2025</h1>
    <hr style='border:1px solid #ccc;'>
""", unsafe_allow_html=True)

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

# Couleurs personnalisées
couleurs_personnalisees = {
    "MOUSSE": "#e74c3c",
    "TEXLINE": "#145A32",
    "PRIMETEX": "#F4D03F",
    "NERA": "#3498db",
    "TMAX": "#6E2C00",
    "SPORISOL": "#7f8c8d",
    "TARABUS": "#27ae60"
}

# Sélection du mois
mois_selectionne = st.selectbox("🗓️ Choisir un mois :", mois)
pic_mois_realise = pic_realise.loc[mois_selectionne]
pic_mois_prevu = pic_prevu.loc[mois_selectionne]
campagne_mois = campagne_data.loc[mois_selectionne]

# Onglets
tabs = st.tabs(["📈 KPI & Évolution", "📊 Répartition", "🗺️ Heatmap", "🚨 Ruptures", "✅ Adhérence"])

with tabs[0]:
    st.markdown("### 🔍 Indicateurs clés", unsafe_allow_html=True)
    st.metric("PIC Réalisé", f"{pic_mois_realise} m²")
    st.metric("PIC Prévu", f"{pic_mois_prevu} m²")

    st.markdown("### 📈 Évolution mensuelle du PIC", unsafe_allow_html=True)
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True, color_discrete_map={"PIC Réalisé": "#2ecc71", "PIC Prévu": "#e67e22"})
    fig_line.update_layout(template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

with tabs[1]:
    st.markdown("### 📊 Répartition des m² réalisés par campagne", unsafe_allow_html=True)
    fig_pie = px.pie(
        values=campagne_mois.values,
        names=campagne_mois.index,
        color=campagne_mois.index,
        color_discrete_map=couleurs_personnalisees,
        hole=0.4
    )
    fig_pie.update_traces(textinfo='label+value', textfont_size=14)
    fig_pie.update_layout(template="plotly_white")
    st.plotly_chart(fig_pie, use_container_width=True)

with tabs[2]:
    st.markdown("### 🗺️ Heatmap des m² réalisés par campagne et mois", unsafe_allow_html=True)
    fig_heatmap = px.imshow(campagne_data.T, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
    fig_heatmap.update_layout(template="plotly_white")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tabs[3]:
    st.markdown("### 🚨 Ruptures client", unsafe_allow_html=True)
    st.write(f"Nombre de ruptures : {ruptures}")

with tabs[4]:
    st.markdown("### ✅ Taux d'adhérence S-1", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=taux_adherence,
        title=dict(text="Taux d'adhérence S-1"),
        gauge=dict(
            axis=dict(range=[0, 100]),
            bar=dict(color="#2c3e50"),
            steps=[
                dict(range=[0, 50], color="#ecf0f1"),
                dict(range=[50, 80], color="#bdc3c7"),
                dict(range=[80, 100], color="#2ecc71")
            ]
        )
    ))
    fig_gauge.update_layout(template="plotly_white")
    st.plotly_chart(fig_gauge, use_container_width=True)
