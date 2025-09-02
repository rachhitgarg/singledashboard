
import streamlit as st

st.header("Definitions & Notes")
st.markdown("""
**Phases (‘Phase’ field):** `Pre-AI`, `Yoodli`, `JPT`

**Key KPI formulas**
- Placement % = Placed / Eligible
- Conversion per Opening % = Offers_Issued / Openings_Announced (computed in JPT and via Company_Visits)
- Avg Conversion per Visit % = mean of (Offers_Issued / Openings_Announced) per visit, by cohort/phase
- Avg Openings per Visit = mean Openings_Announced per visit
- Tier-1 Share % = Tier1_Offers / Offers
- Pass % (exam) = provided by Exam Cell aggregates (Tutor_Cohort_Summary)

**Ownership**
- CR Team: Company_Visits, Placements_Cohort
- PRP/AI Team: JPT_Cohort
- Exam Cell: Tutor_* sheets
- Academic Manager: Mentor_Cohort

**Counter-example (market normalization)**
- Before JPT: 10 companies, 30 openings, 5 offers ⇒ 16.7% conversion per opening
- After JPT: 20 companies, 10 openings, 5 offers ⇒ 50% conversion per opening
Even with the same offers, JPT cohorts are more efficient in a shrinking market.
""")
