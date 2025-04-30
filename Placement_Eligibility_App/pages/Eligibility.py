import streamlit as st
from database import database
import pandas as pd

db = database()

st.markdown(
    """
    <style>
    /* Sidebar Background - Light Grey */
    [data-testid="stSidebar"] {
        background-color: #F5F5F5;
    }
    /* Title & Headers - Dark Grey */
    h1, h2, h3 {
        color: #333333;
    }
    /* Buttons - Soft Blue */
    div.stButton > button {
        background-color: #007BFF;
        color: white;
        border-radius: 6px;
        font-size: 14px;
        padding: 6px 12px;
    }
    /* Data Table Styling */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #CCCCCC;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(" Check Placement Eligibility 🎓")
st.sidebar.title("Filter Criteria 🔍 ")



col1, col2 = st.columns(2)

with col1:
    Prog_lang = st.selectbox("Programming Language Kmown",   options=[ "Python", "JavaScript", "Go", "Rust", "TypeScript","Kotlin"],index=0)
    problems_solved = st.selectbox("Minimum Coding Problems Solved",   options=[0,50,75,100],index=1)
    internships = st.slider("Minimum Internships Completed", 0, 3, 1)

with col2:
    placement_status = st.selectbox("Placement Status",   options=[ "Ready","Not Ready"],index=0)
    critical_thinking = st.selectbox("Critical Thinking Level", options=["Low", "Medium", "High"], index=1)
    mock_score = st.slider("Minimum Mock Interview Score", 0, 100, 65)

if st.button("Show Eligible Students"):

    critical_thinking_map = {"Low": 50, "Medium": 70, "High": 90}
    min_critical_thinking = critical_thinking_map[critical_thinking]

    query = """
    select st.student_id, st.name, st.age, st.course_batch, 
    pl.mock_interview_score, pl.internships_completed, pl.placement_status,pg.language, pg.problems_solved,
    sf.critical_thinking
    from students as st
    join placements as pl ON st.student_id = pl.student_id
    join programming as pg on st.student_id = pg.student_id
    JOIN soft_skills AS sf ON st.student_id = sf.student_id
    WHERE pl.placement_status != 'Placed' AND pg.language = %s AND pg.problems_solved >= %s 
    AND pl.placement_status = %s AND pl.mock_interview_score >= %s 
    AND pl.internships_completed >= %s AND sf.critical_thinking >= %s
    """
    results = db.fetchall(query, (Prog_lang,problems_solved,placement_status,mock_score, internships,min_critical_thinking))
    
    if results:
        df =pd.DataFrame(results, columns=["ID", "Name", "Age", "Batch", "Mock Score", "Internships",
             "Status", "Language", "Problems Solved", "Critical Thinking"])
        
        df = df[["ID","Name","Age","Batch", "Language", "Internships", "Problems Solved","Status"]]

        st.dataframe(df)

    else:
        st.write("eligible students Not found. ❌ ")
