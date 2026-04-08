import os
import csv
from datetime import datetime

import streamlit as st
from utils.ui_helpers import render_sidebar_nav
from data.machines_data import MACHINES

st.set_page_config(
    page_title="Machines",
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
</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Machines")

st.title("Machines")
st.caption("Empower MFG - Programming Reference")

machine_names = list(MACHINES.keys())
selected_machine = st.selectbox("Select Machine", machine_names)
machine = MACHINES[selected_machine]


def show_section(title, key):
    data = machine.get(key, [])
    if data:
        st.markdown(f"### {title}")
        for item in data:
            st.write(f"- {item}")
        st.markdown("")


def save_machine_note(machine_name, note_text):
    os.makedirs("data", exist_ok=True)
    log_path = os.path.join("data", "machine_change_log.csv")
    file_exists = os.path.isfile(log_path)

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "machine", "note"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            machine_name,
            note_text.strip()
        ])


st.markdown("## Overview")
show_section("Overview", "overview")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    show_section("Program Behavior", "program_behavior")
    show_section("Post Limits", "post_limits")
    show_section("Code Rules", "code_rules")

with col2:
    show_section("Shop Notes", "shop_notes")
    show_section("Special Notes", "special_notes")

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    show_section("Workholding", "workholding")
    show_section("Tooling", "tooling")
    show_section("Turning Notes", "turning_notes")
    show_section("Drilling Notes", "drilling_notes")

with col4:
    show_section("Posting / CIMCO Checks", "posting_cimco")
    show_section("Offset Logic", "offset_logic")
    show_section("Mastercam Rules", "mastercam_rules")
    show_section("Milling Notes", "milling_notes")
    show_section("Live Tooling Notes", "live_tooling_notes")

st.markdown("---")
st.markdown("## Machine Change / Correction Log")

with st.expander("Add machine note / correction", expanded=False):
    note_text = st.text_area(
        "Type machine changes, post issues, setup corrections, or notes to send later",
        height=180,
        placeholder=(
            "Example:\n"
            "- 432 steady rest location note needs updated\n"
            "- 421 post output needs safer retract after groove\n"
            "- 655 drill cycle note should mention peck behavior"
        )
    )

    if st.button("Save Machine Note"):
        if note_text.strip():
            save_machine_note(selected_machine, note_text)
            st.success(f"Saved note for {selected_machine}")
        else:
            st.warning("Enter a note before saving.")