import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================
# CONFIGURATION & THEME
# =========================
st.set_page_config(page_title="Dashboard PIC", layout="wide")

# CSS pour améliorer le design
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1f2937, #4b5563);
    color: #f9fafb;
}
h1, h2, h3 {
    font-family: 'Roboto', sans-serif;
    color: #ffffff;
}
.metric-container {
    background-color: #374151;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    font-weight: bold;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Logo_Gerflor.svg/2560px-Logo_Gerflor.svg.png", width=150)
st.markdown("<h1 style='text-align:center;'>📊 Dashboard PIC - Gerflor</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:right; font-size:16px;'>Date : {datetime.today().strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Paramètres")
uap_selection = st.sidebar.selectbox("Choisir une UAP", ["4M", "2M", "P2000", "KLAM"])
mois_selectionne = st.sidebar.selectbox("Choisir un mois", ["Janvier", "Février", "Mars", "Avril"])

# Mode Dark/Light
theme = st.sidebar.radio("🎨 Thème", ["Dark", "Light"])
if theme == "Light":
    st.markdown("""
    <style>
    body { background: #f9fafb; color: #111827; }
    h1, h2, h3 { color: #111827; }
    .metric-container { background-color: #e5e7eb; color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# IMPORT DONNÉES
# =========================
file_path = 'Essai appli dashboard (1).xlsx'
df = pd.read_excel(file_path, sheet_name='2025', engine='openpyxl', header=None)

# Extraction des données
mois = df.iloc[2:14, 0].tolist()
campagnes = df.iloc[1, 25:34].tolist()
pic_realise = pd.Series(pd.to_numeric(df.iloc[2:14, 1], errors='coerce').fillna(0).astype(int).values, index=mois)
pic_prevu = pd.Series(pd.to_numeric(df.iloc[2:14, 2], errors='coerce').fillna(0).astype(int).values, index=mois)
ruptures = int(df.iloc[1, 16])
raw_adherence = pd.to_numeric(df.iloc[1, 22], errors='coerce')
taux_adherence = (raw_adherence * 100) if pd.notna(raw_adherence) else 0
adherence_s1 = pd.to_numeric(df.iloc[1, 19], errors='coerce')

# =========================
# TABS POUR STRUCTURE
# =========================
tab1, tab2, tab3, tab4 = st.tabs(["📈 KPI", "📊 Graphiques", "🔥 Heatmap", "🎯 Jauge & GIF"])

# =========================
# TAB 1 : KPI
# =========================
with tab1:
    st.subheader("Indicateurs clés")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ PIC Réalisé", f"{pic_realise[mois_selectionne]} km²")
    col2.metric("📌 PIC Prévu", f"{pic_prevu[mois_selectionne]} km²")
    col3.metric("⚠ Ruptures", f"{ruptures}")
    col4.metric("📊 Taux d'adhérence S-1", f"{adherence_s1:.1f}%" if pd.notna(adherence_s1) else "N/A")

    # Objectif journalier recalculé
    st.markdown("### 📅 Objectif Journalier")
    start_date = datetime.today().replace(day=1)
    end_date = start_date + timedelta(days=30)
    nb_days = len([d for d in pd.date_range(start_date, end_date) if d.weekday() < 5])
    pic_journalier = pic_prevu[mois_selectionne] / nb_days
    st.info(f"Objectif journalier : {pic_journalier:.1f} km²")

# =========================
# TAB 2 : GRAPHIQUES
# =========================
with tab2:
    st.subheader("Répartition par campagne")
    campagne_labels = df.iloc[1, 6:14].tolist()
    campagne_values = pd.to_numeric(df[df.iloc[:, 0] == mois_selectionne].iloc[0, 6:14], errors='coerce').fillna(0)
    fig_pie = go.Figure(data=[go.Pie(labels=campagne_labels, values=campagne_values, hole=0.4)])
    fig_pie.update_traces(pull=[0.05]*len(campagne_labels))  # Animation
    fig_pie.update_layout(title="Répartition par campagne", height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Évolution hebdomadaire du taux d'adhérence")
    weekly_data = df.iloc[2:51, [21, 22]]
    weekly_data.columns = ["Semaine", "Taux d'adhérence"]
    weekly_data.dropna(inplace=True)
    weekly_data["Taux d'adhérence"] = (pd.to_numeric(weekly_data["Taux d'adhérence"], errors="coerce") * 100).round(1)
    fig_weekly = go.Figure()
    fig_weekly.add_trace(go.Scatter(x=weekly_data["Semaine"], y=weekly_data["Taux d'adhérence"], mode='lines+markers',
                                    line=dict(color="royalblue", width=3), marker=dict(size=10, color="orange")))
    fig_weekly.update_layout(title="Taux d'adhérence hebdo", height=400)
    st.plotly_chart(fig_weekly, use_container_width=True)

# =========================
# TAB 3 : HEATMAP
# =========================
with tab3:
    st.subheader("Heatmap des campagnes")
    campagne_data_heatmap = df.iloc[2:14, 6:14]
    campagne_data_heatmap.columns = campagne_labels
    campagne_data_heatmap.index = mois
    campagne_data_heatmap = campagne_data_heatmap.apply(pd.to_numeric, errors='coerce').fillna(0)
    fig_heatmap = go.Figure(data=go.Heatmap(z=campagne_data_heatmap.values, x=campagne_data_heatmap.columns, y=campagne_data_heatmap.index, colorscale='Viridis'))
    fig_heatmap.update_layout(title="Heatmap des campagnes", height=600)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# =========================
# TAB 4 : JAUGE & GIF
# =========================
with tab4:
    st.subheader("Progression PIC")
    fig_dynamic = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pic_realise[mois_selectionne],
        title={'text': f"Progression PIC ({mois_selectionne})"},
        gauge={
            'axis': {'range': [0, pic_prevu[mois_selectionne]*1.2]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, pic_prevu[mois_selectionne]*0.85], 'color': "lightgreen"},
                {'range': [pic_prevu[mois_selectionne]*0.85, pic_prevu[mois_selectionne]], 'color': "yellow"},
                {'range': [pic_prevu[mois_selectionne], pic_prevu[mois_selectionne]*1.2], 'color': "lightgrey"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'value': pic_prevu[mois_selectionne]}
        }
    ))
    st.plotly_chart(fig_dynamic, use_container_width=True)

    # GIF si dépassement
    if pic_realise[mois_selectionne] > pic_prevu[mois_selectionne]:
        st.image("GIF_20251219_081101_562.gif", use_container_width=True)

# =========================
# SECTION CAMPAGNES RESTANTES
# =========================
st.markdown("### 📦 Campagnes restantes du mois")
cols = st.columns(len(campagnes) + 1)
if cols[0].button("🔄 Instant T"):
    st.session_state.current_value = pic_realise[mois_selectionne]
    st.session_state.campagne_clicks = {campagne: False for campagne in campagnes}
    st.session_state.bar_color = "darkblue"


for i, campagne in enumerate(campagnes):
    # Utilisation de l'index positionnel pour éviter KeyError
    index_pos = mois.index(mois_selectionne)
    val = df.iloc[2:14, 25 + i].apply(pd.to_numeric, errors='coerce').fillna(0).iloc[index_pos]



    if val > 0:
        clicked = st.session_state.get("campagne_clicks", {}).get(campagne, False)
        indicator = "🟢" if not clicked else "🔴"
        if cols[i + 1].button(f"{indicator} {campagne}"):
            if not clicked:
                st.session_state.campagne_clicks[campagne] = True
                st.session_state.current_value += val
                st.session_state.bar_color = "blue"

# =========================
# JAUGE DYNAMIQUE
# =========================
fig_dynamic = go.Figure(go.Indicator(
    mode="gauge+number",
    value=st.session_state.get("current_value", pic_realise[mois_selectionne]),
    title={'text': f"Progression PIC ({mois_selectionne})"},
    gauge={
        'axis': {'range': [0, pic_prevu[mois_selectionne] * 1.2]},
        'bar': {'color': st.session_state.get("bar_color", "darkblue")},
        'steps': [
            {'range': [0, pic_prevu[mois_selectionne] * 0.85], 'color': "lightgreen"},
            {'range': [pic_prevu[mois_selectionne] * 0.85, pic_prevu[mois_selectionne]], 'color': "yellow"},
            {'range': [pic_prevu[mois_selectionne], pic_prevu[mois_selectionne] * 1.2], 'color': "lightgrey"}
        ],
        'threshold': {'line': {'color': "red", 'width': 4}, 'value': pic_prevu[mois_selectionne]}
    }
))
st.plotly_chart(fig_dynamic, use_container_width=True)

# Message dépassement
if st.session_state.get("current_value", pic_realise[mois_selectionne]) > pic_prevu[mois_selectionne]:
    st.markdown(
        f"<p style='color:red; font-size:18px; font-weight:bold;'>⚠ Dépassement du PIC prévu : {st.session_state.get('current_value')} km²</p>",
        unsafe_allow_html=True
    )

# =========================
# HEATMAP AMÉLIORÉE
# =========================
campagne_data_heatmap = df.iloc[2:14, 6:14]
campagne_data_heatmap.columns = df.iloc[1, 6:14].tolist()
campagne_data_heatmap.index = mois
campagne_data_heatmap = campagne_data_heatmap.apply(pd.to_numeric, errors='coerce').fillna(0)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=campagne_data_heatmap.values,
    x=campagne_data_heatmap.columns,
    y=campagne_data_heatmap.index,
    colorscale='Viridis',
    colorbar=dict(title="Valeur"),
    zmin=0,
    zmax=campagne_data_heatmap.values.max(),
    hoverongaps=False
))

annotations = []
for i, mois_val in enumerate(campagne_data_heatmap.index):
    for j, campagne_val in enumerate(campagne_data_heatmap.columns):
        value = campagne_data_heatmap.iloc[i, j]
        annotations.append(dict(
            x=campagne_val,
            y=mois_val,
            text=str(value),
            showarrow=False,
            font=dict(color="white" if value < campagne_data_heatmap.values.max() / 2 else "black", size=10)
        ))

fig_heatmap.update_layout(
    title="Heatmap des campagnes (améliorée)",
    height=600,
    annotations=annotations,
    xaxis=dict(title="Campagnes", tickangle=-45),
    yaxis=dict(title="Mois")
)
st.plotly_chart(fig_heatmap, use_container_width=True)
