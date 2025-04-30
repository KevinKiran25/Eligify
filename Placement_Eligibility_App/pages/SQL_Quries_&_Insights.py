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

st.title("Placement Insights & SQL Queries 📊 ")


query_options = {
    "Average Programming Score Per Batch": """
        SELECT st.course_batch, AVG(pg.latest_project_score) AS avg_score
        FROM students AS st
        JOIN programming AS pg ON st.student_id = pg.student_id 
        GROUP BY st.course_batch
    """,

    "Top 5 Best of Best Students for Placement": """
        SELECT st.name, pl.mock_interview_score, pl.internships_completed, pg.latest_project_score
        FROM students AS st
        JOIN placements AS pl ON st.student_id = pl.student_id 
        JOIN programming AS pg ON st.student_id = pg.student_id 
        WHERE pl.placement_status = 'Ready' 
        ORDER BY pl.mock_interview_score DESC, pg.latest_project_score DESC 
        LIMIT 5
    """,

    "Students Who Are Placed": """
        SELECT st.name, pl.company_name, pl.placement_package, pl.interview_rounds_cleared
        FROM students AS st
        JOIN placements AS pl ON st.student_id = pl.student_id 
        WHERE pl.placement_status = 'Placed'
        ORDER BY pl.placement_package DESC
    """,

    "Placement Rate Per Batch": """
        SELECT st.course_batch, 
               COUNT(CASE WHEN pl.placement_status = 'Placed' THEN 1 END) * 100.0 / COUNT(*) AS placement_rate
        FROM students AS st
        JOIN placements AS pl ON st.student_id = pl.student_id 
        GROUP BY st.course_batch
    """,

    "Soft Skills Score Distribution": """
        SELECT sf.communication, sf.teamwork, sf.presentation, sf.leadership, sf.critical_thinking
        FROM soft_skills AS sf
    """,

    "Students With Highest Soft Skills": """
        SELECT st.name, 
               (sf.communication + sf.teamwork + sf.leadership + sf.critical_thinking) AS total_soft_skills
        FROM students AS st
        JOIN soft_skills AS sf ON st.student_id = sf.student_id 
        ORDER BY total_soft_skills DESC 
        LIMIT 5
    """,

    "Top 5 Students With Best Project Scores": """
        SELECT st.name, pg.latest_project_score 
        FROM students AS st
        JOIN programming AS pg ON st.student_id = pg.student_id 
        ORDER BY pg.latest_project_score DESC 
        LIMIT 5
    """,

    "Average Placement Package Per Batch": """
        SELECT st.course_batch, AVG(pl.placement_package) AS avg_package
        FROM students AS st
        JOIN placements AS pl ON st.student_id = pl.student_id 
        WHERE pl.placement_package > 0 
        GROUP BY st.course_batch
    """,

    "Not Ready for Placement But Have Good Soft Skills": """
        SELECT st.name, pl.placement_status, 
               (sf.communication + sf.teamwork + sf.leadership + sf.critical_thinking) AS soft_skills_score
        FROM students AS st
        JOIN placements AS pl ON st.student_id = pl.student_id 
        JOIN soft_skills AS sf ON st.student_id = sf.student_id 
        WHERE pl.placement_status = 'Not Ready'
        ORDER BY soft_skills_score DESC 
        LIMIT 10
    """,

    "Students With Best Technical & Soft Skills Combined": """
        SELECT st.name, 
               (pg.latest_project_score + sf.communication + sf.teamwork + sf.leadership + sf.critical_thinking) AS total_score
        FROM students AS st
        JOIN programming AS pg ON st.student_id = pg.student_id 
        JOIN soft_skills AS sf ON st.student_id = sf.student_id 
        ORDER BY total_score DESC 
        LIMIT 5
    """
}

selected_query = st.selectbox("Select an SQL Insight", list(query_options.keys()))

if st.button("Run Query"):
    query = query_options[selected_query]
    results = db.fetchall(query)
    
    if results:
        column_names = [desc[0] for desc in db.cursor.description]
        df = pd.DataFrame(results,columns=column_names)
        st.dataframe(df)
    else:
        st.write("❌ No data found.")
