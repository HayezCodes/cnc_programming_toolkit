import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from utils.ui_helpers import render_sidebar_nav

from utils.checklist_utils import build_job_folder_path, open_job_folder
from data.machines_data import MACHINES

st.set_page_config(
    page_title="Checklist",
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

render_sidebar_nav("Checklist")

st.title("Checklist")
st.caption("Empower MFG - Built for Joshua")

os.makedirs("data", exist_ok=True)
DB_PATH = Path("data/checklist_logs.db")


# -------------------------
# DB
# -------------------------
def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS checklist_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                saved_at TEXT NOT NULL,
                submitted_at TEXT,
                job_number TEXT,
                drawing_number TEXT,
                revision TEXT,
                customer TEXT,
                programmer TEXT,
                machine TEXT,
                material TEXT,
                notes TEXT,
                drawing_json TEXT NOT NULL,
                solidworks_json TEXT NOT NULL,
                mastercam_json TEXT NOT NULL,
                cimco_json TEXT NOT NULL,
                drawing_complete INTEGER NOT NULL,
                solidworks_complete INTEGER NOT NULL,
                mastercam_complete INTEGER NOT NULL,
                cimco_complete INTEGER NOT NULL,
                overall_complete INTEGER NOT NULL
            )
            """
        )

        existing_cols = [row[1] for row in conn.execute("PRAGMA table_info(checklist_logs)").fetchall()]

        if "machine" not in existing_cols:
            conn.execute("ALTER TABLE checklist_logs ADD COLUMN machine TEXT")

        if "material" not in existing_cols:
            conn.execute("ALTER TABLE checklist_logs ADD COLUMN material TEXT")

        conn.commit()


def get_default_state(items):
    return {item: False for item in items}


def load_saved_records():
    try:
        with get_conn() as conn:
            query = """
                SELECT
                    id,
                    status,
                    saved_at,
                    submitted_at,
                    job_number,
                    drawing_number,
                    revision,
                    customer,
                    programmer,
                    machine,
                    material,
                    notes,
                    drawing_json,
                    solidworks_json,
                    mastercam_json,
                    cimco_json,
                    drawing_complete,
                    solidworks_complete,
                    mastercam_complete,
                    cimco_complete,
                    overall_complete
                FROM checklist_logs
                ORDER BY id DESC
            """
            return pd.read_sql_query(query, conn)
    except Exception:
        return pd.DataFrame()


def parse_json_state(value, fallback_items):
    try:
        parsed = json.loads(value) if value else {}
        if isinstance(parsed, dict):
            return {item: bool(parsed.get(item, False)) for item in fallback_items}
    except Exception:
        pass
    return get_default_state(fallback_items)


def load_selected_record(record_row):
    default_machine = list(MACHINES.keys())[0] if MACHINES else ""
    loaded_machine = record_row["machine"] if "machine" in record_row.index and pd.notna(record_row["machine"]) else default_machine

    if loaded_machine not in MACHINES and MACHINES:
        loaded_machine = default_machine

    loaded_material = ""
    if "material" in record_row.index and pd.notna(record_row["material"]):
        loaded_material = str(record_row["material"]).strip().upper()

    return {
        "job_number": record_row["job_number"] or "",
        "drawing_number": record_row["drawing_number"] or "",
        "revision": record_row["revision"] or "",
        "customer": record_row["customer"] or "",
        "programmer": record_row["programmer"] or "",
        "machine": loaded_machine,
        "material": loaded_material,
        "notes": record_row["notes"] or "",
        "drawing_state": parse_json_state(record_row["drawing_json"], DRAWING_MARKUP_ITEMS),
        "solidworks_state": parse_json_state(record_row["solidworks_json"], SOLIDWORKS_ITEMS),
        "mastercam_state": parse_json_state(record_row["mastercam_json"], MASTERCAM_ITEMS),
        "cimco_state": parse_json_state(record_row["cimco_json"], CIMCO_ITEMS),
    }


def save_record(
    status,
    submitted_at,
    job_number,
    drawing_number,
    revision,
    customer,
    programmer,
    machine,
    material,
    notes,
    drawing_state,
    solidworks_state,
    mastercam_state,
    cimco_state,
    drawing_complete,
    solidworks_complete,
    mastercam_complete,
    cimco_complete,
    overall_complete,
):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO checklist_logs (
                status,
                saved_at,
                submitted_at,
                job_number,
                drawing_number,
                revision,
                customer,
                programmer,
                machine,
                material,
                notes,
                drawing_json,
                solidworks_json,
                mastercam_json,
                cimco_json,
                drawing_complete,
                solidworks_complete,
                mastercam_complete,
                cimco_complete,
                overall_complete
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                status,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                submitted_at,
                job_number,
                drawing_number,
                revision,
                customer,
                programmer,
                machine,
                material,
                notes,
                json.dumps(drawing_state),
                json.dumps(solidworks_state),
                json.dumps(mastercam_state),
                json.dumps(cimco_state),
                int(drawing_complete),
                int(solidworks_complete),
                int(mastercam_complete),
                int(cimco_complete),
                int(overall_complete),
            ),
        )
        conn.commit()


# -------------------------
# TXT EXPORT MIRROR
# -------------------------
def export_checklist_txt(
    job_number,
    drawing_number,
    revision,
    customer,
    programmer,
    machine,
    material,
    notes,
    drawing_state,
    solidworks_state,
    mastercam_state,
    cimco_state,
    status_label,
):
    os.makedirs("data/checklist_exports", exist_ok=True)

    safe_job = job_number.strip() if job_number.strip() else "NO_JOB"
    filename = f"{safe_job}_{status_label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join("data/checklist_exports", filename)

    def section_to_text(title, data):
        lines = [f"\n=== {title} ==="]
        for k, v in data.items():
            mark = "✔" if v else "✘"
            lines.append(f"{mark} {k}")
        return "\n".join(lines)

    content = f"""
CHECKLIST EXPORT
========================
Status: {status_label.upper()}
Job: {job_number}
Drawing: {drawing_number}
Revision: {revision}
Customer: {customer}
Programmer: {programmer}
Machine: {machine}
Material: {material}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

NOTES:
{notes}

{section_to_text("DRAWING", drawing_state)}
{section_to_text("SOLIDWORKS", solidworks_state)}
{section_to_text("MASTERCAM", mastercam_state)}
{section_to_text("CIMCO", cimco_state)}
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

    return path


# -------------------------
# CHECKLIST ITEMS
# -------------------------
DRAWING_MARKUP_ITEMS = [
    "Yellow - Grind stock diameters",
    "Light Blue - To-size diameters",
    "Light Green - Length dimensions",
    "Grey - Radii and edge breaks",
    "Red - Keyways",
    "Dark Blue - End work",
    "Purple - Threads",
    "Dimensions checked in correct order",
]

SOLIDWORKS_ITEMS = [
    "Base shaft geometry complete",
    "Undercuts added where required",
    "Threads modeled correctly (mean major)",
    "Thread relief and chamfers correct",
    "Grooves verified for width and depth",
    "Keyway verified",
    "End work modeled correctly",
    "Edge breaks correct per print",
    "Grind stock correct per side and in correct locations",
    "Final model matches print before CAM",
]

MASTERCAM_ITEMS = [
    "Correct machine and post selected",
    "Part aligned correctly",
    "Stock defined correctly",
    "Wireframe created for toolpaths",
    "Steady rest / tailstock defined if needed",
    "All tools selected before chaining",
    "Roughing verified (tool, DOC, direction)",
    "Finishing passes verified",
    "Keyway verified",
    "Tool order logical",
    "Offsets make sense",
    "Verify backplot",
]

CIMCO_ITEMS = [
    "Header complete (Part Number, Drawing Number + Rev, Machine)",
    "Tools not starting in material",
    "Safe start confirmed",
    "No rapid crashes or jumps",
    "Spindle directions correct",
    "Drill and tap depths correct",
    "Keyway depth, width, and length correct",
    "Proper offsets for milling programs",
    "Verify backplot",
    "Confident handing to operator",
    "Program placed in Predator machine file location",
]


# -------------------------
# ACTIVE CHECKLIST SESSION STATE
# -------------------------
def ensure_active_checklist_initialized():
    default_machine = list(MACHINES.keys())[0] if MACHINES else ""

    defaults = {
        "active_checklist_job_number": "",
        "active_checklist_drawing_number": "",
        "active_checklist_revision": "",
        "active_checklist_customer": "",
        "active_checklist_programmer": "",
        "active_checklist_machine": default_machine,
        "active_checklist_material": "",
        "active_checklist_notes": "",
        "active_checklist_drawing_state": get_default_state(DRAWING_MARKUP_ITEMS),
        "active_checklist_solidworks_state": get_default_state(SOLIDWORKS_ITEMS),
        "active_checklist_mastercam_state": get_default_state(MASTERCAM_ITEMS),
        "active_checklist_cimco_state": get_default_state(CIMCO_ITEMS),
        "active_checklist_loaded_label": "New Checklist",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_active_checklist_into_session(data, label="Loaded Checklist"):
    st.session_state["active_checklist_job_number"] = data["job_number"]
    st.session_state["active_checklist_drawing_number"] = data["drawing_number"]
    st.session_state["active_checklist_revision"] = data["revision"]
    st.session_state["active_checklist_customer"] = data["customer"]
    st.session_state["active_checklist_programmer"] = data["programmer"]
    st.session_state["active_checklist_machine"] = data["machine"]
    st.session_state["active_checklist_material"] = data["material"]
    st.session_state["active_checklist_notes"] = data["notes"]
    st.session_state["active_checklist_drawing_state"] = data["drawing_state"]
    st.session_state["active_checklist_solidworks_state"] = data["solidworks_state"]
    st.session_state["active_checklist_mastercam_state"] = data["mastercam_state"]
    st.session_state["active_checklist_cimco_state"] = data["cimco_state"]
    st.session_state["active_checklist_loaded_label"] = label

    st.session_state["job_number_input"] = data["job_number"]
    st.session_state["drawing_number_input"] = data["drawing_number"]
    st.session_state["revision_input"] = data["revision"]
    st.session_state["customer_input"] = data["customer"]
    st.session_state["programmer_input"] = data["programmer"]
    st.session_state["machine_input"] = data["machine"]
    st.session_state["material_input"] = data["material"]
    st.session_state["notes_input"] = data["notes"]

    for idx, item in enumerate(DRAWING_MARKUP_ITEMS):
        st.session_state[f"drawing_{idx}"] = data["drawing_state"].get(item, False)

    for idx, item in enumerate(SOLIDWORKS_ITEMS):
        st.session_state[f"solidworks_{idx}"] = data["solidworks_state"].get(item, False)

    for idx, item in enumerate(MASTERCAM_ITEMS):
        st.session_state[f"mastercam_{idx}"] = data["mastercam_state"].get(item, False)

    for idx, item in enumerate(CIMCO_ITEMS):
        st.session_state[f"cimco_{idx}"] = data["cimco_state"].get(item, False)


def clear_active_checklist():
    default_machine = list(MACHINES.keys())[0] if MACHINES else ""
    load_active_checklist_into_session(
        {
            "job_number": "",
            "drawing_number": "",
            "revision": "",
            "customer": "",
            "programmer": "",
            "machine": default_machine,
            "material": "",
            "notes": "",
            "drawing_state": get_default_state(DRAWING_MARKUP_ITEMS),
            "solidworks_state": get_default_state(SOLIDWORKS_ITEMS),
            "mastercam_state": get_default_state(MASTERCAM_ITEMS),
            "cimco_state": get_default_state(CIMCO_ITEMS),
        },
        label="New Checklist"
    )


def collect_section_state(section_key, items):
    current_state = {}
    checked_count = 0

    for idx, item in enumerate(items):
        widget_key = f"{section_key}_{idx}"
        val = bool(st.session_state.get(widget_key, False))
        current_state[item] = val
        if val:
            checked_count += 1

    total = len(items)
    return current_state, checked_count, total


def sync_active_states_from_widgets():
    st.session_state["active_checklist_job_number"] = st.session_state.get("job_number_input", "").strip().upper()
    st.session_state["active_checklist_drawing_number"] = st.session_state.get("drawing_number_input", "").strip()
    st.session_state["active_checklist_revision"] = st.session_state.get("revision_input", "").strip().upper()
    st.session_state["active_checklist_customer"] = st.session_state.get("customer_input", "").strip()
    st.session_state["active_checklist_programmer"] = st.session_state.get("programmer_input", "").strip()

    default_machine = list(MACHINES.keys())[0] if MACHINES else ""
    machine_val = st.session_state.get("machine_input", default_machine)
    if machine_val not in MACHINES and MACHINES:
        machine_val = default_machine
    st.session_state["active_checklist_machine"] = machine_val

    st.session_state["active_checklist_material"] = st.session_state.get("material_input", "").strip().upper()
    st.session_state["active_checklist_notes"] = st.session_state.get("notes_input", "")

    drawing_state, _, _ = collect_section_state("drawing", DRAWING_MARKUP_ITEMS)
    solidworks_state, _, _ = collect_section_state("solidworks", SOLIDWORKS_ITEMS)
    mastercam_state, _, _ = collect_section_state("mastercam", MASTERCAM_ITEMS)
    cimco_state, _, _ = collect_section_state("cimco", CIMCO_ITEMS)

    st.session_state["active_checklist_drawing_state"] = drawing_state
    st.session_state["active_checklist_solidworks_state"] = solidworks_state
    st.session_state["active_checklist_mastercam_state"] = mastercam_state
    st.session_state["active_checklist_cimco_state"] = cimco_state


def initialize_widget_values_from_active_state():
    if "job_number_input" not in st.session_state:
        st.session_state["job_number_input"] = st.session_state["active_checklist_job_number"]
    if "drawing_number_input" not in st.session_state:
        st.session_state["drawing_number_input"] = st.session_state["active_checklist_drawing_number"]
    if "revision_input" not in st.session_state:
        st.session_state["revision_input"] = st.session_state["active_checklist_revision"]
    if "customer_input" not in st.session_state:
        st.session_state["customer_input"] = st.session_state["active_checklist_customer"]
    if "programmer_input" not in st.session_state:
        st.session_state["programmer_input"] = st.session_state["active_checklist_programmer"]
    if "machine_input" not in st.session_state:
        st.session_state["machine_input"] = st.session_state["active_checklist_machine"]
    if "material_input" not in st.session_state:
        st.session_state["material_input"] = st.session_state["active_checklist_material"]
    if "notes_input" not in st.session_state:
        st.session_state["notes_input"] = st.session_state["active_checklist_notes"]

    for idx, item in enumerate(DRAWING_MARKUP_ITEMS):
        key = f"drawing_{idx}"
        if key not in st.session_state:
            st.session_state[key] = st.session_state["active_checklist_drawing_state"].get(item, False)

    for idx, item in enumerate(SOLIDWORKS_ITEMS):
        key = f"solidworks_{idx}"
        if key not in st.session_state:
            st.session_state[key] = st.session_state["active_checklist_solidworks_state"].get(item, False)

    for idx, item in enumerate(MASTERCAM_ITEMS):
        key = f"mastercam_{idx}"
        if key not in st.session_state:
            st.session_state[key] = st.session_state["active_checklist_mastercam_state"].get(item, False)

    for idx, item in enumerate(CIMCO_ITEMS):
        key = f"cimco_{idx}"
        if key not in st.session_state:
            st.session_state[key] = st.session_state["active_checklist_cimco_state"].get(item, False)


def section_ui(section_key, title, items):
    st.markdown(f"### {title}")
    checked_count = 0

    for idx, item in enumerate(items):
        widget_key = f"{section_key}_{idx}"
        val = st.checkbox(item, key=widget_key)
        if val:
            checked_count += 1

    total = len(items)
    st.progress(checked_count / total if total else 0)
    st.caption(f"{checked_count}/{total}")
    st.markdown("---")
    return checked_count, total


init_db()
records_df = load_saved_records()
ensure_active_checklist_initialized()
initialize_widget_values_from_active_state()

load_options = ["Keep Current Active Checklist", "New Blank Checklist"]
if not records_df.empty:
    for _, row in records_df.iterrows():
        status = row["status"] or "unknown"
        job = row["job_number"] or "NO JOB"
        saved = row["saved_at"] or ""
        load_options.append(f"{status.upper()} | {job} | {saved}")

selected_load = st.selectbox("Checklist Load Options", load_options)

load_col1, load_col2 = st.columns([1, 1])

with load_col1:
    if st.button("Load Selected Option", width="stretch"):
        if selected_load == "Keep Current Active Checklist":
            st.success("Kept current active checklist.")
        elif selected_load == "New Blank Checklist":
            clear_active_checklist()
            st.success("Started new blank checklist.")
            st.rerun()
        else:
            selected_index = load_options.index(selected_load) - 2
            selected_row = records_df.iloc[selected_index]
            loaded_data = load_selected_record(selected_row)
            load_active_checklist_into_session(loaded_data, label=selected_load)
            st.success("Loaded saved checklist into active session.")
            st.rerun()

with load_col2:
    if st.button("Clear Active Checklist", width="stretch"):
        clear_active_checklist()
        st.success("Active checklist cleared.")
        st.rerun()

sync_active_states_from_widgets()

active_job = st.session_state["active_checklist_job_number"]
active_label = st.session_state.get("active_checklist_loaded_label", "New Checklist")

if active_job:
    st.info(f"ACTIVE CHECKLIST: {active_job}  |  SOURCE: {active_label}")
else:
    st.info(f"ACTIVE CHECKLIST: NONE  |  SOURCE: {active_label}")

st.markdown("## Job Info")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.text_input("Job Number", key="job_number_input")
with c2:
    st.text_input("Drawing Number", key="drawing_number_input")
with c3:
    st.text_input("Revision", key="revision_input")
with c4:
    machine_names = list(MACHINES.keys())
    if not machine_names:
        machine_names = [""]
    current_machine = st.session_state.get("machine_input", machine_names[0])
    if current_machine not in machine_names:
        current_machine = machine_names[0]
    machine_index = machine_names.index(current_machine)
    st.selectbox("Machine", machine_names, index=machine_index, key="machine_input")

sync_active_states_from_widgets()
job_number = st.session_state["active_checklist_job_number"]
drawing_number = st.session_state["active_checklist_drawing_number"]
revision = st.session_state["active_checklist_revision"]
machine = st.session_state["active_checklist_machine"]

job_col1, job_col2 = st.columns(2)

with job_col1:
    if st.button("🚀 Open Job Folder", width="stretch"):
        success, message = open_job_folder(job_number)
        if success:
            st.success(message)
        else:
            st.error(message)

with job_col2:
    if job_number:
        try:
            preview_path = build_job_folder_path(job_number)
            st.info(f"Path Preview:\n{preview_path}")
        except Exception as e:
            st.warning(str(e))

c5, c6, c7 = st.columns(3)
with c5:
    st.text_input("Customer", key="customer_input")
with c6:
    st.text_input("Programmer", key="programmer_input")
with c7:
    st.text_input("Material *", key="material_input", placeholder="17-4 / 4140 / ALLOY 20")

st.text_area("Notes", height=120, key="notes_input")

sync_active_states_from_widgets()
customer = st.session_state["active_checklist_customer"]
programmer = st.session_state["active_checklist_programmer"]
material = st.session_state["active_checklist_material"]
notes = st.session_state["active_checklist_notes"]
machine = st.session_state["active_checklist_machine"]
machine_data = MACHINES.get(machine, {})

st.markdown("---")
st.markdown("## Selected Machine")

if machine_data:
    st.markdown(f"### {machine}")

    mc1, mc2 = st.columns(2)

    with mc1:
        for section in ["overview", "shop_notes", "workholding"]:
            if machine_data.get(section):
                st.markdown(f"#### {section.replace('_', ' ').title()}")
                for item in machine_data[section]:
                    st.write(f"- {item}")

    with mc2:
        for section in ["posting_cimco", "mastercam_rules", "special_notes"]:
            if machine_data.get(section):
                st.markdown(f"#### {section.replace('_', ' ').title()}")
                for item in machine_data[section]:
                    st.write(f"- {item}")

st.markdown("---")
st.markdown("## Checklist")

drawing_checked, drawing_total = section_ui(
    "drawing",
    "Drawing",
    DRAWING_MARKUP_ITEMS
)

solidworks_checked, sw_total = section_ui(
    "solidworks",
    "SolidWorks",
    SOLIDWORKS_ITEMS
)

mastercam_checked, mc_total = section_ui(
    "mastercam",
    "Mastercam",
    MASTERCAM_ITEMS
)

cimco_checked, cimco_total = section_ui(
    "cimco",
    "CIMCO",
    CIMCO_ITEMS
)

sync_active_states_from_widgets()

drawing_state = st.session_state["active_checklist_drawing_state"]
solidworks_state = st.session_state["active_checklist_solidworks_state"]
mastercam_state = st.session_state["active_checklist_mastercam_state"]
cimco_state = st.session_state["active_checklist_cimco_state"]

drawing_complete = drawing_checked == drawing_total
solidworks_complete = solidworks_checked == sw_total
mastercam_complete = mastercam_checked == mc_total
cimco_complete = cimco_checked == cimco_total
overall_complete = all([
    drawing_complete,
    solidworks_complete,
    mastercam_complete,
    cimco_complete
])

st.markdown("## Summary")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Drawing", f"{drawing_checked}/{drawing_total}")
s2.metric("SolidWorks", f"{solidworks_checked}/{sw_total}")
s3.metric("Mastercam", f"{mastercam_checked}/{mc_total}")
s4.metric("CIMCO", f"{cimco_checked}/{cimco_total}")

if overall_complete:
    st.success("Checklist Complete")
else:
    st.warning("Checklist Incomplete")

btn1, btn2 = st.columns(2)

with btn1:
    if st.button("Save Draft", width="stretch"):
        if not job_number.strip():
            st.error("Job Number required to save draft.")
        elif not material.strip():
            st.error("Material is required to save draft.")
        else:
            save_record(
                status="draft",
                submitted_at=None,
                job_number=job_number,
                drawing_number=drawing_number,
                revision=revision,
                customer=customer,
                programmer=programmer,
                machine=machine,
                material=material,
                notes=notes,
                drawing_state=drawing_state,
                solidworks_state=solidworks_state,
                mastercam_state=mastercam_state,
                cimco_state=cimco_state,
                drawing_complete=drawing_complete,
                solidworks_complete=solidworks_complete,
                mastercam_complete=mastercam_complete,
                cimco_complete=cimco_complete,
                overall_complete=overall_complete,
            )

            export_path = export_checklist_txt(
                job_number,
                drawing_number,
                revision,
                customer,
                programmer,
                machine,
                material,
                notes,
                drawing_state,
                solidworks_state,
                mastercam_state,
                cimco_state,
                "draft",
            )

            st.success(f"Draft saved + exported to: {export_path}")

with btn2:
    if st.button("Submit Checklist", width="stretch"):
        if not job_number.strip():
            st.error("Job Number required to submit checklist.")
        elif not material.strip():
            st.error("Material is required to submit checklist.")
        else:
            submitted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            save_record(
                status="submitted",
                submitted_at=submitted_time,
                job_number=job_number,
                drawing_number=drawing_number,
                revision=revision,
                customer=customer,
                programmer=programmer,
                machine=machine,
                material=material,
                notes=notes,
                drawing_state=drawing_state,
                solidworks_state=solidworks_state,
                mastercam_state=mastercam_state,
                cimco_state=cimco_state,
                drawing_complete=drawing_complete,
                solidworks_complete=solidworks_complete,
                mastercam_complete=mastercam_complete,
                cimco_complete=cimco_complete,
                overall_complete=overall_complete,
            )

            export_path = export_checklist_txt(
                job_number,
                drawing_number,
                revision,
                customer,
                programmer,
                machine,
                material,
                notes,
                drawing_state,
                solidworks_state,
                mastercam_state,
                cimco_state,
                "submitted",
            )

            st.success(f"Checklist submitted + exported to: {export_path}")

st.markdown("---")
st.markdown("## Recent Checklist Log")

records_df = load_saved_records()

if not records_df.empty:
    display_cols = [
        "status",
        "saved_at",
        "submitted_at",
        "job_number",
        "drawing_number",
        "revision",
        "customer",
        "programmer",
    ]

    if "machine" in records_df.columns:
        display_cols.append("machine")

    if "material" in records_df.columns:
        display_cols.append("material")

    display_cols.append("overall_complete")

    display_df = records_df[display_cols].copy()

    display_df["overall_complete"] = display_df["overall_complete"].map(
        lambda x: "Yes" if int(x) == 1 else "No"
    )

    st.dataframe(display_df, width="stretch", hide_index=True)
else:
    st.info("No checklist records saved yet.")