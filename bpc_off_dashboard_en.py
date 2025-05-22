
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests

st.set_page_config(page_title="BPCOff Budget Impact Dashboard", layout="wide")
st.title("💊 BPCOff – Budget Impact Simulation")

# Sidebar – user input
st.sidebar.header("🎛️ Model Parameters")

population = st.sidebar.number_input("Target population", 1000, 100000, 50000, step=1000)
adoption_rate = st.sidebar.slider("Adoption rate (%)", 0, 100, 40) / 100
drug_price = st.sidebar.number_input("Drug price per patient (€)", 100, 10000, 2500, step=100)
internal_cost = st.sidebar.number_input("Internal cost per patient (€)", 0, 10000, 800, step=100)
time_horizon = st.sidebar.slider("Time horizon (years)", 1, 5, 3)

exacerbation_cost = st.sidebar.number_input("Average cost of exacerbation (€)", 1000, 10000, 3200, step=100)
exacerbation_reduction = st.sidebar.slider("Exacerbation reduction (%)", 0, 100, 25) / 100

# Main calculations
treated_patients = int(population * adoption_rate)
revenue = treated_patients * drug_price * time_horizon
internal_total_cost = treated_patients * internal_cost * time_horizon
gross_margin = revenue - internal_total_cost
roi_manufacturer = (gross_margin / internal_total_cost) if internal_total_cost else 0

savings_per_patient = exacerbation_cost * exacerbation_reduction
total_savings = savings_per_patient * treated_patients * time_horizon
payer_total_cost = treated_patients * drug_price * time_horizon
roi_payer = (total_savings - payer_total_cost) / payer_total_cost if payer_total_cost else 0

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧍 Treated patients", treated_patients)
col2.metric("💰 Gross margin (manufacturer)", f"{gross_margin:,.0f} €")
col3.metric("📈 ROI manufacturer", f"{roi_manufacturer:.2f}")
col4.metric("🏥 ROI payer", f"{roi_payer:.2f}")

# Interpretation message
if gross_margin > 0:
    st.success("✅ The treatment is profitable for the manufacturer.")
else:
    st.warning("⚠️ The treatment is not profitable for the manufacturer.")

# ROI comparison
st.subheader("📊 ROI Comparison")
roi_df = pd.DataFrame({
    "Stakeholder": ["Manufacturer", "Payer"],
    "ROI": [roi_manufacturer, roi_payer]
})
fig_roi = px.bar(roi_df, x="Stakeholder", y="ROI", color="Stakeholder", text="ROI", range_y=[min(0, roi_df['ROI'].min()), roi_df['ROI'].max()*1.1])
st.plotly_chart(fig_roi, use_container_width=True)

# Margin evolution
st.subheader("📈 Cumulative Margin Over Time")
years = list(range(1, time_horizon+1))
margin_per_year = [(treated_patients * drug_price - treated_patients * internal_cost) * y for y in years]
fig_margin = go.Figure()
fig_margin.add_trace(go.Scatter(x=years, y=margin_per_year, mode="lines+markers", name="Cumulative Margin"))
fig_margin.update_layout(xaxis_title="Year", yaxis_title="Margin (€)")
st.plotly_chart(fig_margin, use_container_width=True)

# Sensitivity analysis
st.subheader("🧪 Interactive Sensitivity Analysis")
col1, col2, col3, col4 = st.columns(4)
with col1:
    sens_price = st.slider("Price (€)", 1000, 5000, drug_price, step=100)
with col2:
    sens_adoption = st.slider("Adoption (%)", 0, 100, int(adoption_rate * 100), step=5) / 100
with col3:
    sens_exac_cost = st.slider("Exacerbation cost (€)", 1000, 6000, exacerbation_cost, step=100)
with col4:
    sens_exac_reduc = st.slider("Exacerbation reduction (%)", 0, 100, int(exacerbation_reduction * 100), step=5) / 100

sens_patients = int(population * sens_adoption)
sens_savings = sens_patients * sens_exac_cost * sens_exac_reduc * time_horizon
sens_total_cost = sens_patients * sens_price * time_horizon
sens_net_impact = sens_savings - sens_total_cost
st.write(f"📉 Net impact for payer: **{sens_net_impact:,.0f} €**")

# Scenario comparison
st.subheader("📦 Scenario Comparison")
scenarios = {
    "Conservative": 0.20,
    "Realistic": 0.40,
    "Optimistic": 0.60
}
scenario_data = []
for label, rate in scenarios.items():
    n = int(population * rate)
    eco = n * exacerbation_cost * exacerbation_reduction * time_horizon
    cost = n * drug_price * time_horizon
    scenario_data.append({"Scenario": label, "Net Impact (€)": eco - cost})

df_scenarios = pd.DataFrame(scenario_data)
fig_scenarios = px.bar(df_scenarios, x="Scenario", y="Net Impact (€)", color="Scenario", text="Net Impact (€)")
st.plotly_chart(fig_scenarios, use_container_width=True)

# Cost breakdown
st.subheader("💡 Cost Breakdown (payer perspective)")
net_per_patient = drug_price - savings_per_patient
df_costs = pd.DataFrame({
    "Item": ["Treatment", "Savings", "Net Cost"],
    "Value per patient (€)": [drug_price, savings_per_patient, net_per_patient]
})
fig_pie = px.pie(df_costs, names="Item", values="Value per patient (€)", title="Per-Patient Breakdown")
st.plotly_chart(fig_pie, use_container_width=True)

# Regional analysis
st.subheader("🗺️ Regional Analysis by Hospital Type")
regions = [
    "Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie",
    "Hauts-de-France", "Grand Est", "Provence-Alpes-Côte d'Azur", "Brittany",
    "Normandy", "Bourgogne-Franche-Comté", "Centre-Val de Loire", "Pays de la Loire"
]
facility_types = ["All", "CHU", "CHG", "ESPIC"]
selected_facility = st.selectbox("Filter by facility type:", facility_types)

np.random.seed(42)
regional_adoption = np.random.uniform(0.15, 0.75, len(regions))
regional_data = pd.DataFrame({
    "Region": regions,
    "Adoption rate (%)": (regional_adoption * 100).round(1),
    "Facility type": np.random.choice(facility_types[1:], len(regions)) if selected_facility != "All" else ["All"]*len(regions)
})
if selected_facility != "All":
    regional_data = regional_data[regional_data["Facility type"] == selected_facility]

geojson_url = "https://france-geojson.gregoiredavid.fr/repo/regions.geojson"
with requests.get(geojson_url) as r:
    geojson = r.json()

fig_map = px.choropleth(
    regional_data,
    geojson=geojson,
    featureidkey="properties.nom",
    locations="Region",
    color="Adoption rate (%)",
    color_continuous_scale="Viridis",
    title="Simulated Adoption Rate by Region"
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)

# Export CSV
st.subheader("📤 Export Results")
export_data = {
    "Treated patients": [treated_patients],
    "Revenue": [revenue],
    "Internal cost": [internal_total_cost],
    "Gross margin": [gross_margin],
    "ROI manufacturer": [roi_manufacturer],
    "Payer savings": [total_savings],
    "ROI payer": [roi_payer]
}
df_export = pd.DataFrame(export_data)
st.download_button("Download results (CSV)", data=df_export.to_csv(index=False).encode('utf-8'), file_name="bpc_off_dashboard_en.csv", mime="text/csv")
