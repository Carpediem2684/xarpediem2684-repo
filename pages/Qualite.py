import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def show_qualite():

    # --- Bouton retour menu ---
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Retour Menu"):
            st.session_state.page = "menu"
            return

    st.title("📊 Suivi Qualité – U4M")

    file_path = "Essai appli dashboard (1).xlsx"

    # --- Lecture du tableau à partir de A47 ---
    df = pd.read_excel(
        file_path,
        sheet_name="2025",
        engine="openpyxl",
        header=46,       # ligne 47 comme en-tête
        usecols="A:G"    # colonnes A → G
    )

    # ----------------------------------------
    # 1️⃣ Vérification des colonnes détectées
    # ----------------------------------------
    # (optionnel pour debug)
    # st.write("Colonnes détectées :", df.columns.tolist())

    df.columns = [
        "Libelle ligne",
        "Date début OF",
        "Quantité demandée",
        "Quantité IC",
        df.columns[4],           # nom réel de la colonne Rdt Réel (qui peut varier)
        "Rebuts budget",
        "Rebuts écart"
    ]

    # ---------------------------------------------------------
    # 2️⃣ Identification dynamique de la colonne "Rdt Réel"
    # ---------------------------------------------------------
    col_rdt = [c for c in df.columns if "Rdt" in c or "rend" in c.lower()][0]

    # ---------------------------------------------------------
    # 3️⃣ Nettoyage + conversion correcte du rendement
    # ---------------------------------------------------------
    df[col_rdt] = (
        df[col_rdt]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
        .str.strip()
    )

    df[col_rdt] = pd.to_numeric(df[col_rdt], errors="coerce").fillna(0)

    # ---------------------------------------------------------
    # 4️⃣ Calcul du rebut réel = 100 - rendement
    # ---------------------------------------------------------
    df["Rebut Réel (%)"] = 100 - df[col_rdt]

    # ---------------------------------------------------------
    # 5️⃣ Sélection de la ligne (LIGNE 1, IMPRIMERIE, LIGNE 2)
    # ---------------------------------------------------------
    lignes = sorted(df["Libelle ligne"].dropna().unique())

    ligne_sel = st.selectbox("Choisir une ligne :", lignes)

    df_ligne = df[df["Libelle ligne"] == ligne_sel]

    # ---------------------------------------------------------
    # 6️⃣ Calculs des moyennes
    # ---------------------------------------------------------
    rdt_moyen = df_ligne[col_rdt].mean()
    rebut_moyen = df_ligne["Rebut Réel (%)"].mean()

    # ---------------------------------------------------------
    # 7️⃣ KPIs
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)

    col1.metric("Fabrication moyenne du jour", f"{rdt_moyen:.2f} %")
    col2.metric("Rebut moyen du jour", f"{rebut_moyen:.2f} %")

    # ---------------------------------------------------------
    # 8️⃣ Graphique rendement
    # ---------------------------------------------------------
    fig_rdt = go.Figure(go.Bar(
        x=df_ligne["Quantité demandée"],
        y=df_ligne[col_rdt],
        text=[f"{v:.1f} %" for v in df_ligne[col_rdt]],
        textposition="outside",
        marker_color="green"
    ))

    fig_rdt.update_layout(
        title=f"Rendement réel – {ligne_sel}",
        xaxis_title="Quantité demandée",
        yaxis_title="Rendement (%)",
        height=400
    )

    st.plotly_chart(fig_rdt, use_container_width=True)

    # ---------------------------------------------------------
    # 9️⃣ Graphique rebut
    # ---------------------------------------------------------
    fig_rebut = go.Figure(go.Bar(
        x=df_ligne["Quantité demandée"],
        y=df_ligne["Rebut Réel (%)"],
        text=[f"{v:.1f} %" for v in df_ligne["Rebut Réel (%)"]],
        textposition="outside",
        marker_color="red"
    ))

    fig_rebut.update_layout(
        title=f"Rebut réel – {ligne_sel}",
        xaxis_title="Quantité demandée",
        yaxis_title="Rebut (%)",
        height=400
    )

    st.plotly_chart(fig_rebut, use_container_width=True)

    # ---------------------------------------------------------
    # 🔟 Tableau récapitulatif
    # ---------------------------------------------------------
    st.subheader("📄 Détail des OF")
    st.dataframe(df_ligne, use_container_width=True)