import streamlit as st

# Titre du dashboard
st.title("🩺 Simulation d'Impact Budgétaire – Traitement BPCOff (BPCO)")

# Sidebar : paramètres de simulation
st.sidebar.header("🎛 Paramètres de simulation")

# Variables modifiables
population_cible = st.sidebar.number_input("Population cible (patients/an)", min_value=1000, max_value=100000, value=50000, step=1000)
taux_adoption = st.sidebar.slider("Taux d’adoption (%)", 0, 100, 40, step=5)
prix_traitement = st.sidebar.number_input("Prix du traitement (€)", min_value=100, max_value=5000, value=2500, step=100)
reduction_exacerbations = st.sidebar.slider("Réduction des exacerbations (%)", 0, 100, 25, step=1)
cout_exacerbation = st.sidebar.number_input("Coût moyen annuel d’un patient avec exacerbation (€)", min_value=500, max_value=10000, value=3200, step=100)

# Calculs
nb_patients_traites = population_cible * (taux_adoption / 100)
gain_par_patient = cout_exacerbation * (reduction_exacerbations / 100)
cout_net_par_patient = prix_traitement - gain_par_patient
impact_budgetaire_total = nb_patients_traites * cout_net_par_patient

# Résultats
st.subheader("📊 Résultats de la simulation")

col1, col2 = st.columns(2)
col1.metric("Patients traités", f"{int(nb_patients_traites):,}")
col2.metric("Gain moyen par patient", f"{gain_par_patient:,.0f} €")

col1.metric("Coût net par patient", f"{cout_net_par_patient:,.0f} €")
col2.metric("Impact budgétaire total", f"{impact_budgetaire_total:,.0f} €")

# Interprétation automatique
st.markdown("---")
st.subheader("🔍 Interprétation")
if impact_budgetaire_total > 0:
    st.warning(f"⚠️ Le traitement génère un **surcoût** estimé à **{impact_budgetaire_total:,.0f} €** pour le système de santé.")
elif impact_budgetaire_total < 0:
    st.success(f"✅ Le traitement permet une **économie** nette de **{abs(impact_budgetaire_total):,.0f} €** pour le système de santé.")
else:
    st.info("ℹ️ Le traitement est **neutre budgétairement**.")

# Footer
st.markdown("---")
st.caption("Créé par Digital Pharma Lab • Simulation fictive à des fins pédagogiques.")
