
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Dashboard PIC', layout='wide')
st.title('Dashboard PIC')

mois = {mois}
pic_realise = pd.Series({pic_realise.tolist()}, index=mois)
pic_prevu = pd.Series({pic_prevu.tolist()}, index=mois)
campagnes = {campagnes}
campagne_data = pd.DataFrame({campagne_data.to_dict()}, index=mois)
ruptures = {ruptures}
taux_adherence = {taux_adherence}

mois_selectionne = st.selectbox("Choisir un mois :", mois)
pic_mois_realise = pic_realise[mois_selectionne]
pic_mois_prevu = pic_prevu[mois_selectionne]
campagne_mois = campagne_data.loc[mois_selectionne]

tabs = st.tabs(["KPI", "Répartition", "Évolution", "Heatmap", "Ruptures", "Adhérence"])

with tabs[0]:
    col1, col2 = st.columns(2)
    col1.metric("PIC Réalisé", f"{pic_mois_realise} m²")
    col2.metric("PIC Prévu", f"{pic_mois_prevu} m²")

with tabs[1]:
    st.subheader("Répartition des m² réalisés par campagne")
    fig_pie = px.pie(values=campagne_mois.values, names=campagne_mois.index)
    st.plotly_chart(fig_pie, use_container_width=True)

with tabs[2]:
    st.subheader("Évolution mensuelle du PIC")
    df_evol = pd.DataFrame({"Mois": mois, "PIC Réalisé": pic_realise.values, "PIC Prévu": pic_prevu.values})
    fig_line = px.line(df_evol, x="Mois", y=["PIC Réalisé", "PIC Prévu"], markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with tabs[3]:
    st.subheader("Heatmap des m² réalisés par campagne et mois")
    fig_heatmap = px.imshow(campagne_data.T, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tabs[4]:
    st.subheader("Ruptures client")
    st.write(f"Nombre de ruptures : {ruptures}")

with tabs[5]:
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
