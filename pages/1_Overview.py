import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_csv, phase_order

st.header("Executive Overview")

# Load data
cm = load_csv("data/warehouse/Cohort_Master.csv")
pc = load_csv("data/warehouse/Placements_Cohort.csv")
jpt = load_csv("data/warehouse/JPT_Cohort.csv")
tutor = load_csv("data/warehouse/Tutor_Cohort_Summary.csv")
mentor = load_csv("data/warehouse/Mentor_Cohort.csv")

# Ensure Phase ordering for context (no Phase filter here)
pc = phase_order(pc)
jpt = phase_order(jpt)
tutor = phase_order(tutor)
mentor = phase_order(mentor)

# Filters: Year & Program ONLY (no Phase filter here)
colf1, colf2 = st.columns(2)
year = colf1.multiselect("Year", sorted(cm["Year"].unique()))
program = colf2.multiselect("Program", sorted(cm["Program"].unique()))

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if "Cohort_ID" in df.columns:
        df = df.merge(cm[["Cohort_ID", "Year", "Program"]], on="Cohort_ID", how="left")
    if year:
        df = df[df["Year"].isin(year)]
    if program:
        df = df[df["Program"].isin(program)]
    return df

pc_f = apply_filters(pc.copy())
jpt_f = apply_filters(jpt.copy())
tut_f = apply_filters(tutor.copy())
men_f = apply_filters(mentor.copy())

# KPI tiles
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Avg Placement Conversion per Visit (%)",
    round(pc_f["Avg_Conversion_Per_Visit_%"].mean(), 2) if not pc_f.empty else "—",
)
c2.metric(
    "Avg Package",
    round(pc_f["Avg_Package"].mean(), 2) if not pc_f.empty else "—",
)
c3.metric(
    "Tier-1 Share (%)",
    round((pc_f["Tier1_Offers"].sum() / pc_f["Offers"].sum()) * 100, 2)
    if pc_f["Offers"].sum() > 0
    else "—",
)
c4.metric(
    "JPT Technical Score (Avg)",
    round(jpt_f["Avg_AI_Technical"].mean(), 2) if not jpt_f.empty else "—",
)

st.divider()

# Phase comparison: Avg Conversion per Visit
st.subheader("Phase Comparison: Conversion per Visit (%)")
if not pc_f.empty:
    grp = pc_f.groupby("Phase", observed=True)["Avg_Conversion_Per_Visit_%"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Phase"], grp["Avg_Conversion_Per_Visit_%"], marker="o")
    ax.set_ylabel("Avg Conversion per Visit (%)")
    st.pyplot(fig)
else:
    st.info("No data for selected filters.")

# Phase comparison: Average Package
st.subheader("Phase Comparison: Average Package")
if not pc_f.empty:
    grp = pc_f.groupby("Phase", observed=True)["Avg_Package"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Phase"], grp["Avg_Package"], marker="o")
    ax.set_ylabel("Avg Package")
    st.pyplot(fig)

# Associations
st.subheader("Associations (Directional)")
st.write("- Higher **PostTutor_Exam_Avg** often aligns with higher **Placement conversion**.")
st.write("- Higher **PostMentor_Capstone_Grade_Avg** aligns with higher **Tier-1 share** and **Avg Package**.")
st.write("- **JPT cohorts** show improved **conversion per opening** even when openings per visit shrink.")
