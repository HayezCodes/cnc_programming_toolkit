import streamlit as st


def render_cutting_mode_sidebar():
    st.session_state["cut_mode"] = "Standard"


def render_sidebar_nav(current_page: str):
    st.sidebar.title("CNC Toolkit")

    st.sidebar.markdown("### Main")
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/1_Speeds_Feeds.py", label="Speeds & Feeds")
    st.sidebar.page_link("pages/4_Standards.py", label="Standards")
    st.sidebar.page_link("pages/5_Machines.py", label="Machines")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Tools")
    st.sidebar.page_link("pages/2_Threads.py", label="Threads")
    st.sidebar.page_link("pages/3_Calculators.py", label="Calculators")

    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/99_Checklist.py", label="Checklist")
