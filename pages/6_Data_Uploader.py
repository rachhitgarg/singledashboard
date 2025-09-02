import streamlit as st
import pandas as pd

st.header("Data Uploader (with Schema Validation)")

schemas = {
    "Cohort_Master": ["Cohort_ID","Year","Program","Batch_Size","Phase"],
    "Company_Visits": ["Cohort_ID","Phase","Company_Name","Visit_Date","Role_Title","Role_Family","Tier","Sector","Geography","Is_Repeat_Recruiter","Openings_Announced","Applicants_Attended","Interview_Slots","Shortlisted","Offers_Issued","Joined_Count"],
    "Placements_Cohort": ["Cohort_ID","Phase","Eligible","Applied","Shortlisted","Offers","Placed","Avg_Package","Median_Package","Highest_Package","Tier1_Offers","Tier2_Offers","Startup_Offers","PSU_Offers","Tech_Role_Share_%","Finance_Role_Share_%","Consulting_Role_Share_%","Other_Role_Share_%","Avg_Conversion_Per_Visit_%","Avg_Openings_Per_Visit"],
    "JPT_Cohort": ["Cohort_ID","Phase","Total_JPT_Sessions","Avg_Sessions_Per_Student","Avg_AI_Confidence","Avg_AI_Communication","Avg_AI_Technical","PreJPT_Conv_Rate_Per_Opening_%","PostJPT_Conv_Rate_Per_Opening_%","Conversion_Boost_Per_Opening_%","Tier1_Offers_Before","Tier1_Offers_After","Avg_Package_Before","Avg_Package_After"],
    "Tutor_Sessions": ["Cohort_ID","Phase","Unit_Code","Unit_Name","Session_ID","Session_Type","Created_Week","Assigned_Count"],
    "Tutor_Session_Utilization": ["Cohort_ID","Phase","Session_ID","Week","Started_Count","Completed_Count","Avg_TRS","Highest_TRS"],
    "Tutor_Weekly_Summary": ["Cohort_ID","Phase","Week","Sessions_Created_This_Week","Overall_Utilization_This_Week_%","Units_With_Sessions_Count","Units_Adopted_%","Active_Users_%","Avg_Sessions_Per_Student"],
    "Tutor_Cohort_Summary": ["Cohort_ID","Phase","Active_Users_%","Units_With_Sessions_Count","Units_Adopted_%","Avg_Sessions_Per_Student","PreTutor_Exam_Avg","PostTutor_Exam_Avg","PreTutor_Assignment_Avg","PostTutor_Assignment_Avg","Pass_Percentage"],
    "Mentor_Cohort": ["Cohort_ID","Phase","PreMentor_Capstone_Grade_Avg","PostMentor_Capstone_Grade_Avg","Grade_A_Distribution_%_Pre","Grade_A_Distribution_%_Post","Higher_Degree_Attempts","Higher_Degree_Admissions","PostMentor_Exam_Avg","Tier1_Offers_Share_%","Avg_Package_in_Phase"]
}

dataset = st.selectbox("Choose dataset to upload", list(schemas.keys()))
file = st.file_uploader("Upload CSV matching the selected schema", type=["csv"])

if file:
    try:
        df = pd.read_csv(file)
        expected = schemas[dataset]
        missing = [c for c in expected if c not in df.columns]
        extra = [c for c in df.columns if c not in expected]

        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            if extra:
                st.warning(f"Extra columns will be ignored: {extra}")
                df = df[expected]
            out_path = f"data/warehouse/{dataset}.csv"
            df.to_csv(out_path, index=False)
            st.success(f"Uploaded and validated successfully. Saved to {out_path}")
            st.write("Preview:")
            st.dataframe(df.head())
    except Exception as e:
        st.error(f"Upload failed: {e}")
