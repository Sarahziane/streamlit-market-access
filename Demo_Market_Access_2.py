
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard BPCOff", layout="wide")

st.title("💊 BPCOff – Simulation d’Impact Économique")

# Sidebar – paramètres utilisateur
st.sidebar.header("🎛️ Paramètres du modèle")

population = st.sidebar.number_input("Population cible", 1000, 100000, 50000, step=1000)
taux_adoption = st.sidebar.slider("Taux d’adoption (%)", 0, 100, 40) / 100
prix_traitement = st.sidebar.number_input("Prix traitement (€)", 100, 10000, 2500, step=100)
cout_interne = st.sidebar.number_input("Coût interne labo/patient (€)", 0, 10000, 800, step=100)
horizon = st.sidebar.slider("Horizon en années", 1, 5, 3)

cout_exacerbation = st.sidebar.number_input("Coût moyen d’une exacerbation (€)", 1000, 10000, 3200, step=100)
reduction_exacerbation = st.sidebar.slider("Réduction des exacerbations (%)", 0, 100, 25) / 100

# Calculs principaux
patients_traites = int(population * taux_adoption)
revenus = patients_traites * prix_traitement * horizon
couts_internes = patients_traites * cout_interne * horizon
marge = revenus - couts_internes
roi_labo = (marge / couts_internes) if couts_internes else 0

economie_par_patient = cout_exacerbation * reduction_exacerbation
economie_totale = economie_par_patient * patients_traites * horizon
cout_total_pour_payeurs = patients_traites * prix_traitement * horizon
roi_payeurs = (economie_totale - cout_total_pour_payeurs) / cout_total_pour_payeurs if cout_total_pour_payeurs else 0

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧍 Patients traités", patients_traites)
col2.metric("💰 Marge brute labo", f"{marge:,.0f} €")
col3.metric("📈 ROI labo", f"{roi_labo:.2f}")
col4.metric("🏥 ROI payeurs", f"{roi_payeurs:.2f}")

# Message interprétation
if marge > 0:
    st.success("✅ Le traitement est **rentable pour le laboratoire**.")
else:
    st.warning("⚠️ Le traitement **n’est pas rentable** pour le laboratoire.")

# Comparaison ROI
st.subheader("📊 Comparaison des ROI")
roi_df = pd.DataFrame({
    "Acteur": ["Labo", "Payeurs"],
    "ROI": [roi_labo, roi_payeurs]
})
fig_roi = px.bar(roi_df, x="Acteur", y="ROI", color="Acteur", text="ROI", range_y=[min(0, roi_df['ROI'].min()), roi_df['ROI'].max()*1.1])
st.plotly_chart(fig_roi, use_container_width=True)

# Évolution de la marge
st.subheader("📈 Marge cumulée sur l’horizon")
years = list(range(1, horizon+1))
marge_par_an = [(patients_traites * prix_traitement - patients_traites * cout_interne) * y for y in years]
fig_marge = go.Figure()
fig_marge.add_trace(go.Scatter(x=years, y=marge_par_an, mode="lines+markers", name="Marge cumulée"))
fig_marge.update_layout(xaxis_title="Année", yaxis_title="Marge (€)")
st.plotly_chart(fig_marge, use_container_width=True)

# Analyse de sensibilité
st.subheader("🧪 Analyse de sensibilité interactive")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sens_prix = st.slider("Prix (€)", 1000, 5000, prix_traitement, step=100)
with col2:
    sens_adoption = st.slider("Adoption (%)", 0, 100, int(taux_adoption * 100), step=5) / 100
with col3:
    sens_cout_exac = st.slider("Coût exacerbation (€)", 1000, 6000, cout_exacerbation, step=100)
with col4:
    sens_reduc_exac = st.slider("Réduction exacerbations (%)", 0, 100, int(reduction_exacerbation * 100), step=5) / 100

sens_patients = int(population * sens_adoption)
sens_economie = sens_patients * sens_cout_exac * sens_reduc_exac * horizon
sens_cout_total = sens_patients * sens_prix * horizon
sens_impact_net = sens_economie - sens_cout_total
st.write(f"📉 Impact net pour le payeur : **{sens_impact_net:,.0f} €**")

# Scénarios
st.subheader("📦 Comparaison de scénarios")
scenarios = {
    "Conservateur": 0.20,
    "Réaliste": 0.40,
    "Optimiste": 0.60
}
scenario_data = []
for label, taux in scenarios.items():
    n = int(population * taux)
    eco = n * cout_exacerbation * reduction_exacerbation * horizon
    cout = n * prix_traitement * horizon
    scenario_data.append({"Scénario": label, "Impact net (€)": eco - cout})

df_scenarios = pd.DataFrame(scenario_data)
fig_scenarios = px.bar(df_scenarios, x="Scénario", y="Impact net (€)", color="Scénario", text="Impact net (€)")
st.plotly_chart(fig_scenarios, use_container_width=True)

# Répartition des coûts
st.subheader("💡 Répartition des coûts (payeurs)")
net_per_patient = prix_traitement - economie_par_patient
df_costs = pd.DataFrame({
    "Poste": ["Traitement", "Économies générées", "Coût net"],
    "Montant moyen / patient (€)": [prix_traitement, economie_par_patient, net_per_patient]
})
fig_pie = px.pie(df_costs, names="Poste", values="Montant moyen / patient (€)", title="Répartition par patient")
st.plotly_chart(fig_pie, use_container_width=True)

# Export CSV
st.subheader("📤 Export des résultats")
export_data = {
    "Patients traités": [patients_traites],
    "Revenus": [revenus],
    "Coûts internes": [couts_internes],
    "Marge brute": [marge],
    "ROI labo": [roi_labo],
    "Économie payeurs": [economie_totale],
    "ROI payeurs": [roi_payeurs]
}
df_export = pd.DataFrame(export_data)
st.download_button("Télécharger les résultats (CSV)", data=df_export.to_csv(index=False).encode('utf-8'), file_name="bpc_off_simulation.csv", mime="text/csv")
