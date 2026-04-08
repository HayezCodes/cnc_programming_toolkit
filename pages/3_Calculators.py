import math
import streamlit as st
from utils.ui_helpers import render_sidebar_nav

st.set_page_config(
    page_title="Calculators",
    layout="wide",
    initial_sidebar_state="expanded"
)

CENTER_DRILL_PRESETS = {
    "Custom": None,

    "Std 00": {"style": "Standard", "pilot": 0.025000, "body": 0.1250, "C": 0.025000},
    "Std 0": {"style": "Standard", "pilot": 0.031250, "body": 0.1250, "C": 0.031250},
    "Std 1": {"style": "Standard", "pilot": 0.046875, "body": 0.1250, "C": 0.046875},
    "Std 2": {"style": "Standard", "pilot": 0.078125, "body": 0.1875, "C": 0.078125},
    "Std 3": {"style": "Standard", "pilot": 0.109375, "body": 0.2500, "C": 0.109375},
    "Std 4": {"style": "Standard", "pilot": 0.125000, "body": 0.3125, "C": 0.125000},
    "Std 5": {"style": "Standard", "pilot": 0.187500, "body": 0.4375, "C": 0.187500},
    "Std 6": {"style": "Standard", "pilot": 0.218750, "body": 0.5000, "C": 0.218750},
    "Std 7": {"style": "Standard", "pilot": 0.250000, "body": 0.6250, "C": 0.250000},
    "Std 8": {"style": "Standard", "pilot": 0.312500, "body": 0.7500, "C": 0.312500},

    "Bell 11": {"style": "Bell", "pilot": 0.046875, "body": 0.1250, "C": 0.046875},
    "Bell 12": {"style": "Bell", "pilot": 0.062500, "body": 0.1875, "C": 0.062500},
    "Bell 13": {"style": "Bell", "pilot": 0.093750, "body": 0.2500, "C": 0.093750},
    "Bell 14": {"style": "Bell", "pilot": 0.109375, "body": 0.3125, "C": 0.109375},
    "Bell 15": {"style": "Bell", "pilot": 0.156250, "body": 0.4375, "C": 0.156250},
    "Bell 16": {"style": "Bell", "pilot": 0.187500, "body": 0.5000, "C": 0.187500},
    "Bell 17": {"style": "Bell", "pilot": 0.218750, "body": 0.6250, "C": 0.218750},
    "Bell 18": {"style": "Bell", "pilot": 0.250000, "body": 0.7500, "C": 0.250000},
}

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 1.2rem;
}

header[data-testid="stHeader"] {
    height: 0.8rem;
}

.calc-title-wrap {
    margin-top: 0.2rem;
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

render_sidebar_nav("Calculators")

col1, col2 = st.columns([1, 6])
with col1:
    if st.button("🏠"):
        st.switch_page("app.py")

with col2:
    st.markdown('<div class="calc-title-wrap">', unsafe_allow_html=True)
    st.title("Calculators")
    st.caption("Empower MFG - Built for Joshua")
    st.markdown("</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Triangle", "Keyway", "Center Drill", "Chamfer", "Drill Breakthrough", "IN ↔ MM"]
)

with tab1:
    st.subheader("Triangle Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use the diagram below so you can fill values in by location.
Right angle is at the bottom left.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<svg width="420" height="220" xmlns="http://www.w3.org/2000/svg">
  <line x1="60" y1="180" x2="60" y2="40" stroke="white" stroke-width="3"/>
  <line x1="60" y1="180" x2="320" y2="180" stroke="white" stroke-width="3"/>
  <line x1="60" y1="40" x2="320" y2="180" stroke="white" stroke-width="3"/>
  <rect x="60" y="165" width="15" height="15" fill="none" stroke="white" stroke-width="2"/>
  <text x="8" y="115" fill="white" font-size="16">Vertical</text>
  <text x="160" y="205" fill="white" font-size="16">Base</text>
  <text x="180" y="95" fill="white" font-size="16">Hypotenuse</text>
  <text x="326" y="175" fill="white" font-size="16">Angle</text>
</svg>
""",
        unsafe_allow_html=True,
    )

    tri_mode = st.selectbox(
        "Solve Using",
        [
            "Vertical + Base",
            "Vertical + Hypotenuse",
            "Base + Hypotenuse",
            "Base + Angle",
            "Vertical + Angle",
            "Hypotenuse + Angle",
        ],
        key="triangle_mode"
    )

    formula_map = {
        "Vertical + Base": "Hyp = √(V² + B²) | Angle = atan(V/B)",
        "Vertical + Hypotenuse": "Base = √(H² - V²) | Angle = asin(V/H)",
        "Base + Hypotenuse": "Vertical = √(H² - B²) | Angle = acos(B/H)",
        "Base + Angle": "V = tan(A)*B | H = B / cos(A)",
        "Vertical + Angle": "B = V / tan(A) | H = V / sin(A)",
        "Hypotenuse + Angle": "B = H*cos(A) | V = H*sin(A)",
    }

    st.markdown(
        f"""
<div style="font-size:0.78rem; opacity:0.75; margin-top:-6px;">
{formula_map[tri_mode]}
</div>
""",
        unsafe_allow_html=True,
    )

    if tri_mode == "Vertical + Base":
        col1, col2 = st.columns(2)
        with col1:
            vertical = st.number_input("Vertical", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_vert_1")
        with col2:
            base = st.number_input("Base", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_base_1")

        hyp = math.sqrt(vertical**2 + base**2)
        angle = math.degrees(math.atan(vertical / base))

    elif tri_mode == "Vertical + Hypotenuse":
        col1, col2 = st.columns(2)
        with col1:
            vertical = st.number_input("Vertical ", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_vert_2")
        with col2:
            hyp = st.number_input("Hypotenuse", min_value=0.0001, value=2.0000, step=0.1, format="%.4f", key="tri_hyp_2")

        if hyp <= vertical:
            st.error("Hypotenuse must be greater than vertical side.")
            st.stop()

        base = math.sqrt(hyp**2 - vertical**2)
        angle = math.degrees(math.asin(vertical / hyp))

    elif tri_mode == "Base + Hypotenuse":
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Base ", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_base_3")
        with col2:
            hyp = st.number_input("Hypotenuse ", min_value=0.0001, value=2.0000, step=0.1, format="%.4f", key="tri_hyp_3")

        if hyp <= base:
            st.error("Hypotenuse must be greater than base side.")
            st.stop()

        vertical = math.sqrt(hyp**2 - base**2)
        angle = math.degrees(math.acos(base / hyp))

    elif tri_mode == "Base + Angle":
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Base Side", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_base_4")
        with col2:
            angle = st.number_input("Angle (deg)", min_value=0.0001, max_value=89.9999, value=30.0, step=1.0, format="%.4f", key="tri_angle_4")

        vertical = math.tan(math.radians(angle)) * base
        hyp = base / math.cos(math.radians(angle))

    elif tri_mode == "Vertical + Angle":
        col1, col2 = st.columns(2)
        with col1:
            vertical = st.number_input("Vertical Side  ", min_value=0.0001, value=1.0000, step=0.1, format="%.4f", key="tri_vert_5")
        with col2:
            angle = st.number_input("Angle (deg) ", min_value=0.0001, max_value=89.9999, value=30.0, step=1.0, format="%.4f", key="tri_angle_5")

        base = vertical / math.tan(math.radians(angle))
        hyp = vertical / math.sin(math.radians(angle))

    else:
        col1, col2 = st.columns(2)
        with col1:
            hyp = st.number_input("Hypotenuse  ", min_value=0.0001, value=2.0000, step=0.1, format="%.4f", key="tri_hyp_6")
        with col2:
            angle = st.number_input("Angle (deg)  ", min_value=0.0001, max_value=89.9999, value=30.0, step=1.0, format="%.4f", key="tri_angle_6")

        base = hyp * math.cos(math.radians(angle))
        vertical = hyp * math.sin(math.radians(angle))

    other_angle = 90 - angle

    c1, c2, c3 = st.columns(3)
    c1.metric("Vertical", f"{vertical:.4f}")
    c2.metric("Base", f"{base:.4f}")
    c3.metric("Hypotenuse", f"{hyp:.4f}")

    c4, c5 = st.columns(2)
    c4.metric("Angle", f"{angle:.4f}")
    c5.metric("Other Angle", f"{other_angle:.4f}")

with tab2:
    st.subheader("Keyway Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Built around the print styles you actually use. Main output is the X value (dia) for programming.
</div>
""",
        unsafe_allow_html=True,
    )

    key_mode = st.selectbox(
        "Callout Style",
        [
            "Bottom of Keyway to Bottom of Shaft",
            "Depth from OD",
            "Width Chord + Depth Below Chord"
        ],
        key="key_mode_v8"
    )

    if key_mode == "Bottom of Keyway to Bottom of Shaft":
        st.markdown(
            """
<svg width="640" height="330" xmlns="http://www.w3.org/2000/svg">
  <circle cx="290" cy="175" r="110" stroke="white" stroke-width="4" fill="none"/>
  <line x1="245" y1="84" x2="245" y2="112" stroke="white" stroke-width="4"/>
  <line x1="335" y1="84" x2="335" y2="112" stroke="white" stroke-width="4"/>
  <line x1="245" y1="112" x2="335" y2="112" stroke="white" stroke-width="4"/>

  <line x1="130" y1="285" x2="290" y2="285" stroke="#999999" stroke-width="4"/>
  <line x1="130" y1="112" x2="245" y2="112" stroke="#999999" stroke-width="4"/>
  <line x1="110" y1="112" x2="110" y2="285" stroke="#999999" stroke-width="4"/>
  <polygon points="110,112 100,126 120,126" fill="#999999"/>
  <polygon points="110,285 100,271 120,271" fill="#999999"/>

  <line x1="480" y1="255" x2="405" y2="215" stroke="#999999" stroke-width="4"/>
  <line x1="480" y1="255" x2="535" y2="255" stroke="#999999" stroke-width="4"/>

  <line x1="290" y1="50" x2="290" y2="300" stroke="#cccccc" stroke-width="2"/>
  <line x1="175" y1="175" x2="405" y2="175" stroke="#cccccc" stroke-width="2"/>
</svg>
""",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            shaft_dia = st.number_input("Shaft Diameter", min_value=0.0001, value=1.2500, step=0.1250, format="%.4f", key="kw_bot_dia")
        with col2:
            bottom_to_bottom = st.number_input("Bottom of Keyway to Bottom of Shaft", min_value=0.0001, value=1.1250, step=0.0100, format="%.4f", key="kw_bot_val")

        radius = shaft_dia / 2
        depth_from_od = shaft_dia - bottom_to_bottom
        centerline_to_floor = bottom_to_bottom - radius
        x_value_dia = 2 * centerline_to_floor

        st.markdown("### Results")
        r1, r2 = st.columns(2)
        r1.metric("Depth from OD", f"{depth_from_od:.4f}")
        r2.metric("X Value (Dia)", f"{x_value_dia:.4f}")

    elif key_mode == "Depth from OD":
        st.markdown(
            """
<svg width="640" height="330" xmlns="http://www.w3.org/2000/svg">
  <circle cx="290" cy="175" r="110" stroke="white" stroke-width="4" fill="none"/>
  <line x1="245" y1="84" x2="245" y2="112" stroke="white" stroke-width="4"/>
  <line x1="335" y1="84" x2="335" y2="112" stroke="white" stroke-width="4"/>
  <line x1="245" y1="112" x2="335" y2="112" stroke="white" stroke-width="4"/>

  <line x1="405" y1="75" x2="515" y2="75" stroke="#999999" stroke-width="4"/>
  <line x1="405" y1="112" x2="515" y2="112" stroke="#999999" stroke-width="4"/>
  <line x1="495" y1="75" x2="495" y2="112" stroke="#999999" stroke-width="4"/>
  <polygon points="495,75 484,88 506,88" fill="#999999"/>
  <polygon points="495,112 484,99 506,99" fill="#999999"/>

  <line x1="480" y1="255" x2="405" y2="215" stroke="#999999" stroke-width="4"/>
  <line x1="480" y1="255" x2="535" y2="255" stroke="#999999" stroke-width="4"/>

  <line x1="290" y1="50" x2="290" y2="300" stroke="#cccccc" stroke-width="2"/>
  <line x1="175" y1="175" x2="405" y2="175" stroke="#cccccc" stroke-width="2"/>
</svg>
""",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            shaft_dia = st.number_input("Shaft Diameter ", min_value=0.0001, value=1.2500, step=0.1250, format="%.4f", key="kw_top_dia")
        with col2:
            depth_from_od = st.number_input("Depth from OD", min_value=0.0001, value=0.1250, step=0.0100, format="%.4f", key="kw_top_depth")

        radius = shaft_dia / 2
        centerline_to_floor = radius - depth_from_od
        bottom_to_bottom = shaft_dia - depth_from_od
        x_value_dia = 2 * centerline_to_floor

        st.markdown("### Results")
        r1, r2 = st.columns(2)
        r1.metric("X Value (Dia)", f"{x_value_dia:.4f}")
        r2.metric("Bottom of Keyway to Bottom of Shaft", f"{bottom_to_bottom:.4f}")

    else:
        st.markdown(
            """
<svg width="700" height="360" xmlns="http://www.w3.org/2000/svg">
  <circle cx="320" cy="190" r="115" stroke="white" stroke-width="4" fill="none"/>

  <line x1="225" y1="120" x2="415" y2="120" stroke="white" stroke-width="4"/>

  <line x1="225" y1="103" x2="225" y2="137" stroke="#999999" stroke-width="4"/>
  <line x1="415" y1="103" x2="415" y2="137" stroke="#999999" stroke-width="4"/>
  <line x1="225" y1="103" x2="415" y2="103" stroke="#999999" stroke-width="4"/>
  <polygon points="225,103 240,95 240,111" fill="#999999"/>
  <polygon points="415,103 400,95 400,111" fill="#999999"/>

  <line x1="450" y1="120" x2="565" y2="120" stroke="#999999" stroke-width="4"/>
  <line x1="450" y1="160" x2="565" y2="160" stroke="#999999" stroke-width="4"/>
  <line x1="545" y1="120" x2="545" y2="160" stroke="#999999" stroke-width="4"/>
  <polygon points="545,120 535,133 555,133" fill="#999999"/>
  <polygon points="545,160 535,147 555,147" fill="#999999"/>

  <line x1="530" y1="280" x2="450" y2="235" stroke="#999999" stroke-width="4"/>
  <line x1="530" y1="280" x2="590" y2="280" stroke="#999999" stroke-width="4"/>

  <line x1="320" y1="55" x2="320" y2="325" stroke="#cccccc" stroke-width="2"/>
  <line x1="200" y1="190" x2="440" y2="190" stroke="#cccccc" stroke-width="2"/>
</svg>
""",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            depth_below_chord = st.number_input("Depth Below Chord", min_value=0.0000, value=0.0000, step=0.0100, format="%.4f", key="kw_chord_depth")
        with col2:
            keyway_width = st.number_input("Keyway Width (Chord)", min_value=0.0001, value=0.3750, step=0.0625, format="%.4f", key="kw_chord_width")
        with col3:
            shaft_dia = st.number_input("Shaft Diameter  ", min_value=0.0001, value=0.8750, step=0.1250, format="%.4f", key="kw_chord_dia")

        radius = shaft_dia / 2
        if keyway_width >= shaft_dia:
            st.error("Keyway width must be smaller than shaft diameter.")
            st.stop()

        chord_x_dia = 2 * math.sqrt(max(0.0, radius**2 - (keyway_width / 2) ** 2))
        final_x_dia = chord_x_dia - (2 * depth_below_chord)
        centerline_to_floor = final_x_dia / 2
        depth_from_od = radius - centerline_to_floor
        bottom_to_bottom = radius + centerline_to_floor

        st.markdown("### Results")
        r1, r2, r3 = st.columns(3)
        r1.metric("Depth from OD", f"{depth_from_od:.4f}")
        r2.metric("Final X Value (Dia)", f"{final_x_dia:.4f}")
        r3.metric("Bottom of Keyway to Bottom of Shaft", f"{bottom_to_bottom:.4f}")

    st.markdown("### Notes")
    st.write("X Value (Dia) is the diameter value from spindle centerline to the keyway floor for programming use.")
    st.write("Width Chord + Depth Below Chord matches the workflow where you model the width as a chord, then step deeper from that line.")

with tab3:
    st.subheader("Center Drill Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use bell / body diameter like the shop talks about it. Calculator gives pilot hole depth only, or works backwards from pilot hole depth.
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        preset = st.selectbox("Center Drill Size", list(CENTER_DRILL_PRESETS.keys()), key="cd_preset")
        angle = st.number_input("Included Angle (deg)", min_value=1.0, max_value=179.0, value=60.0, step=1.0, format="%.1f", key="cd_angle")

        if CENTER_DRILL_PRESETS[preset] is not None:
            preset_data = CENTER_DRILL_PRESETS[preset]
            pilot_dia = preset_data["pilot"]
            body_dia = preset_data["body"]
            drill_len = preset_data["C"]

            st.metric("Style", preset_data["style"])
            st.metric("Pilot Dia", f"{pilot_dia:.4f}")
            st.metric("Body / Bell Dia", f"{body_dia:.4f}")
            st.metric("Drill Length (C)", f"{drill_len:.4f}")
        else:
            pilot_dia = st.number_input("Pilot Diameter", min_value=0.0001, value=0.1250, step=0.0010, format="%.4f", key="cd_pilot")
            body_dia = st.number_input("Body / Bell Diameter", min_value=0.0001, value=0.2500, step=0.0010, format="%.4f", key="cd_body")
            drill_len = st.number_input("Drill Length (C)", min_value=0.0001, value=0.1250, step=0.0010, format="%.4f", key="cd_drill_len")

    with col2:
        mode = st.selectbox("Solve For", ["Pilot Hole Depth", "Bell / Body Diameter"], key="cd_mode")

        if mode == "Pilot Hole Depth":
            bell_dia = st.number_input("Bell / Body Diameter Target", min_value=0.0001, value=0.1500, step=0.0010, format="%.4f", key="cd_bell_target")
        else:
            pilot_hole_depth_input = st.number_input("Pilot Hole Depth Target", min_value=0.0001, value=0.1000, step=0.0010, format="%.4f", key="cd_pilot_depth_target")

    st.markdown("---")

    half_angle = math.radians(angle / 2)

    if mode == "Pilot Hole Depth":
        if bell_dia <= pilot_dia:
            st.error("Bell / body diameter must be larger than pilot diameter.")
        else:
            chamfer_depth = (bell_dia - pilot_dia) / (2 * math.tan(half_angle))
            pilot_hole_depth = chamfer_depth + drill_len

            st.markdown("### Result")
            st.metric("Pilot Hole Depth", f"{pilot_hole_depth:.4f}")

            st.markdown("### Notes")
            st.write(f"Pilot diameter is {pilot_dia:.4f}.")
            st.write(f"Body / bell diameter of tool is {body_dia:.4f}.")
            st.write(f"Drill length (C) is {drill_len:.4f}.")

            if bell_dia > body_dia:
                st.warning("Bell / body diameter target exceeds tool body diameter.")

    else:
        if pilot_hole_depth_input <= drill_len:
            st.error("Pilot hole depth must be greater than drill length (C).")
        else:
            chamfer_depth = pilot_hole_depth_input - drill_len
            bell_dia_calc = (2 * chamfer_depth * math.tan(half_angle)) + pilot_dia

            st.markdown("### Result")
            st.metric("Bell / Body Diameter", f"{bell_dia_calc:.4f}")

            st.markdown("### Notes")
            st.write(f"Pilot diameter is {pilot_dia:.4f}.")
            st.write(f"Body / bell diameter of tool is {body_dia:.4f}.")
            st.write(f"Drill length (C) is {drill_len:.4f}.")

            if bell_dia_calc > body_dia:
                st.warning("Calculated bell / body diameter exceeds tool body diameter.")

with tab4:
    st.subheader("Chamfer Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use this for quick chamfer math on diameters. BELL DIAMETER is the finished major diameter across the chamfer.
</div>
""",
        unsafe_allow_html=True,
    )

    chamfer_mode = st.selectbox("Mode", ["Width -> Depth", "Depth -> Width"], key="chamfer_mode")

    col1, col2, col3 = st.columns(3)
    with col1:
        base_diameter = st.number_input("Diameter", min_value=0.0001, value=1.0000, step=0.0100, format="%.4f", key="chamfer_diameter")
    with col2:
        included_angle = st.number_input("Included Angle (deg)", min_value=1.0, max_value=179.0, value=90.0, step=1.0, format="%.1f", key="chamfer_angle")
    with col3:
        if chamfer_mode == "Width -> Depth":
            chamfer_width = st.number_input("Chamfer Width", min_value=0.0001, value=0.0300, step=0.0010, format="%.4f", key="chamfer_width")
        else:
            chamfer_depth = st.number_input("Chamfer Depth", min_value=0.0001, value=0.0300, step=0.0010, format="%.4f", key="chamfer_depth")

    st.markdown("---")

    half_angle = math.radians(included_angle / 2)

    if chamfer_mode == "Width -> Depth":
        chamfer_depth = chamfer_width / math.tan(half_angle)
    else:
        chamfer_width = chamfer_depth * math.tan(half_angle)

    bell_diameter = base_diameter + (2 * chamfer_width)

    st.markdown("### Results")
    r1, r2, r3 = st.columns(3)
    r1.metric("Chamfer Width", f"{chamfer_width:.4f}")
    r2.metric("Chamfer Depth", f"{chamfer_depth:.4f}")
    r3.metric("BELL DIAMETER", f"{bell_diameter:.4f}")

with tab5:
    st.subheader("Drill Breakthrough Calculator")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Use this to figure the extra drill travel needed after the point first reaches the far side.
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        drill_diameter = st.number_input("Drill Diameter", min_value=0.0001, value=0.2500, step=0.0010, format="%.4f", key="breakthrough_dia")
    with col2:
        point_angle = st.number_input("Point Angle (deg)", min_value=1.0, max_value=179.0, value=118.0, step=1.0, format="%.1f", key="breakthrough_angle")
    with col3:
        breakthrough_past_center = st.number_input("Breakthrough Past Center", min_value=0.0000, value=0.0200, step=0.0010, format="%.4f", key="breakthrough_past_center")

    point_height_to_center = (drill_diameter / 2) / math.tan(math.radians(point_angle / 2))
    additional_depth_required = point_height_to_center + breakthrough_past_center
    total_drill_depth = additional_depth_required

    st.markdown("### Results")
    r1, r2 = st.columns(2)
    r1.metric("Additional Depth Required", f"{additional_depth_required:.4f}")
    r2.metric("Total Drill Depth", f"{total_drill_depth:.4f}")

    st.write("Total drill depth is referenced from the moment the drill point first contacts the back side of the part.")

with tab6:
    st.subheader("IN ↔ MM Converter")

    st.markdown(
        """
<div style="font-size:0.92rem; line-height:1.35;">
Convert either direction. Enter a value in the side you want to use.
</div>
""",
        unsafe_allow_html=True,
    )

    convert_mode = st.radio("Conversion Direction", ["IN to MM", "MM to IN"], horizontal=True, key="unit_convert_mode")

    if convert_mode == "IN to MM":
        inches = st.number_input("Inches", min_value=0.0000, value=1.0000, step=0.0010, format="%.4f", key="inch_input")
        mm = inches * 25.4

        c1, c2 = st.columns(2)
        c1.metric("Inches", f"{inches:.4f}")
        c2.metric("Millimeters", f"{mm:.4f}")

    else:
        mm = st.number_input("Millimeters", min_value=0.0000, value=25.4000, step=0.0100, format="%.4f", key="mm_input")
        inches = mm / 25.4

        c1, c2 = st.columns(2)
        c1.metric("Millimeters", f"{mm:.4f}")
        c2.metric("Inches", f"{inches:.4f}")

    st.markdown("### Quick Reference")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("1/16 in", f"{0.0625 * 25.4:.4f} mm")
    q2.metric("1/8 in", f"{0.1250 * 25.4:.4f} mm")
    q3.metric("1/4 in", f"{0.2500 * 25.4:.4f} mm")
    q4.metric("1 in", f"{1.0000 * 25.4:.4f} mm")
