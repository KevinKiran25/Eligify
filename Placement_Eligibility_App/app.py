import streamlit as st

st.set_page_config(page_title="Placement App", layout="wide", initial_sidebar_state="expanded")

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
st.sidebar.title("Home 🏠")  

st.title("Placement Eligibility App")

st.write("Use the sidebar to switch between eligibility criteria and SQL insights.")
