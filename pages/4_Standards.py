import os
import webbrowser
import streamlit as st
from utils.ui_helpers import render_sidebar_nav

st.set_page_config(
    page_title="Standards",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1.2rem;
}

.std-hero {
    border: 1px solid rgba(250,250,250,0.12);
    border-radius: 18px;
    padding: 18px 20px;
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.018));
    margin-bottom: 1rem;
}

.std-panel {
    border: 1px solid rgba(250,250,250,0.10);
    border-radius: 16px;
    padding: 16px 18px;
    background: rgba(255,255,255,0.025);
}
</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Standards")

st.markdown("""
<div class="std-hero">
    <div style="font-size:0.9rem; opacity:0.8;">PROGRAMMING STANDARDS</div>
    <div style="font-size:2.15rem; font-weight:800; margin-top:0.2rem;">Standards</div>
    <div style="font-size:0.96rem; opacity:0.85; margin-top:0.35rem;">
        Empower MFG - Programming Standards
    </div>
</div>
""", unsafe_allow_html=True)

project_root = os.path.dirname(os.path.dirname(__file__))
base_path = os.path.join(project_root, "standards")

left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="std-panel">', unsafe_allow_html=True)
    st.markdown("### Lathe Order of Operations")
    st.code("""SETUP
- Workholding / jaws / collet
- Stickout verified
- Tailstock / steady rest setup

OPERATION ORDER
1. Face / Endwork
2. OD Rough Turning
3. OD Finish Turning
4. Grooves / Undercuts
5. Threading
6. Keyways (live tooling)
7. Drill / Tap in keyways (LAST)

FINAL
- Deburr
- Verify critical features
""")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="std-panel">', unsafe_allow_html=True)
    st.markdown("### Mill Order of Operations")
    st.code("""SETUP
- Workholding / fixture / v-block
- Datum / origin verified

OPERATION ORDER
1. Keyways / slots
2. Finish keyways / slots
3. Spot drill
4. Drill
5. Tap
6. Deburr

FINAL
- Verify depths
- Verify diameters
""")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("## Standards Library")

if not os.path.exists(base_path):
    st.error(f"Standards folder not found: {base_path}")
    st.stop()

def get_companies(path: str):
    try:
        return sorted(
            [
                f for f in os.listdir(path)
                if os.path.isdir(os.path.join(path, f))
            ]
        )
    except Exception as e:
        st.error(f"Error reading standards folders: {e}")
        return []

companies = get_companies(base_path)

if not companies:
    st.info("No standards folders found yet.")
    st.stop()

company = st.selectbox("Select Company", companies)
company_path = os.path.join(base_path, company)

files = []
for root, dirs, filenames in os.walk(company_path):
    dirs.sort()
    for filename in sorted(filenames):
        if filename.lower().endswith((".pdf", ".doc", ".docx", ".txt")):
            files.append(os.path.join(root, filename))

if not files:
    st.warning("No standards files found in that company folder.")
    st.stop()

display_names = [os.path.relpath(file_path, company_path) for file_path in files]
selected_display = st.selectbox("Select Document", display_names)
selected_path = files[display_names.index(selected_display)]

st.markdown("### Selected Document")
st.write(f"**Company:** {company}")
st.write(f"**File:** {selected_display}")
st.code(selected_path)

btn1, btn2 = st.columns(2)
with btn1:
    if st.button("Open File", use_container_width=True):
        webbrowser.open(selected_path)

with btn2:
    if st.button("Open Folder", use_container_width=True):
        webbrowser.open(company_path)