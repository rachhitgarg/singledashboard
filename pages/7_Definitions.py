import streamlit as st

st.header("Definitions & Notes")

st.markdown(
"""
**Phases (‘Phase’ field):** `Pre-AI`, `Yoodli`, `JPT`  
_Phase filters are available **only** on the Placements page. Other pages may show Phase in charts for context but do not offer a Phase selector._

**Key KPI formulas**
- **Placement %** = Placed / Eligible  
- **Conversion per Opening %** = Offers_Issued / Openings_Announced  
- **Avg Conversion per Visit %** = mean of (Offers_Issued / Openings_Announced) per visit  
- **Avg Openings per Visit** = mean(Openings_Announced) per visit  
- **Tier-1 Share %** = Tier1_Offers / Offers  
- **Pass % (exam)** = provided by Exam Cell aggregates (Tutor_Cohort_Summary)

**Ownership**
- CR Team: Company_Visits, Placements_Cohort  
- PRP/AI Team: JPT_Cohort  
- Exam Cell: Tutor_* sheets  
- Academic Manager: Mentor_Cohort  

**Market normalization example**
- _Before JPT_: 10 companies, 30 openings, 5 offers ⇒ **16.7%** conversion per opening  
- _After JPT_: 20 companies, 10 openings, 5 offers ⇒ **50%** conversion per opening  
Even with the same number of offers, efficiency improved **3×** in a shrinking market.
"""
)
