
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_csv, phase_order


st.header("AI Mentor – Cohort Comparisons & Journey Links")
cm = load_csv("data/warehouse/Cohort_Master.csv")
mc = load_csv("data/warehouse/Mentor_Cohort.csv")
pc = load_csv("data/warehouse/Placements_Cohort.csv")
for df in [mc, pc]: phase_order(df)

col1, col2, col3 = st.columns(3)
year = col1.multiselect("Year", sorted(cm["Year"].unique()))
program = col2.multiselect("Program", sorted(cm["Program"].unique()))
phase = col3.multiselect("Phase", ["Pre-AI","Yoodli","JPT"], default=["Pre-AI","Yoodli","JPT"])

def apply_filters(df):
    if "Cohort_ID" in df.columns:
        df = df.merge(cm[["Cohort_ID","Year","Program"]], on="Cohort_ID", how="left")
    if year: df = df[df["Year"].isin(year)]
    if program: df = df[df["Program"].isin(program)]
    if phase and "Phase" in df.columns: df = df[df["Phase"].isin(phase)]
    return df

mc_f = apply_filters(mc)
pc_f = apply_filters(pc)

c1,c2,c3 = st.columns(3)
c1.metric("PostMentor Capstone Avg", round(mc_f["PostMentor_Capstone_Grade_Avg"].mean(),2) if not mc_f.empty else "—")
c2.metric("Grade A% (Post)", round(mc_f["Grade_A_Distribution_%_Post"].mean(),2) if not mc_f.empty else "—")
c3.metric("Tier-1 Share (%)", round(pc_f["Tier1_Offers"].sum()/pc_f["Offers"].sum()*100,2) if pc_f["Offers"].sum()>0 else "—")

st.subheader("Capstone Grade Average: Pre vs Post (by Phase)")
if not mc_f.empty:
    fig, ax = plt.subplots()
    tmp = mc_f.groupby("Phase")[["PreMentor_Capstone_Grade_Avg","PostMentor_Capstone_Grade_Avg"]].mean()
    tmp.plot(kind="bar", ax=ax)
    st.pyplot(fig)

st.subheader("Journey View: PostMentor Exam Avg vs Avg Package")
if not mc_f.empty and not pc_f.empty:
    merged = mc_f.merge(pc_f[["Cohort_ID","Phase","Avg_Package"]], on=["Cohort_ID","Phase"], how="left")
    fig, ax = plt.subplots()
    ax.scatter(merged["PostMentor_Exam_Avg"], merged["Avg_Package"])
    ax.set_xlabel("PostMentor Exam Avg")
    ax.set_ylabel("Avg Package")
    st.pyplot(fig)
