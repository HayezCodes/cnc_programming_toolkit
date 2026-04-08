from fractions import Fraction
import re
import streamlit as st
from data.materials import TAP_SFM, OD_THREADING
from utils.formulas import rpm_from_sfm, tap_feed_ipm_from_tpi
from utils.ui_helpers import render_sidebar_nav, render_cutting_mode_sidebar

st.set_page_config(
    page_title="Threads",
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

render_sidebar_nav("Threads")

render_cutting_mode_sidebar()

st.title("Threads")
st.caption("Empower MFG - Built for Joshua")


def apply_cut_mode(value, kind="sfm"):
    return value


def parse_fractional_number(text: str) -> float:
    text = text.strip()

    if " " in text:
        whole, frac = text.split()
        return float(whole) + float(Fraction(frac))

    if "/" in text:
        return float(Fraction(text))

    return float(text)


def parse_thread_callout(callout: str):
    """
    Supports:
    - Imperial: 1/2-13, 7/8-14, 1 1/4-12, 3.34-12
    - Metric: M6x1, M8 x 1.25, M10x1.5, M12 X 1.75
    """
    raw = callout.strip().upper().replace("×", "X")

    metric_match = re.match(r"^M\s*([\d\.]+)\s*[X]\s*([\d\.]+)$", raw)
    if metric_match:
        nominal_mm = float(metric_match.group(1))
        pitch_mm = float(metric_match.group(2))
        nominal_in = nominal_mm / 25.4
        pitch_in = pitch_mm / 25.4
        tpi_equiv = 25.4 / pitch_mm

        return {
            "system": "metric",
            "display_nominal": nominal_mm,
            "display_pitch": pitch_mm,
            "display_unit": "mm",
            "nominal_dia_in": nominal_in,
            "pitch_in": pitch_in,
            "pitch_mm": pitch_mm,
            "tpi_equiv": tpi_equiv,
        }

    if "-" in raw:
        nominal_str, tpi_str = raw.split("-", 1)
        nominal_dia = parse_fractional_number(nominal_str.strip())
        tpi = float(tpi_str.strip())
        pitch_in = 1 / tpi
        pitch_mm = pitch_in * 25.4

        return {
            "system": "imperial",
            "display_nominal": nominal_dia,
            "display_pitch": tpi,
            "display_unit": "in",
            "nominal_dia_in": nominal_dia,
            "pitch_in": pitch_in,
            "pitch_mm": pitch_mm,
            "tpi_equiv": tpi,
        }

    raise ValueError("Invalid thread format")


def tap_feed_ipm_from_metric_pitch(rpm: float, pitch_mm: float) -> float:
    return rpm * (pitch_mm / 25.4)


st.markdown("### Quick Thread Input")

c1, c2, c3, c4 = st.columns(4)

with c1:
    callout = st.text_input("Thread Callout", value="1/2-13")
    st.caption("Examples: 1/2-13, 7/8-14, 1 1/4-12, M6x1, M10x1.5")

with c2:
    material = st.selectbox("Material", list(TAP_SFM.keys()))

with c3:
    thread_type = st.selectbox("Type", ["ID", "OD"])

with c4:
    thread_percent = st.selectbox("Percent Thread", [65, 70, 75, 80], index=2)

st.markdown("---")

try:
    thread_data = parse_thread_callout(callout)
except Exception:
    st.error("Format must be like: 1/2-13, 7/8-14, 1 1/4-12, M6x1, or M10x1.5")
    st.stop()

system = thread_data["system"]
nominal_dia_in = thread_data["nominal_dia_in"]
pitch_in = thread_data["pitch_in"]
pitch_mm = thread_data["pitch_mm"]
tpi_equiv = thread_data["tpi_equiv"]
percent_factor = thread_percent / 100.0

if thread_type == "ID":
    recommended_drill_in_basic = nominal_dia_in - pitch_in
    recommended_drill_in_percent = nominal_dia_in - (percent_factor * pitch_in)

    recommended_drill_mm_basic = recommended_drill_in_basic * 25.4
    recommended_drill_mm_percent = recommended_drill_in_percent * 25.4

    tap_sfm = apply_cut_mode(TAP_SFM[material], "sfm")
    tap_rpm = rpm_from_sfm(tap_sfm, nominal_dia_in)

    if system == "metric":
        tap_feed = tap_feed_ipm_from_metric_pitch(tap_rpm, pitch_mm)
    else:
        tap_feed = tap_feed_ipm_from_tpi(tap_rpm, tpi_equiv)

    if system == "metric":
        st.code(
f"""THREAD: {callout}
TYPE: ID
SYSTEM: METRIC
MATERIAL: {material}

NOMINAL DIAMETER: {thread_data["display_nominal"]:.4f} mm
PITCH: {pitch_mm:.4f} mm
TPI EQUIVALENT: {tpi_equiv:.4f}

RECOMMENDED DRILL:
BASIC (100% PITCH RULE): {recommended_drill_mm_basic:.4f} mm   ({recommended_drill_in_basic:.4f} in)
{thread_percent}% THREAD: {recommended_drill_mm_percent:.4f} mm   ({recommended_drill_in_percent:.4f} in)

TAP SFM: {tap_sfm:.0f}
TAP RPM: {tap_rpm:.0f}
TAP FEED: {tap_feed:.6f} IPM

NOTES:
- BASIC DRILL = NOMINAL - PITCH
- {thread_percent}% THREAD DRILL = NOMINAL - ({thread_percent}% x PITCH)
- VERIFY FINAL DRILL AGAINST PRINT / GAGE / SHOP STANDARD
""",
            language="text"
        )
    else:
        st.code(
f"""THREAD: {callout}
TYPE: ID
SYSTEM: IMPERIAL
MATERIAL: {material}

NOMINAL DIAMETER: {thread_data["display_nominal"]:.4f} in
TPI: {tpi_equiv:.4f}
PITCH: {pitch_in:.6f} in   ({pitch_mm:.4f} mm)

RECOMMENDED DRILL:
BASIC (100% PITCH RULE): {recommended_drill_in_basic:.4f} in   ({recommended_drill_mm_basic:.4f} mm)
{thread_percent}% THREAD: {recommended_drill_in_percent:.4f} in   ({recommended_drill_mm_percent:.4f} mm)

TAP SFM: {tap_sfm:.0f}
TAP RPM: {tap_rpm:.0f}
TAP FEED: {tap_feed:.6f} IPM

NOTES:
- BASIC DRILL = NOMINAL - PITCH
- {thread_percent}% THREAD DRILL = NOMINAL - ({thread_percent}% x PITCH)
- VERIFY FINAL DRILL AGAINST PRINT / GAGE / SHOP STANDARD
""",
            language="text"
        )

else:
    model_drop_in = 0.07 * pitch_in
    model_dia_in = nominal_dia_in - model_drop_in

    model_drop_mm = model_drop_in * 25.4
    model_dia_mm = model_dia_in * 25.4
    nominal_dia_mm = nominal_dia_in * 25.4

    od_sfm = apply_cut_mode(OD_THREADING[material]["sfm"], "sfm")
    od_rpm = rpm_from_sfm(od_sfm, nominal_dia_in)
    od_ipr = apply_cut_mode(pitch_in, "ipr")

    if system == "metric":
        st.code(
f"""THREAD: {callout}
TYPE: OD
SYSTEM: METRIC
MATERIAL: {material}

NOMINAL DIAMETER: {nominal_dia_mm:.4f} mm   ({nominal_dia_in:.4f} in)
PITCH: {pitch_mm:.4f} mm
TPI EQUIVALENT: {tpi_equiv:.4f}

MODEL DIAMETER: {model_dia_mm:.4f} mm   ({model_dia_in:.4f} in)
MODEL DROP: {model_drop_mm:.4f} mm   ({model_drop_in:.4f} in)

THREAD SFM: {od_sfm:.0f}
THREAD LEAD / FEED: {od_ipr:.6f} IPR
APPROX RPM: {od_rpm:.0f}

NOTES:
- MODEL DIA USES CURRENT SHOP APPROXIMATION
- THREAD FEED = PITCH IN INCHES PER REV
- VERIFY AGAINST PRINT / GAGE WHEN NEEDED
""",
            language="text"
        )
    else:
        st.code(
f"""THREAD: {callout}
TYPE: OD
SYSTEM: IMPERIAL
MATERIAL: {material}

NOMINAL DIAMETER: {nominal_dia_in:.4f} in   ({nominal_dia_mm:.4f} mm)
TPI: {tpi_equiv:.4f}
PITCH: {pitch_in:.6f} in   ({pitch_mm:.4f} mm)

MODEL DIAMETER: {model_dia_in:.4f} in   ({model_dia_mm:.4f} mm)
MODEL DROP: {model_drop_in:.4f} in   ({model_drop_mm:.4f} mm)

THREAD SFM: {od_sfm:.0f}
THREAD LEAD / FEED: {od_ipr:.6f} IPR
APPROX RPM: {od_rpm:.0f}

NOTES:
- MODEL DIA USES CURRENT SHOP APPROXIMATION
- THREAD FEED = 1 / TPI
- VERIFY AGAINST PRINT / GAGE WHEN NEEDED
""",
            language="text"
        )