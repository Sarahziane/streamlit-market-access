
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Impact Économique - Perspective Laboratoire", layout="wide")

st.title("💊 Simulation Médico-Économique - Perspective Laboratoire (Produit BPCOff)")

# Sidebar - Paramètres
st.sidebar.header("🔧 Paramètres de simulation")
population = st.sidebar.slider("Population cible", 10000, 100000, 50000, step=5000)
prix_traitement = st.sidebar.number_input("Prix annuel du traitement (€)", value=2500)
cout_interne = st.sidebar.number_input("Coût interne / patient (€)", value=600)
taux_adoption = st.sidebar.slider("Taux d’adoption (%)", 0, 100, 40)
horizon = st.sidebar.slider("Horizon (années)", 1, 5, 3)

# Paramètres payeur
st.sidebar.markdown("---")
st.sidebar.header("📉 Perspective payeur")
cout_exacerbation = st.sidebar.number_input("Coût exacerbation (€)", value=3200)
reduction_exacerbation = st.sidebar.slider("Réduction exacerbations (%)", 0, 100, 25)

# Calculs
nb_patients = population * (taux_adoption / 100)
gain_par_patient = cout_exacerbation * (reduction_exacerbation / 100)
ca_total = nb_patients * prix_traitement
cout_total_interne = nb_patients * cout_interne
marge_brute = ca_total - cout_total_interne
roi_labo = (marge_brute / cout_total_interne) * 100 if cout_total_interne > 0 else 0

economie_totale = nb_patients * gain_par_patient
impact_net_payeur = economie_totale - ca_total
roi_payeur = (impact_net_payeur / ca_total) * 100 if ca_total > 0 else 0

# KPI Cards
st.subheader("📌 Résumé économique")
col1, col2, col3 = st.columns(3)
col1.metric("👥 Patients traités", f"{int(nb_patients):,}")
col2.metric("💼 Marge brute totale", f"{int(marge_brute):,} €", delta=f"{roi_labo:.1f}% ROI labo")
col3.metric("🏥 ROI payeur", f"{roi_payeur:.1f} %", delta=f"{int(impact_net_payeur):,} € impact net")

st.markdown("---")

# Message final pour le laboratoire
st.subheader("🧾 Interprétation")
if marge_brute > 0:
    st.success("✅ Le traitement BPCOff est rentable pour le laboratoire sur la base des paramètres simulés.")
else:
    st.warning("⚠️ Le traitement BPCOff génère une perte nette pour le laboratoire dans ce scénario.")

# Graphique ROI labo vs ROI payeur
st.subheader("📊 ROI Laboratoire vs Payeur")
df_roi = pd.DataFrame({
    "Indicateur": ["ROI Labo (%)", "ROI Payeur (%)"],
    "Valeur": [roi_labo, roi_payeur]
})
fig_bar = px.bar(df_roi, x="Indicateur", y="Valeur", text="Valeur", color="Indicateur", title="Comparatif des ROI")
st.plotly_chart(fig_bar, use_container_width=True)

# Marge cumulée sur horizon
st.subheader("📈 Marge cumulée sur horizon")
years = list(range(1, horizon + 1))
marge_par_an = [marge_brute * (i / horizon) for i in years]
fig_line = px.line(x=years, y=marge_par_an, markers=True, labels={"x": "Année", "y": "Marge cumulée (€)"}, title="Projection de la marge cumulée (labo)")
st.plotly_chart(fig_line, use_container_width=True)

# Téléchargement CSV
st.subheader("📥 Exporter les résultats")
df_export = pd.DataFrame({
    "Paramètre": ["Population", "Prix traitement", "Coût interne", "Nb patients", "CA total", "Marge brute", "ROI labo (%)", "Impact net payeur", "ROI payeur (%)"],
    "Valeur": [population, prix_traitement, cout_interne, int(nb_patients), int(ca_total), int(marge_brute), round(roi_labo, 2), int(impact_net_payeur), round(roi_payeur, 2)]
})
csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button("📄 Télécharger les résultats (CSV)", data=csv, file_name="resultats_labo.csv", mime="text/csv")
