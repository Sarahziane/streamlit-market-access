
import streamlit as st
import pandas as pd

st.title("💊 Simulation d'Impact Budgétaire - Traitement BPCOne")

# Hypothèses de base
st.sidebar.header("🔧 Paramètres")
population = st.sidebar.slider("Population cible", 10000, 100000, 50000, step=5000)
cout_exacerbation = st.sidebar.number_input("Coût annuel des exacerbations par patient (€)", value=3200)
reduction_exacerbation = st.sidebar.slider("Réduction des exacerbations (%)", 0, 100, 25)
prix_traitement = st.sidebar.number_input("Prix annuel du traitement (€)", value=2500)
taux_adoption = st.sidebar.slider("Taux d’adoption (%)", 0, 100, 40)

# Calculs
nb_patients = population * (taux_adoption / 100)
gain_par_patient = cout_exacerbation * (reduction_exacerbation / 100)
cout_total_traitement = nb_patients * prix_traitement
economie_totale = nb_patients * gain_par_patient
impact_net = economie_totale - cout_total_traitement

# Résultats
st.subheader("📊 Résultats de la simulation")
data = {
    "Nombre de patients traités": [int(nb_patients)],
    "Coût total traitement (€)": [round(cout_total_traitement)],
    "Économie totale estimée (€)": [round(economie_totale)],
    "Impact budgétaire net (€)": [round(impact_net)]
}
df = pd.DataFrame(data)
st.table(df)

# Message final
if impact_net > 0:
    st.success("✅ Le traitement génère une économie nette.")
else:
    st.warning("⚠️ Le traitement a un coût net pour le système.")
