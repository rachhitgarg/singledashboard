import streamlit as st
import pandas as pd
import io
import os
from utils import load_csv  # not required here but fine to keep

st.header("Data Uploader (with Schema Validation)")

# ======== MASTER SCHEMAS (download + validation) ========
SCHEMAS = {
    "Cohort_Master": [
        "Cohort_ID", "Year", "Program", "Batch_Size", "Phase"
    ],
    "Company_Visits": [
        "Cohort_ID","Phase","Company_Name","Visit_Date","Role_Title","Role_Family",
        "Tier","Sector","Geography","Is_Repeat_Recruiter",
        "Openings_Announced","Applicants_Attended","Interview_Slots","Shortlisted","Offers_Issued","Joined_Count"
    ],
    "Placements_Cohort": [
        "Cohort_ID","Phase","Eligible","Applied","Shortlisted","Offers","Placed",
        "Avg_Package","Median_Package","Highest_Package",
        "Tier1_Offers","Tier2_Offers","Startup_Offers","PSU_Offers",
        "Tech_Role_Share_%","Finance_Role_Share_%","Consulting_Role_Share_%","Other_Role_Share_%",
        "Avg_Conversion_Per_Visit_%","Avg_Openings_Per_Visit"
    ],
    "JPT_Cohort": [
        "Cohort_ID","Phase",
        "Total_JPT_Sessions","Avg_Sessions_Per_Student",
        "Avg_AI_Confidence","Avg_AI_Communication","Avg_AI_Technical",
        "PreJPT_Conv_Rate_Per_Opening_%","PostJPT_Conv_Rate_Per_Opening_%","Conversion_Boost_Per_Opening_%",
        "Tier1_Offers_Before","Tier1_Offers_After",
        "Avg_Package_Before","Avg_Package_After"
    ],
    "Tutor_Sessions": [
        "Cohort_ID","Phase","Unit_Code","Unit_Name","Session_ID","Session_Type","Created_Week","Assigned_Count"
    ],
    "Tutor_Session_Utilization": [
        "Cohort_ID","Phase","Session_ID","Week","Started_Count","Completed_Count","Avg_TRS","Highest_TRS"
    ],
    "Tutor_Weekly_Summary": [
        "Cohort_ID","Phase","Week","Sessions_Created_This_Week","Overall_Utilization_This_Week_%",
        "Units_With_Sessions_Count","Units_Adopted_%","Active_Users_%","Avg_Sessions_Per_Student"
    ],
    "Tutor_Cohort_Summary": [
        "Cohort_ID","Phase","Active_Users_%","Units_With_Sessions_Count","Units_Adopted_%","Avg_Sessions_Per_Student",
        "PreTutor_Exam_Avg","PostTutor_Exam_Avg","PreTutor_Assignment_Avg","PostTutor_Assignment_Avg","Pass_Percentage"
    ],
    "Mentor_Cohort": [
        "Cohort_ID","Phase",
        "PreMentor_Capstone_Grade_Avg","PostMentor_Capstone_Grade_Avg",
        "Grade_A_Distribution_%_Pre","Grade_A_Distribution_%_Post",
        "Higher_Degree_Attempts","Higher_Degree_Admissions",
        "PostMentor_Exam_Avg","Tier1_Offers_Share_%","Avg_Package_in_Phase"
    ]
}

# ======== MASTER TEMPLATE DOWNLOAD ========
def build_master_template_bytes() -> bytes:
    """
    Build an Excel file in-memory with one sheet per dataset,
    containing only header rows matching SCHEMAS.
    Prefers an existing file at templates/SPJ_AI_Cohort_Dashboard_Template_vFinal.xlsx if present.
    """
    # If you want to ship a pre-bundled template, put it under templates/ and we'll use it
    template_path = "templates/SPJ_AI_Cohort_Dashboard_Template_vFinal.xlsx"
    if os.path.exists(template_path):
        with open(template_path, "rb") as f:
            return f.read()

    # else build an Excel workbook on the fly
    bio = io.BytesIO()
    # use XlsxWriter engine (ensure xlsxwriter is in requirements.txt)
    with pd.ExcelWriter(bio, engine="xlsxwriter") as writer:
        # README sheet
        readme = pd.DataFrame({
            "SPJ Cohort-Level Data Template": [
                "Guidelines:",
                "- Cohort-first design (no student-level needed in uploads).",
                "- Phase values: Pre-AI, Yoodli, JPT.",
                "- Company_Visits rows are keyed by (Cohort_ID, Phase, Company_Name, Visit_Date, Role_Title).",
                "- AI Tutor is unit-based (no faculty IDs).",
                "- TRS tracked in Tutor_Session_Utilization: Avg_TRS, Highest_TRS.",
                "- Week format: ISO YYYY-WW (e.g., 2025-09)."
            ]
        })
        readme.to_excel(writer, sheet_name="README_Data_Dictionary", index=False)

        # one sheet per schema with header row only
        for sheet, cols in SCHEMAS.items():
            df = pd.DataFrame(columns=cols)
            df.to_excel(writer, sheet_name=sheet, index=False)

    return bio.getvalue()

st.download_button(
    label="⬇️ Download Master Template (Excel)",
    data=build_master_template_bytes(),
    file_name="SPJ_AI_Cohort_Dashboard_Template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.markdown("---")

# ======== VALIDATED UPLOADS ========
dataset = st.selectbox("Choose dataset to upload", list(SCHEMAS.keys()))
file = st.file_uploader("Upload CSV matching the selected schema", type=["csv"])

if file:
    try:
        df = pd.read_csv(file)
        expected = SCHEMAS[dataset]
        missing = [c for c in expected if c not in df.columns]
        extra = [c for c in df.columns if c not in expected]

        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            if extra:
                st.warning(f"Extra columns will be ignored: {extra}")
                df = df[expected]
            out_path = f"data/warehouse/{dataset}.csv"
            os.makedirs("data/warehouse", exist_ok=True)
            df.to_csv(out_path, index=False)
            st.success(f"Uploaded and validated successfully. Saved to `{out_path}`")
            st.write("Preview:")
            st.dataframe(df.head())
    except Exception as e:
        st.error(f"Upload failed: {e}")
