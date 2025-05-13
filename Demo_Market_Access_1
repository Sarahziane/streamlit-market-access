import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulation Impact Budgétaire - BPCOff", layout="centered")

st.title("📊 Simulation de l'Impact Budgétaire – BPCOff")

# Paramètres de base
population_totale = 50000
cout_exacerbation = 3200

st.sidebar.header("🎛️ Paramètres de simulation")

# Inputs utilisateurs
prix_traitement = st.sidebar.slider("💸 Prix du traitement par patient (€)", 500, 5000, 2500, step=100)
taux_adoption = st.sidebar.slider("👥 Taux d'adoption (%)", 0, 100, 40, step=5) / 100
reduction_exacerbation = st.sidebar.slider("📉 Réduction des exacerbations (%)", 0, 100, 25, step=5) / 100

# Calculs
nb_patients = population_totale * taux_adoption
economie_par_patient = cout_exacerbation * reduction_exacerbation

cout_total = nb_patients * prix_traitement
economie_totale = nb_patients * economie_par_patient
impact_net = cout_total - economie_totale

# Affichage des résultats
st.subheader("🧮 Résultats de la simulation")

st.metric(label="Patients traités", value=int(nb_patients))
st.metric(label="Coût total du traitement", value=f"{int(cout_total):,} €")
st.metric(label="Économies générées", value=f"{int(economie_totale):,} €")
st.metric(label="Impact économique net", value=f"{int(impact_net):,} €")

# Tableau récapitulatif
df = pd.DataFrame({
    "Indicateur": ["Patients traités", "Coût total traitement", "Économies générées", "Impact net"],
    "Valeur (€)": [int(nb_patients), int(cout_total), int(economie_totale), int(impact_net)]
})
st.table(df.set_index("Indicateur"))

# Message conditionnel
if impact_net > 0:
    st.warning("💡 Le traitement génère un surcoût net. Considérez une baisse du prix ou une efficacité accrue.")
else:
    st.success("✅ Le traitement est économiquement favorable pour le système de santé.")
