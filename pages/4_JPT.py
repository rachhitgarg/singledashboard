
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from 0_utils import load_csv, phase_order

st.header("JPT – Readiness & Conversion per Opening")
cm = load_csv("data/warehouse/Cohort_Master.csv")
jpt = load_csv("data/warehouse/JPT_Cohort.csv")
pc  = load_csv("data/warehouse/Placements_Cohort.csv")
for df in [jpt, pc]: phase_order(df)

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

jpt_f = apply_filters(jpt)
pc_f = apply_filters(pc)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Avg JPT Sessions/Student", round(jpt_f["Avg_Sessions_Per_Student"].mean(),2) if not jpt_f.empty else "—")
c2.metric("AI Technical (Avg)", round(jpt_f["Avg_AI_Technical"].mean(),2) if not jpt_f.empty else "—")
c3.metric("Pre Conv/Open (%)", round(pd.to_numeric(jpt_f["PreJPT_Conv_Rate_Per_Opening_%"], errors="coerce").mean(),2) if not jpt_f.empty else "—")
c4.metric("Post Conv/Open (%)", round(pd.to_numeric(jpt_f["PostJPT_Conv_Rate_Per_Opening_%"], errors="coerce").mean(),2) if not jpt_f.empty else "—")

st.subheader("Phase Comparison: Conversion per Opening (%)")
if not jpt_f.empty:
    tmp = jpt_f.copy()
    for col in ["PreJPT_Conv_Rate_Per_Opening_%","PostJPT_Conv_Rate_Per_Opening_%"]:
        tmp[col] = pd.to_numeric(tmp[col], errors="coerce")
    grp = tmp.groupby("Phase")[["PreJPT_Conv_Rate_Per_Opening_%","PostJPT_Conv_Rate_Per_Opening_%"]].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(grp["Phase"], grp["PreJPT_Conv_Rate_Per_Opening_%"], marker="o", label="Pre")
    ax.plot(grp["Phase"], grp["PostJPT_Conv_Rate_Per_Opening_%"], marker="o", label="Post")
    ax.legend()
    st.pyplot(fig)

st.subheader("Tier-1 Offers Before vs After (by Phase)")
if not jpt_f.empty:
    fig, ax = plt.subplots()
    tmp = jpt_f.copy()
    for c in ["Tier1_Offers_Before","Tier1_Offers_After"]:
        tmp[c] = pd.to_numeric(tmp[c], errors="coerce")
    p = tmp.groupby("Phase")[["Tier1_Offers_Before","Tier1_Offers_After"]].sum()
    p.plot(kind="bar", ax=ax)
    st.pyplot(fig)
