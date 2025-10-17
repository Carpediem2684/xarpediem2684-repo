
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Dashboard PIC', layout='wide')

# CSS pour fond dégradé
st.markdown('''
    <style>
    body {
        background: linear-gradient(to right, #8e44ad, #e84393);
        color: white;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
''', unsafe_allow_html=True)

# Page d'accueil : sélection de l'UAP
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])

if uap_selection != "4M":
    st.markdown(f"<h2 style='text-align:center;'>Dashboard PIC - {uap_selection}</h2>", unsafe_allow_html=True)
    st.warning("Données non disponibles pour cette UAP.")
else:
    # Lecture du fichier Excel
df = pd.read_excel("Essai appli dashboard.xlsx", sheet_name="2025", engine="openpyxl", header=None)
mois = df.iloc[2:14, 0].tolist()
pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
campagnes = df.iloc[1, 7:14].tolist()
campagne_data = df.iloc[2:14, 7:14]
campagne_data.columns = campagnes
campagne_data.index = mois
ruptures = int(df.iloc[1, 16])
taux_adherence = int(df.iloc[1, 19])

    st.markdown("<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - 4M</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PIC Réalisé", f"{pic_realise[mois_selectionne]} m²")
    col2.metric("PIC Prévu", f"{pic_prevu[mois_selectionne]} m²")
    col3.metric("Ruptures", f"{ruptures}")
    col4.metric("Adhérence S-1", f"{taux_adherence}%")

    st.subheader("Évolution mensuelle du PIC")
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Répartition des m² réalisés par campagne")
    campagne_mois = campagne_data.loc[mois_selectionne]
    fig_pie = px.pie(values=campagne_mois.values, names=campagne_mois.index, color=campagne_mois.index, color_discrete_map={
        "MOUSSE": "#e74c3c",
        "TEXLINE": "#145A32",
        "PRIMETEX": "#F4D03F",
        "NERA": "#3498db",
        "TMAX": "#6E2C00",
        "SPORISOL": "#7f8c8d",
        "TARABUS": "#27ae60"
    }, hole=0.4)
    fig_pie.update_traces(textinfo='label+value')
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Heatmap des campagnes")
    fig_heatmap = px.imshow(campagne_data.T, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.subheader("Taux d'adhérence S-1")
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
    st.plotly_chart(fig_gauge, use_container_width=True)
