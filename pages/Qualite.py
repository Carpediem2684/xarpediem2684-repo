import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ------------------------------------------------
# Parse robustes de pourcentages style français
# ------------------------------------------------
def parse_percent(series: pd.Series) -> pd.Series:
    """
    Convertit '100,28 %' -> 100.28
    Gère espaces, NBSP, %, virgule FR.
    Si Excel fournit déjà des float, pd.to_numeric les conservera.
    Détecte l’échelle (0-1 vs 0-100) et la corrige si besoin.
    """
    s = (
        series.astype(str)
        .str.replace("\u00A0", "", regex=False)   # NBSP
        .str.replace(" ", "", regex=False)        # espaces
        .str.replace("%", "", regex=False)        # signe %
        .str.replace(",", ".", regex=False)       # virgule -> point
        .str.strip()
    )
    v = pd.to_numeric(s, errors="coerce")

    # Si Excel a stocké 0.9828 (= 98.28%), on remet à l’échelle.
    # Heuristique simple : médiane <= 1.5 -> on multiplie par 100.
    med = v.dropna().median()
    if pd.notna(med) and med <= 1.5:
        v = v * 100.0

    # Valeurs NAN -> 0, on ne clippe PAS le rendement (il peut dépasser 100 ponctuellement)
    return v.fillna(0.0)


def show_qualite():
    # --- Bouton retour menu ---
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("⬅️ Retour Menu"):
            st.session_state.page = "menu"
            return

    st.title("📊 Qualité – U4M (source : Rdt Réel Excel)")

    # --- Lecture Excel (lecture seule) ---
    file_path = "Essai appli dashboard (1).xlsx"

    # On lit exactement A→G à partir de A47 (entêtes en ligne 47)
    df = pd.read_excel(
        file_path,
        sheet_name="2025",
        engine="openpyxl",
        header=46,        # ligne 47 = entêtes
        usecols="A:G"
    ).copy()

    # Renomme explicitement selon ta capture (A→G)
    df.columns = [
        "Libelle ligne",            # A
        "Date début OF",            # B
        "Quantité demandée",        # C
        "Quantité IC",              # D
        "Rdt Réel",                 # E
        "Rebuts budget",            # F
        "Rebuts en écart vs budget" # G
    ]

    # Nettoyage minimal des noms (si Excel ajoute des NBSP)
    df.columns = [c.strip().replace("\u00A0", " ") for c in df.columns]

    # --- Rendement depuis la colonne E (en %) ---
    df["Rdt Excel (%)"] = parse_percent(df["Rdt Réel"])

    # --- Rebut = 100 - Rendement (borné 0-100 pour l’affichage du rebut uniquement) ---
    df["Rebut Excel (%)"] = (100.0 - df["Rdt Excel (%)"]).clip(lower=0, upper=100)

    # --- Sélection de ligne ---
    lignes = sorted(df["Libelle ligne"].dropna().unique())
    if not lignes:
        st.error("Aucune 'Libelle ligne' détectée dans la plage A47:G (onglet '2025').")
        return

    ligne_sel = st.selectbox("Choisir une ligne :", lignes)
    dfl = df[df["Libelle ligne"] == ligne_sel].copy()
    if dfl.empty:
        st.info("Aucune donnée pour cette ligne.")
        return

    # --- KPI (moyennes) ---
    rdt_moy = dfl["Rdt Excel (%)"].mean()
    reb_moy = dfl["Rebut Excel (%)"].mean()

    k1, k2 = st.columns(2)
    k1.metric("Fabrication moyenne (Excel)", f"{rdt_moy:.2f} %")
    k2.metric("Rebut moyen (Excel)",        f"{reb_moy:.2f} %")

    # --- Graphiques ---
    dfl = dfl.reset_index(drop=True)
    dfl["OF #"] = dfl.index + 1

    fig_rdt = go.Figure(go.Bar(
        x=dfl["OF #"],
        y=dfl["Rdt Excel (%)"],
        text=[f"{v:.1f} %" for v in dfl["Rdt Excel (%)"]],
        textposition="outside",
        marker_color="#2e8b57",
        hovertemplate="OF #%{x}<br>Rdt: %{y:.2f}%<extra></extra>"
    ))
    fig_rdt.update_layout(
        title=f"Rendement (Excel) – {ligne_sel}",
        xaxis_title="OF #",
        yaxis_title="Rendement (%)",
        height=420
    )

    fig_reb = go.Figure(go.Bar(
        x=dfl["OF #"],
        y=dfl["Rebut Excel (%)"],
        text=[f"{v:.1f} %" for v in dfl["Rebut Excel (%)"]],
        textposition="outside",
        marker_color="#cd5c5c",
        hovertemplate="OF #%{x}<br>Rebut: %{y:.2f}%<extra></extra>"
    ))
    fig_reb.update_layout(
        title=f"Rebut (Excel) – {ligne_sel}",
        xaxis_title="OF #",
        yaxis_title="Rebut (%)",
        height=420
    )

    g1, g2 = st.columns(2)
    g1.plotly_chart(fig_rdt, use_container_width=True)
    g2.plotly_chart(fig_reb, use_container_width=True)

    # --- Tableau détaillé (on n'altère pas Excel) ---
    st.subheader("📄 Détail des OF (source Excel)")
    colonnes_aff = [
        "Libelle ligne", "Date début OF",
        "Quantité demandée", "Quantité IC",
        "Rdt Réel", "Rdt Excel (%)",
        "Rebuts budget", "Rebuts en écart vs budget",
        "Rebut Excel (%)"
    ]
    colonnes_aff = [c for c in colonnes_aff if c in dfl.columns]
    st.dataframe(dfl[colonnes_aff], use_container_width=True)
