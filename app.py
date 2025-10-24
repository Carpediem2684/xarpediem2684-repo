
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title='Dashboard PIC', layout='wide')

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
    h1, h4, h3, h2, p, div {
        font-weight: bold !important;
    }
    .metric-label {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.sidebar.title("Sélection UAP")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])

date_du_jour = datetime.today().strftime('%d/%m/%Y')

st.markdown(f"<h1 style='text-align:center; color:#ffffff;'>Dashboard PIC - {uap_selection}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:right; font-size:16px; font-weight:bold;'>Date du jour : {date_du_jour}</p>", unsafe_allow_html=True)

if uap_selection == "4M":
    df = pd.read_excel("Essai appli dashboard (1).xlsx", sheet_name="2025", engine="openpyxl", header=None)

    mois = df.iloc[2:14, 0].tolist()
    pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
    pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
    ruptures = int(df.iloc[1, 16])

    raw_adherence = pd.to_numeric(df.iloc[1, 22], errors="coerce")
    taux_adherence = (raw_adherence * 100) if pd.notna(raw_adherence) else 0

    st.markdown(f"<h4 style='color:white;'>Taux d'adhérence S-1 : {taux_adherence:.1f}%</h4>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-label'>PIC Réalisé</div>", unsafe_allow_html=True)
    col1.metric("", f"{pic_realise[mois_selectionne]} km²")
    col2.markdown(f"<div class='metric-label'>PIC Prévu</div>", unsafe_allow_html=True)
    col2.metric("", f"{pic_prevu[mois_selectionne]} km²")
    col3.markdown(f"<div class='metric-label'>Ruptures cette semaine</div>", unsafe_allow_html=True)
    col3.metric("", f"{ruptures}")

    campagnes = df.iloc[1, 7:14].tolist()
    campagne_data = df.iloc[2:14, 7:14]
    campagne_data.columns = campagnes
    campagne_data.index = mois
    campagne_mois = campagne_data.loc[mois_selectionne]
    campagne_mois["AUTRES"] = 80

    weekly_data = df.iloc[2:51, [21, 22]]
    weekly_data.columns = ["Semaine", "Taux d'adhérence"]
    weekly_data.dropna(inplace=True)
    weekly_data["Taux d'adhérence"] = pd.to_numeric(weekly_data["Taux d'adhérence"], errors="coerce")
    weekly_data["Taux d'adhérence"] = (weekly_data["Taux d'adhérence"] * 100).round(1)
    weekly_data["Semaine"] = weekly_data["Semaine"].astype(int)

    semaines_completes = list(range(1, 51))
    colors = ["green" if val >= 85 else "red" for val in weekly_data["Taux d'adhérence"]]

    st.markdown("### Répartition par campagne et évolution du taux d'adhérence")
    col_gauche, col_droite = st.columns(2)

    with col_gauche:
        st.markdown("#### Répartition par campagne")
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=campagne_mois.index,
                values=campagne_mois.values,
                hole=0.4,
                textinfo='label+percent+value',
                hoverinfo='label+percent+value'
            )
        ])
        fig_pie.update_layout(height=400, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_droite:
        st.markdown("#### Évolution hebdomadaire du taux d'adhérence")
        fig_weekly = go.Figure()
        fig_weekly.add_trace(go.Scatter(
            x=weekly_data["Semaine"],
            y=weekly_data["Taux d'adhérence"],
            mode='markers+lines+text',
            marker=dict(color=colors, size=10),
            name="Taux d'adhérence",
            text=[f"{val:.1f}%" for val in weekly_data["Taux d'adhérence"]],
            textposition="top center"
        ))
        fig_weekly.add_trace(go.Scatter(
            x=semaines_completes,
            y=[85]*len(semaines_completes),
            mode='lines',
            name="Objectif",
            line=dict(dash='dash', color='blue')
        ))
        fig_weekly.update_layout(
            height=400,
            xaxis_title="Semaine",
            yaxis_title="% d'adhérence",
            xaxis=dict(tickmode='array', tickvals=semaines_completes)
        )
        st.plotly_chart(fig_weekly, use_container_width=True)

    st.markdown("### Évolution mensuelle du PIC")
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=df_evol["Mois"], y=df_evol["PIC Réalisé"], mode='lines+markers', name="PIC Réalisé"))
    fig_line.add_trace(go.Scatter(x=df_evol["Mois"], y=df_evol["PIC Prévu"], mode='lines+markers', name="PIC Prévu"))
    fig_line.update_layout(height=300, title="PIC mensuel", xaxis_title="Mois", yaxis_title="Surface (km²)")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### Heatmap des campagnes")
    fig_heatmap = go.Figure(data=go.Heatmap(z=campagne_data.values, x=campagne_data.columns, y=campagne_data.index, colorscale='Viridis'))
    fig_heatmap.update_layout(height=300)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ✅ Nouvelle jauge interactive basée sur PIC Réalisé et PIC Prévu
    st.markdown("### Simulation des campagnes à venir")
    if "current_value" not in st.session_state:
        st.session_state.current_value = pic_realise[mois_selectionne]

    if st.button("Instant présent"):
        st.session_state.current_value = pic_realise[mois_selectionne]

    for campagne, val in campagne_mois.items():
        if val > 0:
            if st.button(campagne):
                st.session_state.current_value += val
                if st.session_state.current_value > pic_prevu[mois_selectionne]:
                    st.session_state.current_value = pic_prevu[mois_selectionne]

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
