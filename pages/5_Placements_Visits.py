import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_csv, phase_order

st.header("Placements & Company Visits (Normalized)")

cm = load_csv("data/warehouse/Cohort_Master.csv")
pc = load_csv("data/warehouse/Placements_Cohort.csv")
cv = load_csv("data/warehouse/Company_Visits.csv")

for df in [pc, cv]:
    phase_order(df)

# Filters: Year, Program, AND Phase (Phase only here)
col1, col2, col3 = st.columns(3)
year = col1.multiselect("Year", sorted(cm["Year"].unique()))
program = col2.multiselect("Program", sorted(cm["Program"].unique()))
phase = col3.multiselect("Phase", ["Pre-AI", "Yoodli", "JPT"], default=["Pre-AI", "Yoodli", "JPT"])

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if "Cohort_ID" in df.columns:
        df = df.merge(cm[["Cohort_ID", "Year", "Program"]], on="Cohort_ID", how="left")
    if year:
        df = df[df["Year"].isin(year)]
    if program:
        df = df[df["Program"].isin(program)]
    if phase and "Phase" in df.columns:
        df = df[df["Phase"].isin(phase)]
    return df

pc_f = apply_filters(pc.copy())
cv_f = apply_filters(cv.copy())

c1, c2, c3 = st.columns(3)
c1.metric(
    "Avg Conversion per Visit (%)",
    round(pc_f["Avg_Conversion_Per_Visit_%"].mean(), 2) if not pc_f.empty else "—",
)
c2.metric(
    "Avg Openings per Visit",
    round(pc_f["Avg_Openings_Per_Visit"].mean(), 2) if not pc_f.empty else "—",
)
c3.metric("Total Offers", int(pc_f["Offers"].sum()) if not pc_f.empty else 0)

st.subheader("Placement Funnel by Phase")
if not pc_f.empty:
    fig, ax = plt.subplots()
    p = pc_f.groupby("Phase", observed=True)[
        ["Eligible", "Applied", "Shortlisted", "Offers", "Placed"]
    ].sum()
    p.plot(kind="bar", ax=ax)
    st.pyplot(fig)

st.subheader("Company Role Families – Offers Issued (by Phase)")
if not cv_f.empty:
    fig, ax = plt.subplots()
    fam = cv_f.groupby(["Phase", "Role_Family"], observed=True)["Offers_Issued"].sum().unstack(fill_value=0)
    fam.plot(kind="bar", ax=ax)
    st.pyplot(fig)
