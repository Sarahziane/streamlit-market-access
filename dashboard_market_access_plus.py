
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Impact Budgétaire - Market Access", layout="wide")

st.title("💊 Simulation d'Impact Budgétaire - Traitement BPCOne")

# Sidebar - Paramètres
st.sidebar.header("🔧 Paramètres de simulation")
population = st.sidebar.slider("Population cible", 10000, 100000, 50000, step=5000)
cout_exacerbation = st.sidebar.number_input("Coût annuel des exacerbations (€)", value=3200)
reduction_exacerbation = st.sidebar.slider("Réduction des exacerbations (%)", 0, 100, 25)
prix_traitement = st.sidebar.number_input("Prix annuel du traitement (€)", value=2500)
taux_adoption = st.sidebar.slider("Taux d’adoption (%)", 0, 100, 40)
horizon = st.sidebar.slider("Horizon (années)", 1, 5, 3)

# Scénarios
scenarios = {
    "Conservateur": 0.2,
    "Réaliste": 0.4,
    "Optimiste": 0.6
}

# Calculs
nb_patients = population * (taux_adoption / 100)
gain_par_patient = cout_exacerbation * (reduction_exacerbation / 100)
cout_total_traitement = nb_patients * prix_traitement
economie_totale = nb_patients * gain_par_patient
impact_net = economie_totale - cout_total_traitement
roi = (impact_net / cout_total_traitement) * 100 if cout_total_traitement > 0 else 0

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Patients traités", f"{int(nb_patients):,}")
col2.metric("💰 Économie / patient", f"{int(gain_par_patient):,} €")
col3.metric("📉 Impact net total", f"{int(impact_net):,} €", delta=f"{roi:.1f}% ROI")
col4.metric("💸 Coût total traitement", f"{int(cout_total_traitement):,} €")

st.markdown("---")

# Table des résultats principaux
st.subheader("📊 Résumé de la simulation")
results = {
    "Nombre de patients traités": [int(nb_patients)],
    "Coût total traitement (€)": [round(cout_total_traitement)],
    "Économie totale estimée (€)": [round(economie_totale)],
    "Impact budgétaire net (€)": [round(impact_net)],
    "ROI (%)": [round(roi, 2)]
}
st.table(pd.DataFrame(results))

# Graphique évolution sur horizon
st.subheader("📈 Évolution sur 5 ans")
years = list(range(1, horizon + 1))
impact_par_an = [impact_net * (i / horizon) for i in years]
fig_line = px.line(x=years, y=impact_par_an, markers=True, labels={"x": "Année", "y": "Impact budgétaire (€)"}, title="Projection d’impact net")
st.plotly_chart(fig_line, use_container_width=True)

# Analyse des scénarios
st.subheader("📊 Comparaison des scénarios")
scenario_data = []
for name, adoption_rate in scenarios.items():
    patients = population * adoption_rate
    eco_totale = patients * gain_par_patient
    cout_total = patients * prix_traitement
    impact = eco_totale - cout_total
    scenario_data.append({"Scénario": name, "Impact net (€)": impact})

df_scenarios = pd.DataFrame(scenario_data)
fig_bar = px.bar(df_scenarios, x="Scénario", y="Impact net (€)", title="Comparaison des scénarios", text="Impact net (€)")
st.plotly_chart(fig_bar, use_container_width=True)

# Pie chart - Répartition des coûts
st.subheader("📎 Répartition des coûts et économies")
labels = ["Économie estimée", "Coût traitement"]
values = [economie_totale, cout_total_traitement]
fig_pie = px.pie(values=values, names=labels, title="Part relative des gains et dépenses")
st.plotly_chart(fig_pie, use_container_width=True)

# Export CSV
st.subheader("📥 Exporter les données")
df_export = pd.DataFrame({
    "Paramètre": ["Population cible", "Taux adoption", "Prix traitement", "Coût exacerbation", "Réduction exacerbation", "Impact net", "ROI (%)"],
    "Valeur": [population, f"{taux_adoption}%", f"{prix_traitement} €", f"{cout_exacerbation} €", f"{reduction_exacerbation}%", f"{round(impact_net)} €", f"{round(roi, 2)}%"]
})
csv = df_export.to_csv(index=False).encode('utf-8')
st.download_button("📄 Télécharger les résultats (CSV)", data=csv, file_name="resultats_market_access.csv", mime="text/csv")
