
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_csv, phase_order


st.header("AI Tutor – Usage & Impact (Unit-based)")
cm = load_csv("data/warehouse/Cohort_Master.csv")
sess = load_csv("data/warehouse/Tutor_Sessions.csv")
util = load_csv("data/warehouse/Tutor_Session_Utilization.csv")
wk = load_csv("data/warehouse/Tutor_Weekly_Summary.csv")
sumc = load_csv("data/warehouse/Tutor_Cohort_Summary.csv")
for df in [sess, util, wk, sumc]: phase_order(df)

# Filters
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

sess_f = apply_filters(sess)
util_f = apply_filters(util)
wk_f = apply_filters(wk)
sumc_f = apply_filters(sumc)

# KPIs
c1,c2,c3,c4 = st.columns(4)
c1.metric("Units with Sessions", int(sess_f["Unit_Code"].nunique()) if not sess_f.empty else 0)
c2.metric("Sessions Created", len(sess_f) if not sess_f.empty else 0)
c3.metric("Avg TRS (weekly)", round(util_f["Avg_TRS"].mean(),2) if not util_f.empty else 0)
c4.metric("Highest TRS (weekly)", round(util_f["Highest_TRS"].max(),2) if not util_f.empty else 0)

st.subheader("Sessions Created per Week")
if not wk_f.empty:
    grp = wk_f.groupby("Week")["Sessions_Created_This_Week"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Week"], grp["Sessions_Created_This_Week"], marker="o")
    ax.set_ylabel("Sessions Created")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

st.subheader("Overall Utilization per Week (%)")
if not wk_f.empty:
    grp = wk_f.groupby("Week")["Overall_Utilization_This_Week_%"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Week"], grp["Overall_Utilization_This_Week_%"], marker="o")
    ax.set_ylabel("Utilization (%)")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

st.subheader("Academic Averages (Pre vs Post Tutor)")
if not sumc_f.empty:
    fig, ax = plt.subplots()
    p = sumc_f.groupby("Phase")[["PreTutor_Exam_Avg","PostTutor_Exam_Avg"]].mean()
    p.plot(kind="bar", ax=ax)
    ax.set_ylabel("Exam Average")
    st.pyplot(fig)
