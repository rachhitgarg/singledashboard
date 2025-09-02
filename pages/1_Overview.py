
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from 0_utils import load_csv, phase_order

st.header("Executive Overview")

cm = load_csv("data/warehouse/Cohort_Master.csv")
pc = load_csv("data/warehouse/Placements_Cohort.csv")
jpt = load_csv("data/warehouse/JPT_Cohort.csv")
tutor = load_csv("data/warehouse/Tutor_Cohort_Summary.csv")
mentor = load_csv("data/warehouse/Mentor_Cohort.csv")
pc = phase_order(pc); jpt = phase_order(jpt); tutor = phase_order(tutor); mentor = phase_order(mentor)

# Filters
colf1, colf2, colf3 = st.columns(3)
year = colf1.multiselect("Year", sorted(cm["Year"].unique()))
program = colf2.multiselect("Program", sorted(cm["Program"].unique()))
phase = colf3.multiselect("Phase", ["Pre-AI","Yoodli","JPT"], default=["Pre-AI","Yoodli","JPT"])

def apply_filters(df):
    if "Cohort_ID" in df.columns:
        df = df.merge(cm[["Cohort_ID","Year","Program"]], on="Cohort_ID", how="left")
    if year: df = df[df["Year"].isin(year)]
    if program: df = df[df["Program"].isin(program)]
    if phase and "Phase" in df.columns: df = df[df["Phase"].isin(phase)]
    return df

pc_f = apply_filters(pc)
jpt_f = apply_filters(jpt)
tut_f = apply_filters(tutor)
men_f = apply_filters(mentor)

# KPI tiles
def kpi(label, value, suffix=""):
    st.metric(label, f"{value}{suffix}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Placement Conversion per Visit (%)", round(pc_f["Avg_Conversion_Per_Visit_%"].mean(),2) if not pc_f.empty else "—")
c2.metric("Avg Package", round(pc_f["Avg_Package"].mean(),2) if not pc_f.empty else "—")
c3.metric("Tier-1 Share (%)", round((pc_f["Tier1_Offers"].sum()/pc_f["Offers"].sum())*100,2) if pc_f["Offers"].sum()>0 else "—")
c4.metric("JPT Technical Score (Avg)", round(jpt_f["Avg_AI_Technical"].mean(),2) if not jpt_f.empty else "—")

st.divider()

# Phase comparison: Avg_Conversion_Per_Visit_%
st.subheader("Phase Comparison: Conversion per Visit (%)")
if not pc_f.empty:
    grp = pc_f.groupby("Phase")["Avg_Conversion_Per_Visit_%"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Phase"], grp["Avg_Conversion_Per_Visit_%"], marker="o")
    ax.set_ylabel("Avg Conversion per Visit (%)")
    st.pyplot(fig)
else:
    st.info("No data for selected filters.")

# Phase comparison: Average Package
st.subheader("Phase Comparison: Average Package")
if not pc_f.empty:
    grp = pc_f.groupby("Phase")["Avg_Package"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Phase"], grp["Avg_Package"], marker="o")
    ax.set_ylabel("Avg Package")
    st.pyplot(fig)

# Attribution cards (directional)
st.subheader("Associations (Directional)")
st.write("- Cohorts with higher **PostTutor_Exam_Avg** typically show higher **Placement conversion**.")
st.write("- Cohorts with higher **PostMentor_Capstone_Grade_Avg** typically show higher **Tier-1 offers share** and **Avg Package**.")
st.write("- Cohorts in **JPT phase** show improved **conversion per opening** compared to earlier phases, even when openings per visit shrink.")
