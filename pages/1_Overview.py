
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_csv, phase_order


st.header("Executive Overview")

cm = load_csv("data/warehouse/Cohort_Master.csv")
pc = load_csv("data/warehouse/Placements_Cohort.csv")
jpt = load_csv("data/warehouse/JPT_Cohort.csv")
tutor = load_csv("data/warehouse/Tutor_Cohort_Summary.csv")
mentor = load_csv("data/warehouse/Mentor_Cohort.csv")
pc = phase_order(pc); jpt = phase_order(jpt); tutor = phase_order(tutor); mentor = phase_order(mentor)

# Filters
# Filters (remove Phase here)
colf1, colf2 = st.columns(2)
year = colf1.multiselect("Year", sorted(cm["Year"].unique()))
program = colf2.multiselect("Program", sorted(cm["Program"].unique()))

def apply_filters(df):
    if "Cohort_ID" in df.columns:
        df = df.merge(cm[["Cohort_ID","Year","Program"]], on="Cohort_ID", how="left")
    if year:
        df = df[df["Year"].isin(year)]
    if program:
        df = df[df["Program"].isin(program)]
    return df


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
