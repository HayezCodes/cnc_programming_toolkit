import math
import streamlit as st
from data.materials import LATHE_MATERIALS, MILL_MATERIALS, DRILL_DATA, OPERATOR_NOTES
from utils.formulas import rpm_from_sfm, ipm_from_ipr, drill_feed_ipm, tap_feed_ipm_from_tpi
from utils.ui_helpers import render_sidebar_nav, render_cutting_mode_sidebar

st.set_page_config(
    page_title="Speeds & Feeds",
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

render_sidebar_nav("Speeds & Feeds")
render_cutting_mode_sidebar()

st.title("Speeds & Feeds")
st.caption("Empower MFG - Built for Joshua")

CENTER_DRILL_PRESETS = {
    "00": {"style": "Plain", "angle": 60.0, "pilot": 0.015625, "body": 0.1250, "pilot_length": 0.015625},
    "0": {"style": "Plain", "angle": 60.0, "pilot": 0.031250, "body": 0.1250, "pilot_length": 0.031250},
    "1": {"style": "Plain", "angle": 60.0, "pilot": 0.046875, "body": 0.1250, "pilot_length": 0.046875},
    "2": {"style": "Plain", "angle": 60.0, "pilot": 0.078125, "body": 0.1875, "pilot_length": 0.078125},
    "3": {"style": "Plain", "angle": 60.0, "pilot": 0.109375, "body": 0.2500, "pilot_length": 0.109375},
    "4": {"style": "Plain", "angle": 60.0, "pilot": 0.125000, "body": 0.3125, "pilot_length": 0.125000},
    "5": {"style": "Plain", "angle": 60.0, "pilot": 0.187500, "body": 0.4375, "pilot_length": 0.187500},
    "6": {"style": "Plain", "angle": 60.0, "pilot": 0.218750, "body": 0.5000, "pilot_length": 0.218750},
    "7": {"style": "Plain", "angle": 60.0, "pilot": 0.250000, "body": 0.6250, "pilot_length": 0.250000},
    "8": {"style": "Plain", "angle": 60.0, "pilot": 0.312500, "body": 0.7500, "pilot_length": 0.312500},
    "9": {"style": "Plain", "angle": 60.0, "pilot": 0.375000, "body": 0.8750, "pilot_length": 0.375000},
    "10": {"style": "Plain", "angle": 60.0, "pilot": 0.500000, "body": 1.2500, "pilot_length": 0.500000},
    "11": {"style": "Bell", "angle": 120.0, "pilot": 0.046875, "body": 0.1250, "bell": 0.1900, "pilot_length": 0.046875},
    "12": {"style": "Bell", "angle": 120.0, "pilot": 0.062500, "body": 0.1875, "bell": 0.2500, "pilot_length": 0.062500},
    "13": {"style": "Bell", "angle": 120.0, "pilot": 0.093750, "body": 0.2500, "bell": 0.3100, "pilot_length": 0.093750},
    "14": {"style": "Bell", "angle": 120.0, "pilot": 0.109375, "body": 0.3125, "bell": 0.4000, "pilot_length": 0.109375},
    "15": {"style": "Bell", "angle": 120.0, "pilot": 0.156250, "body": 0.4375, "bell": 0.5000, "pilot_length": 0.156250},
    "16": {"style": "Bell", "angle": 120.0, "pilot": 0.187500, "body": 0.5000, "bell": 0.5900, "pilot_length": 0.187500},
    "17": {"style": "Bell", "angle": 120.0, "pilot": 0.218750, "body": 0.6250, "bell": 0.6900, "pilot_length": 0.218750},
    "18": {"style": "Bell", "angle": 120.0, "pilot": 0.250000, "body": 0.7500, "bell": 0.7800, "pilot_length": 0.250000},
}


def apply_cut_mode(value, kind="sfm"):
    return value


def to_display_units(value_in: float, unit_mode: str) -> float:
    return value_in if unit_mode == "STANDARD" else value_in * 25.4


def from_display_units(value: float, unit_mode: str) -> float:
    return value if unit_mode == "STANDARD" else value / 25.4


def unit_label(unit_mode: str) -> str:
    return "in" if unit_mode == "STANDARD" else "mm"


def unit_step(step_in: float, unit_mode: str) -> float:
    return step_in if unit_mode == "STANDARD" else step_in * 25.4


def diameter_input(label: str, key: str, unit_mode: str, value_in: float, step_in: float, min_in: float = 0.001) -> float:
    display_value = st.number_input(
        f"{label} ({unit_label(unit_mode)})",
        min_value=to_display_units(min_in, unit_mode),
        value=to_display_units(value_in, unit_mode),
        step=unit_step(step_in, unit_mode),
        format="%.4f",
        key=key
    )
    return from_display_units(display_value, unit_mode)


def format_length(value_in: float, unit_mode: str) -> str:
    return f"{to_display_units(value_in, unit_mode):.4f} {unit_label(unit_mode)}"


def calculate_spot_depth(target_diameter_in: float, included_angle_deg: float) -> float:
    return target_diameter_in / (2 * math.tan(math.radians(included_angle_deg / 2)))


def calculate_center_drill_depth(
    pilot_diameter_in: float,
    target_bell_diameter_in: float,
    included_angle_deg: float,
    pilot_length_in: float,
) -> float:
    chamfer_depth = (target_bell_diameter_in - pilot_diameter_in) / (2 * math.tan(math.radians(included_angle_deg / 2)))
    return chamfer_depth + pilot_length_in


def calculate_center_drill_usable_depth(
    pilot_diameter_in: float,
    body_diameter_in: float,
    included_angle_deg: float,
    pilot_length_in: float,
) -> float:
    return calculate_center_drill_depth(pilot_diameter_in, body_diameter_in, included_angle_deg, pilot_length_in)


def get_operator_notes(material_name: str):
    if "Titanium" in material_name:
        return OPERATOR_NOTES["Titanium"]
    if "Duplex" in material_name or "Alloy 20" in material_name:
        return OPERATOR_NOTES["Duplex"]
    if "Hastelloy" in material_name:
        return OPERATOR_NOTES["Hastelloy"]
    if "Monel" in material_name:
        return OPERATOR_NOTES["Monel"]
    if "Zirconium" in material_name:
        return OPERATOR_NOTES["Zirconium"]
    if "Steel" in material_name or "17-4" in material_name or "300" in material_name:
        return OPERATOR_NOTES["Steel"]
    return OPERATOR_NOTES["General"]


def render_operator_notes(material_name: str, title="Operator Notes"):
    notes = get_operator_notes(material_name)
    st.markdown("---")
    st.markdown(f"### {title}")
    for line in notes:
        st.write(line)


def get_hif_feed_data(material_name: str):
    if material_name == "10 Series Steel":
        return {"sfm_range": "350 - 700", "ipt_range": ".004 - .015", "axial_doc": ".008 - .016", "chip_thickness": ".002 - .006", "coolant": "No", "grade_note": "Steel family hi-feed starting range"}
    if material_name == "40 Series Steel":
        return {"sfm_range": "350 - 700", "ipt_range": ".004 - .015", "axial_doc": ".008 - .016", "chip_thickness": ".002 - .006", "coolant": "No", "grade_note": "Steel family hi-feed starting range"}
    if material_name == "17-4 / 300 Series":
        return {"sfm_range": "300 - 550", "ipt_range": ".004 - .0165", "axial_doc": ".008 - .016", "chip_thickness": ".002 - .006", "coolant": "Yes / may not be required at high speeds", "grade_note": "Stainless / 17-4 hi-feed starting range"}
    if material_name == "Duplex / Alloy 20":
        return {"sfm_range": "300 - 550", "ipt_range": ".004 - .0165", "axial_doc": ".008 - .016", "chip_thickness": ".002 - .006", "coolant": "Yes / may not be required at high speeds", "grade_note": "Use stainless-style hi-feed starting range"}
    if material_name == "Hastelloy":
        return {"sfm_range": "65 - 200", "ipt_range": ".004 - .015", "axial_doc": ".008 - .016", "chip_thickness": ".002 - .006", "coolant": "Yes", "grade_note": "High-temp alloy hi-feed starting range"}
    if material_name == "Titanium":
        return {"sfm_range": "85 - 200", "ipt_range": ".004 - .015", "axial_doc": ".008 - .016", "chip_thickness": ".002 - .006", "coolant": "Yes", "grade_note": "Titanium hi-feed starting range"}
    if material_name == "Monel":
        return {"sfm_range": "60 - 140", "ipt_range": ".0035 - .010", "axial_doc": ".006 - .012", "chip_thickness": ".0015 - .004", "coolant": "Yes", "grade_note": "Conservative Monel hi-feed starting range"}
    if material_name == "Zirconium":
        return {"sfm_range": "50 - 120", "ipt_range": ".0030 - .009", "axial_doc": ".006 - .012", "chip_thickness": ".0015 - .0035", "coolant": "Yes", "grade_note": "Conservative zirconium hi-feed starting range"}
    return {"sfm_range": "Check chart", "ipt_range": "Check chart", "axial_doc": "Check chart", "chip_thickness": "Check chart", "coolant": "Check chart", "grade_note": "No mapped hi-feed range"}


def get_center_drill_data(material_name: str):
    if material_name == "10 Series Steel":
        return {"sfm": 70, "ipr": 0.0025, "notes": "Conservative center drill baseline for 10 series steel."}
    if material_name == "40 Series Steel":
        return {"sfm": 65, "ipr": 0.0023, "notes": "Conservative center drill baseline for 40 series steel."}
    if material_name == "17-4 / 300 Series":
        return {"sfm": 45, "ipr": 0.0020, "notes": "Conservative center drill baseline for stainless / 17-4."}
    if material_name == "Duplex / Alloy 20":
        return {"sfm": 35, "ipr": 0.0018, "notes": "Conservative center drill baseline for duplex / alloy 20."}
    if material_name == "Hastelloy":
        return {"sfm": 25, "ipr": 0.0015, "notes": "Low-speed center drill baseline for Hastelloy."}
    if material_name == "Titanium":
        return {"sfm": 30, "ipr": 0.0015, "notes": "Conservative center drill baseline for titanium."}
    if material_name == "Monel":
        return {"sfm": 24, "ipr": 0.0014, "notes": "Conservative center drill baseline for Monel."}
    if material_name == "Zirconium":
        return {"sfm": 20, "ipr": 0.0012, "notes": "Very conservative center drill baseline for zirconium."}
    return {"sfm": 50, "ipr": 0.0020, "notes": "General center drill baseline."}


def center_drill_label(size_name: str) -> str:
    preset = CENTER_DRILL_PRESETS[size_name]
    return f"Size {size_name} | {preset['style']} | pilot {preset['pilot']:.4f} in"


def render_center_drill_size_selector(section_key: str):
    selected_size = st.selectbox(
        "Center Drill Size",
        list(CENTER_DRILL_PRESETS.keys()),
        format_func=center_drill_label,
        key=f"{section_key}_center_drill_size"
    )
    return selected_size, CENTER_DRILL_PRESETS[selected_size]


def render_center_drill_depth_block(section_key: str, center_drill_size: str, preset_data: dict, unit_mode: str):
    st.markdown("### Center Drill Depth")

    pilot_diameter_in = preset_data["pilot"]
    body_diameter_in = preset_data["body"]
    bell_diameter_in = preset_data.get("bell", body_diameter_in)
    pilot_length_in = preset_data["pilot_length"]
    included_angle = preset_data["angle"]
    target_default_in = min(bell_diameter_in, pilot_diameter_in + 0.0500)
    usable_depth_in = calculate_center_drill_usable_depth(
        pilot_diameter_in,
        bell_diameter_in,
        included_angle,
        pilot_length_in,
    )

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.metric("Center Drill Size", center_drill_size)
    with d2:
        st.metric("Style / Angle", f"{preset_data['style']} / {included_angle:.0f} deg")
    with d3:
        st.metric("Pilot Diameter", format_length(pilot_diameter_in, unit_mode))
    with d4:
        if "bell" in preset_data:
            st.metric(
                "Body / Bell Diameter",
                f"{to_display_units(body_diameter_in, unit_mode):.4f} / {to_display_units(bell_diameter_in, unit_mode):.4f} {unit_label(unit_mode)}"
            )
        else:
            st.metric("Body / Bell Diameter", format_length(body_diameter_in, unit_mode))

    p1, p2, p3 = st.columns(3)
    p1.metric("Practical Pilot Depth", format_length(usable_depth_in, unit_mode))
    p2.metric("Pilot Length (C)", format_length(pilot_length_in, unit_mode))
    p3.metric("Pilot Feed Basis", format_length(pilot_diameter_in, unit_mode))

    st.caption("Practical pilot depth uses the selected tool's stored pilot diameter, body diameter, angle, and pilot length.")

    target_bell_diameter_in = diameter_input(
        "Target Bell Diameter (Optional)",
        f"{section_key}_cd_target_bell",
        unit_mode,
        target_default_in,
        0.0010
    )

    if target_bell_diameter_in <= pilot_diameter_in:
        st.error("Target bell diameter must be larger than pilot diameter.")
        return

    required_depth_in = calculate_center_drill_depth(pilot_diameter_in, target_bell_diameter_in, included_angle, pilot_length_in)

    r1, r2, r3 = st.columns(3)
    r1.metric("Depth For Target Bell", format_length(required_depth_in, unit_mode))
    r2.metric("Bell Diameter", format_length(target_bell_diameter_in, unit_mode))
    r3.metric("Tool Limit", format_length(bell_diameter_in, unit_mode))

    if target_bell_diameter_in > bell_diameter_in:
        st.warning("Target bell diameter exceeds the tool body / bell diameter.")


st.markdown("### Diameter Units")
unit_mode = st.radio("Use diameter-style inputs in:", ["STANDARD", "METRIC"], horizontal=True, key="speeds_feeds_unit_mode")

main_tab1, main_tab2 = st.tabs(["Lathe", "Mill"])

with main_tab1:
    lathe_tab1, lathe_tab2, lathe_tab3, lathe_tab4 = st.tabs(["Turning", "Drilling", "Live Tooling Endmill", "Live Tooling Drill"])

    with lathe_tab1:
        st.subheader("Lathe Turning")
        col1, col2, col3 = st.columns(3)

        with col1:
            material = st.selectbox("Material", list(LATHE_MATERIALS.keys()), key="lathe_material")
        with col2:
            operation = st.selectbox("Operation", ["rough", "finish"], key="lathe_operation")
        with col3:
            diameter = diameter_input("Work Diameter", "lathe_dia", unit_mode, 2.0000, 0.1000)

        rec = LATHE_MATERIALS[material][operation]
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        ipr = apply_cut_mode(rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = ipm_from_ipr(ipr, rpm)

        st.markdown("### Recommendation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.markdown("### Setup Guidance")
        c1, c2 = st.columns(2)
        c1.metric("DOC Guidance", rec["doc"])
        c2.markdown(
            f"""
<div style="font-size: 0.85rem; line-height: 1.35;">
<b>Chipbreaker:</b><br>{rec["chipbreaker"]}
</div>
""",
            unsafe_allow_html=True,
        )

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material)

    with lathe_tab2:
        st.subheader("Lathe Drilling")

        col1, col2, col3 = st.columns(3)
        with col1:
            material_drill = st.selectbox("Material", list(DRILL_DATA.keys()), key="lathe_drill_material")
        with col2:
            drill_type = st.selectbox("Drill Type", ["HSS", "HSS Coated", "Cobalt", "CoroDrill", "Center Drill"], key="lathe_drill_type")
        with col3:
            if drill_type == "Center Drill":
                center_drill_size, center_drill_preset = render_center_drill_size_selector("lathe_drill")
                drill_diameter = center_drill_preset["pilot"]
            else:
                drill_diameter = diameter_input("Drill Diameter", "lathe_drill_dia", unit_mode, 0.5000, 0.0100)

        drill_rec = get_center_drill_data(material_drill) if drill_type == "Center Drill" else DRILL_DATA[material_drill][drill_type]

        sfm = apply_cut_mode(drill_rec["sfm"], "sfm")
        ipr = apply_cut_mode(drill_rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, drill_diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        st.markdown("### Drill Recommendation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        if drill_type == "Center Drill":
            st.write(f"**Center Drill Selected:** {center_drill_size} ({center_drill_preset['style']})")
            render_center_drill_depth_block("lathe_drill", center_drill_size, center_drill_preset, unit_mode)

        st.write(f"**Notes:** {drill_rec['notes']}")
        render_operator_notes(material_drill)

    with lathe_tab3:
        st.subheader("Lathe Live Tooling Endmill")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            material_live = st.selectbox("Material", list(MILL_MATERIALS.keys()), key="lathe_live_material")
        with col2:
            tool_style_live = st.selectbox("Tool Style", ["Standard Endmill", '1/2 Ingersoll Rougher (Hi-Feed)'], key="lathe_live_tool_style")
        with col3:
            flute_count_live = st.number_input("Flute Count", min_value=1, value=4, step=1, key="lathe_live_flutes")
        with col4:
            em_operation_live = st.selectbox("Operation", ["rough", "finish"], key="lathe_live_op")

        if tool_style_live == '1/2 Ingersoll Rougher (Hi-Feed)':
            tool_diameter_live = 0.5000
        else:
            tool_diameter_live = diameter_input("Endmill Diameter", "lathe_live_em_dia", unit_mode, 0.5000, 0.0100)

        st.write(f"**Diameter Used:** {format_length(tool_diameter_live, unit_mode)}")

        if tool_style_live == '1/2 Ingersoll Rougher (Hi-Feed)':
            hif = get_hif_feed_data(material_live)

            st.markdown("### Live Tooling Recommendation - HI-FEED INSERT MILL")
            c1, c2, c3 = st.columns(3)
            c1.metric("SFM Range", hif["sfm_range"])
            c2.metric("IPT Range", hif["ipt_range"])
            c3.metric("Axial DOC", hif["axial_doc"])

            d1, d2, d3 = st.columns(3)
            d1.metric("Chip Thickness", hif["chip_thickness"])
            d2.metric("Coolant", hif["coolant"])
            d3.metric("Tool", '1/2 Ingersoll Rougher')

            st.write(f"**Chart Note:** {hif['grade_note']}")
            st.write("**Application Note:** Use for keyways larger than .500 when using the hi-feed insert mill.")
            st.write("**Mode Note:** This chart is a roughing / hi-feed style recommendation.")
            render_operator_notes(material_live)
        else:
            rec_live = MILL_MATERIALS[material_live]["Endmill"]

            if em_operation_live == "rough":
                sfm_live = apply_cut_mode(rec_live["rough_sfm"], "sfm")
                ipt_live = apply_cut_mode(rec_live["rough_ipt"], "ipt")
                slot_doc_live = rec_live["rough_slot_doc_factor"] * tool_diameter_live
                side_doc_live = rec_live["rough_side_doc_factor"] * tool_diameter_live
                finish_note_live = rec_live["finish_radial"]
            else:
                sfm_live = apply_cut_mode(rec_live["finish_sfm"], "sfm")
                ipt_live = apply_cut_mode(rec_live["finish_ipt"], "ipt")
                slot_doc_live = rec_live["finish_slot_doc_factor"] * tool_diameter_live
                side_doc_live = rec_live["finish_side_doc_factor"] * tool_diameter_live
                finish_note_live = rec_live["finish_radial"]

            rpm_live = rpm_from_sfm(sfm_live, tool_diameter_live)
            ipm_live = rpm_live * flute_count_live * ipt_live

            st.markdown(f"### Live Tooling Recommendation - {em_operation_live.upper()}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SFM", f"{sfm_live:.0f}")
            c2.metric("RPM", f"{rpm_live:.0f}")
            c3.metric("Chipload (IPT)", f"{ipt_live:.4f}")
            c4.metric("Feed (IPM)", f"{ipm_live:.2f}")

            st.markdown("### DOC Guidance")
            d1, d2, d3 = st.columns(3)
            d1.metric("Slot DOC", format_length(slot_doc_live, unit_mode))
            d2.metric("Side DOC", format_length(side_doc_live, unit_mode))
            d3.metric("Finish Radial", finish_note_live)

            st.write(f"**Notes:** {rec_live['notes']}")
            render_operator_notes(material_live)

    with lathe_tab4:
        st.subheader("Lathe Live Tooling Drill")

        col1, col2, col3 = st.columns(3)
        with col1:
            material_live_drill = st.selectbox("Material", list(DRILL_DATA.keys()), key="lathe_live_drill_material")
        with col2:
            drill_type_live = st.selectbox("Drill Type", ["HSS", "HSS Coated", "Cobalt", "CoroDrill", "Center Drill"], key="lathe_live_drill_type")
        with col3:
            if drill_type_live == "Center Drill":
                center_drill_size_live, center_drill_preset_live = render_center_drill_size_selector("lathe_live_drill")
                drill_diameter_live = center_drill_preset_live["pilot"]
            else:
                drill_diameter_live = diameter_input("Drill Diameter", "lathe_live_drill_dia", unit_mode, 0.5000, 0.0100)

        drill_rec_live = get_center_drill_data(material_live_drill) if drill_type_live == "Center Drill" else DRILL_DATA[material_live_drill][drill_type_live]

        sfm_live = apply_cut_mode(drill_rec_live["sfm"], "sfm")
        ipr_live = apply_cut_mode(drill_rec_live["ipr"], "ipr")
        rpm_live = rpm_from_sfm(sfm_live, drill_diameter_live)
        ipm_live = drill_feed_ipm(rpm_live, ipr_live)

        st.markdown("### Live Tooling Drill Recommendation")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm_live:.0f}")
        c2.metric("RPM", f"{rpm_live:.0f}")
        c3.metric("Feed (IPR)", f"{ipr_live:.4f}")
        c4.metric("Feed (IPM)", f"{ipm_live:.2f}")

        if drill_type_live == "Center Drill":
            st.write(f"**Center Drill Selected:** {center_drill_size_live} ({center_drill_preset_live['style']})")
            render_center_drill_depth_block("lathe_live_drill", center_drill_size_live, center_drill_preset_live, unit_mode)

        st.write(f"**Notes:** {drill_rec_live['notes']}")
        render_operator_notes(material_live_drill)

with main_tab2:
    st.subheader("Mill Speeds & Feeds")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        material_mill = st.selectbox("Material", list(MILL_MATERIALS.keys()), key="mill_material")
    with col2:
        tool_type = st.selectbox("Tool Type", ["Spot Drill", "Center Drill", "Drill", "Tap", "Endmill"], key="mill_tool_type")
    with col3:
        if tool_type == "Endmill":
            em_operation = st.selectbox("Operation", ["rough", "finish"], key="mill_em_operation")
            drill_type_mill = None
            tool_style_mill = st.selectbox("Tool Style", ["Standard Endmill", '1/2 Ingersoll Rougher (Hi-Feed)'], key="mill_tool_style")
            spot_angle = None
        elif tool_type == "Drill":
            drill_type_mill = st.selectbox("Drill Type", ["HSS", "HSS Coated", "Cobalt", "CoroDrill"], key="mill_drill_type")
            em_operation = None
            tool_style_mill = None
            spot_angle = None
        elif tool_type == "Spot Drill":
            em_operation = None
            drill_type_mill = None
            tool_style_mill = None
            spot_angle = st.number_input("Included Angle (deg)", min_value=1.0, max_value=179.0, value=90.0, step=1.0, format="%.1f", key="spot_angle")
        else:
            em_operation = None
            drill_type_mill = None
            tool_style_mill = None
            spot_angle = None
            st.write("")
    with col4:
        if tool_type == "Spot Drill":
            diameter = diameter_input("Spot Drill Diameter", "spot_dia", unit_mode, 0.1250, 0.0100)
            tool_label = "Custom Spot Drill"
        elif tool_type == "Center Drill":
            center_drill_size_mill, center_drill_preset_mill = render_center_drill_size_selector("mill")
            diameter = center_drill_preset_mill["pilot"]
            tool_label = f"Center Drill {center_drill_size_mill}"
        elif tool_type == "Drill":
            diameter = diameter_input("Drill Diameter", "mill_drill_dia", unit_mode, 0.5000, 0.0100)
            tool_label = "Custom Drill"
        elif tool_type == "Endmill":
            if tool_style_mill == '1/2 Ingersoll Rougher (Hi-Feed)':
                diameter = 0.5000
            else:
                diameter = diameter_input("Endmill Diameter", "mill_em_dia", unit_mode, 0.5000, 0.0100)
            tool_label = tool_style_mill
        else:
            diameter = diameter_input("Tap Diameter", "tap_diameter", unit_mode, 0.5000, 0.0100)
            tool_label = "Custom Tap Diameter"

    st.write(f"**Selected Tool:** {tool_label}")
    st.write(f"**Diameter Used:** {format_length(diameter, unit_mode)}")

    st.markdown("### Recommendation")

    if tool_type == "Spot Drill":
        rec = MILL_MATERIALS[material_mill]["Spot Drill"]
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        ipr = apply_cut_mode(rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = drill_feed_ipm(rpm, ipr)
        target_hole_diameter = diameter_input("Target Hole Diameter", "spot_target_dia", unit_mode, min(0.2500, diameter), 0.0010)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed Basis (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        if target_hole_diameter > diameter:
            c5.metric("Required Depth", "N/A")
            st.error("Target hole diameter cannot be larger than the spot drill diameter.")
        else:
            required_depth = calculate_spot_depth(target_hole_diameter, spot_angle)
            c5.metric("Required Depth", format_length(required_depth, unit_mode))
            st.caption("Required depth is tip depth to create a full usable spot equal to the target hole diameter.")

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Center Drill":
        rec = get_center_drill_data(material_mill)
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        ipr = apply_cut_mode(rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed Basis (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.write(f"**Center Drill Selected:** {center_drill_size_mill} ({center_drill_preset_mill['style']})")
        render_center_drill_depth_block("mill_center_drill", center_drill_size_mill, center_drill_preset_mill, unit_mode)

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Drill":
        drill_rec = DRILL_DATA[material_mill][drill_type_mill]
        sfm = apply_cut_mode(drill_rec["sfm"], "sfm")
        ipr = apply_cut_mode(drill_rec["ipr"], "ipr")
        rpm = rpm_from_sfm(sfm, diameter)
        ipm = drill_feed_ipm(rpm, ipr)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPR)", f"{ipr:.4f}")
        c4.metric("Feed (IPM)", f"{ipm:.2f}")

        st.write(f"**Notes:** {drill_rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Tap":
        rec = MILL_MATERIALS[material_mill]["Tap"]
        sfm = apply_cut_mode(rec["sfm"], "sfm")
        rpm = rpm_from_sfm(sfm, diameter)
        tpi = st.number_input("TPI (for inch taps)", min_value=1, value=13, step=1, key="mill_tap_tpi")
        tap_feed = tap_feed_ipm_from_tpi(rpm, tpi)

        c1, c2, c3 = st.columns(3)
        c1.metric("SFM", f"{sfm:.0f}")
        c2.metric("RPM", f"{rpm:.0f}")
        c3.metric("Feed (IPM)", f"{tap_feed:.2f}")

        st.write(f"**Notes:** {rec['notes']}")
        render_operator_notes(material_mill)

    elif tool_type == "Endmill":
        if tool_style_mill == '1/2 Ingersoll Rougher (Hi-Feed)':
            hif = get_hif_feed_data(material_mill)

            st.markdown("### Endmill Recommendation - HI-FEED INSERT MILL")
            c1, c2, c3 = st.columns(3)
            c1.metric("SFM Range", hif["sfm_range"])
            c2.metric("IPT Range", hif["ipt_range"])
            c3.metric("Axial DOC", hif["axial_doc"])

            d1, d2, d3 = st.columns(3)
            d1.metric("Chip Thickness", hif["chip_thickness"])
            d2.metric("Coolant", hif["coolant"])
            d3.metric("Tool", '1/2 Ingersoll Rougher')

            st.write(f"**Chart Note:** {hif['grade_note']}")
            st.write("**Application Note:** Use for keyways larger than .500 when using the hi-feed insert mill.")
            st.write("**Mode Note:** This chart is a roughing / hi-feed style recommendation.")
            render_operator_notes(material_mill)
        else:
            rec = MILL_MATERIALS[material_mill]["Endmill"]
            flute_count = st.number_input("Flute Count", min_value=1, value=4, step=1, key="mill_flutes")

            if em_operation == "rough":
                sfm = apply_cut_mode(rec["rough_sfm"], "sfm")
                ipt = apply_cut_mode(rec["rough_ipt"], "ipt")
                slot_doc = rec["rough_slot_doc_factor"] * diameter
                side_doc = rec["rough_side_doc_factor"] * diameter
                finish_note = rec["finish_radial"]
            else:
                sfm = apply_cut_mode(rec["finish_sfm"], "sfm")
                ipt = apply_cut_mode(rec["finish_ipt"], "ipt")
                slot_doc = rec["finish_slot_doc_factor"] * diameter
                side_doc = rec["finish_side_doc_factor"] * diameter
                finish_note = rec["finish_radial"]

            rpm = rpm_from_sfm(sfm, diameter)
            ipm = rpm * flute_count * ipt

            st.markdown(f"### Endmill Recommendation - {em_operation.upper()}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SFM", f"{sfm:.0f}")
            c2.metric("RPM", f"{rpm:.0f}")
            c3.metric("Chipload (IPT)", f"{ipt:.4f}")
            c4.metric("Feed (IPM)", f"{ipm:.2f}")

            st.markdown("### DOC Guidance")
            d1, d2, d3 = st.columns(3)
            d1.metric("Slot DOC", format_length(slot_doc, unit_mode))
            d2.metric("Side DOC", format_length(side_doc, unit_mode))
            d3.metric("Finish Radial", finish_note)

            st.write(f"**Notes:** {rec['notes']}")
            render_operator_notes(material_mill)
