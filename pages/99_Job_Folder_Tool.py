import streamlit as st
from utils.checklist_utils import build_job_folder_path, open_job_folder

st.set_page_config(page_title="Job Folder Tool", layout="wide")

st.title("📂 Job Folder Quick Access")

# SESSION STATE
if "job_number" not in st.session_state:
    st.session_state.job_number = ""


# INPUT
st.subheader("Enter Job Number")

job_number = st.text_input(
    "Job Number",
    value=st.session_state.job_number,
    placeholder="Example: D24836"
).strip().upper()

st.session_state.job_number = job_number


# BUTTONS
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚀 Open Job Folder", use_container_width=True):
        success, message = open_job_folder(job_number)

        if success:
            st.success(message)
        else:
            st.error(message)


with col2:
    if job_number:
        try:
            preview = build_job_folder_path(job_number)
            st.info(f"Path Preview:\n{preview}")
        except Exception as e:
            st.warning(str(e))


# OPTIONAL QUALITY OF LIFE
st.divider()

st.caption("Tip: Type job number once → reuse it across your workflow.")