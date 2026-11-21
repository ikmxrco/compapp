
import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="RCulator | Reynolds Number Calculator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "system": "SI",
    "simple_mode": True,
    "dark_mode": False,
    "fluid_mode": "Water",
    "diameter": None,
    "velocity": None,
    "temperature": None,
    "density": None,
    "viscosity": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# UNIT CONVERSIONS
# --------------------------------------------------

def change_units():
    old_system = st.session_state.get("previous_system", "SI")
    new_system = st.session_state.system

    if old_system == new_system:
        return

    # SI to English
    if old_system == "SI" and new_system == "English":
        if st.session_state.diameter is not None:
            st.session_state.diameter /= 0.3048

        if st.session_state.velocity is not None:
            st.session_state.velocity /= 0.3048

        if st.session_state.temperature is not None:
            st.session_state.temperature = (
                st.session_state.temperature * 9 / 5
            ) + 32

        if st.session_state.density is not None:
            st.session_state.density /= 16.018463

        if st.session_state.viscosity is not None:
            st.session_state.viscosity /= 47.88026

    # English to SI
    else:
        if st.session_state.diameter is not None:
            st.session_state.diameter *= 0.3048

        if st.session_state.velocity is not None:
            st.session_state.velocity *= 0.3048

        if st.session_state.temperature is not None:
            st.session_state.temperature = (
                st.session_state.temperature - 32
            ) * 5 / 9

        if st.session_state.density is not None:
            st.session_state.density *= 16.018463

        if st.session_state.viscosity is not None:
            st.session_state.viscosity *= 47.88026

    st.session_state.previous_system = new_system


if "previous_system" not in st.session_state:
    st.session_state.previous_system = st.session_state.system


# --------------------------------------------------
# WATER PROPERTY DATA
# Temperature in °C
# Density in kg/m³
# Dynamic viscosity in Pa·s
# --------------------------------------------------

water_data = [
    (0, 999.84, 0.001792),
    (5, 999.97, 0.001519),
    (10, 999.70, 0.001307),
    (15, 999.10, 0.001138),
    (20, 998.21, 0.001002),
    (25, 997.05, 0.000890),
    (30, 995.65, 0.000798),
    (35, 994.03, 0.000720),
    (40, 992.22, 0.000653),
    (45, 990.22, 0.000596),
    (50, 988.04, 0.000547),
    (55, 985.69, 0.000504),
    (60, 983.20, 0.000467),
    (65, 980.55, 0.000433),
    (70, 977.76, 0.000404),
    (75, 974.84, 0.000378),
    (80, 971.79, 0.000355),
    (85, 968.61, 0.000333),
    (90, 965.31, 0.000315),
    (95, 961.89, 0.000297),
    (100, 958.35, 0.000282),
]


def interpolate(temp, column):
    if temp < water_data[0][0] or temp > water_data[-1][0]:
        return None

    for i in range(len(water_data) - 1):
        t1 = water_data[i][0]
        t2 = water_data[i + 1][0]

        if t1 <= temp <= t2:
            v1 = water_data[i][column]
            v2 = water_data[i + 1][column]

            return v1 + (v2 - v1) * (temp - t1) / (t2 - t1)

    return None


# --------------------------------------------------
# THEME
# --------------------------------------------------

if st.session_state.dark_mode:
    bg = "#101827"
    panel = "#192538"
    text = "#F1F5F9"
    muted = "#A7B4C5"
    accent = "#38BDF8"
    border = "#30445E"
    input_bg = "#223249"
else:
    bg = "#F4F7FB"
    panel = "#FFFFFF"
    text = "#172B4D"
    muted = "#60728A"
    accent = "#087EBD"
    border = "#DCE5EF"
    input_bg = "#FFFFFF"


st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    [data-testid="stHeader"] {{
        background-color: {bg};
    }}

    [data-testid="stSidebar"] {{
        background-color: {panel};
    }}

    h1, h2, h3, h4, p, label, span, div {{
        color: inherit;
    }}

    .brand {{
        color: {accent};
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: -12px;
    }}

    .subtitle {{
        color: {muted};
        font-size: 0.95rem;
        margin-top: -12px;
    }}

    .section-label {{
        color: {muted};
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }}

    .result-card {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 22px;
        margin-top: 10px;
    }}

    .result-label {{
        color: {muted};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.2px;
    }}

    .result-number {{
        color: {accent};
        font-size: 2.4rem;
        font-weight: 800;
        margin: 4px 0;
        overflow-wrap: anywhere;
    }}

    .result-regime {{
        color: {text};
        font-size: 1.2rem;
        font-weight: 700;
    }}

    .info-card {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 14px;
    }}

    .small-muted {{
        color: {muted};
        font-size: 0.82rem;
    }}

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {{
        background-color: {input_bg};
        border-color: {border};
        border-radius: 10px;
    }}

    div[data-baseweb="input"] input {{
        color: {text};
    }}

    div[data-baseweb="select"] div {{
        color: {text};
    }}

    [data-testid="stMetric"] {{
        background-color: {panel};
        border: 1px solid {border};
        padding: 15px;
        border-radius: 12px;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {{
        color: {text};
    }}

    .stCaption {{
        color: {muted};
    }}

    div.stButton > button {{
        border-radius: 10px;
    }}

    hr {{
        border-color: {border};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

header1, header2, header3, header4 = st.columns(
    [2.5, 1, 1, 1]
)

with header1:
    logo_col, title_col = st.columns([1, 5])

    with logo_col:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=65)

    with title_col:
        st.markdown(
            '<div class="brand">ENGINEERING CALCULATOR</div>',
            unsafe_allow_html=True
        )
        st.title("RCulator")
        st.markdown(
            '<div class="subtitle">Reynolds Number Calculator</div>',
            unsafe_allow_html=True
        )

with header2:
    st.selectbox(
        "Units",
        ["SI", "English"],
        key="system",
        on_change=change_units
    )

with header3:
    st.toggle("Simple Mode", key="simple_mode")

with header4:
    st.toggle("Dark Mode", key="dark_mode")

st.divider()


# --------------------------------------------------
# UNIT LABELS
# --------------------------------------------------

if st.session_state.system == "SI":
    diameter_unit = "m"
    velocity_unit = "m/s"
    temperature_unit = "°C"
    density_unit = "kg/m³"
    viscosity_unit = "Pa·s"
else:
    diameter_unit = "ft"
    velocity_unit = "ft/s"
    temperature_unit = "°F"
    density_unit = "lb/ft³"
    viscosity_unit = "lb/(ft·s)"


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-label">CALCULATION INPUTS</div>',
    unsafe_allow_html=True
)

# Fluid selection
fluid_col, spacer_col = st.columns([1, 3])

with fluid_col:
    st.selectbox(
        "Fluid Properties",
        ["Water", "Custom Fluid"],
        key="fluid_mode"
    )


# --------------------------------------------------
# SIMPLE MODE INPUTS
# --------------------------------------------------

if st.session_state.simple_mode:

    c1, c2, c3 = st.columns(3)

    with c1:
        st.number_input(
            f"Pipe Diameter ({diameter_unit})",
            min_value=0.0,
            value=None,
            key="diameter",
            placeholder="Enter diameter",
            format="%.6f"
        )

    with c2:
        st.number_input(
            f"Flow Velocity ({velocity_unit})",
            min_value=0.0,
            value=None,
            key="velocity",
            placeholder="Enter velocity",
            format="%.6f"
        )

    with c3:
        if st.session_state.fluid_mode == "Water":
            st.number_input(
                f"Water Temperature ({temperature_unit})",
                value=None,
                key="temperature",
                placeholder="Enter temperature",
                format="%.2f"
            )
        else:
            st.number_input(
                f"Density ({density_unit})",
                min_value=0.0,
                value=None,
                key="density",
                placeholder="Enter density",
                format="%.6f"
            )

    if st.session_state.fluid_mode == "Custom Fluid":
        c4, c5 = st.columns(3)

        with c4:
            st.number_input(
                f"Dynamic Viscosity ({viscosity_unit})",
                min_value=0.0,
                value=None,
                key="viscosity",
                placeholder="Enter viscosity",
                format="%.8f"
            )


# --------------------------------------------------
# FULL MODE INPUTS
# --------------------------------------------------

else:

    c1, c2 = st.columns(2)

    with c1:
        st.number_input(
            f"Pipe Diameter ({diameter_unit})",
            min_value=0.0,
            value=None,
            key="diameter",
            placeholder="Enter pipe diameter",
            format="%.6f"
        )

    with c2:
        st.number_input(
            f"Flow Velocity ({velocity_unit})",
            min_value=0.0,
            value=None,
            key="velocity",
            placeholder="Enter flow velocity",
            format="%.6f"
        )

    if st.session_state.fluid_mode == "Water":

        st.number_input(
            f"Water Temperature ({temperature_unit})",
            value=None,
            key="temperature",
            placeholder="Enter water temperature",
            format="%.2f"
        )

    else:

        c3, c4 = st.columns(2)

        with c3:
            st.number_input(
                f"Density ({density_unit})",
                min_value=0.0,
                value=None,
                key="density",
                placeholder="Enter density",
                format="%.6f"
            )

        with c4:
            st.number_input(
                f"Dynamic Viscosity ({viscosity_unit})",
                min_value=0.0,
                value=None,
                key="viscosity",
                placeholder="Enter viscosity",
                format="%.8f"
            )


# --------------------------------------------------
# FLUID PROPERTY CALCULATION
# --------------------------------------------------

rho_si = None
mu_si = None

if st.session_state.fluid_mode == "Water":

    temp = st.session_state.temperature

    if temp is not None:

        if st.session_state.system == "SI":
            temp_c = temp
        else:
            temp_c = (temp - 32) * 5 / 9

        rho_si = interpolate(temp_c, 1)
        mu_si = interpolate(temp_c, 2)

        if rho_si is None or mu_si is None:
            st.warning(
                "Water temperature must be between 0°C and 100°C "
                "(32°F and 212°F)."
            )

else:

    density = st.session_state.density
    viscosity = st.session_state.viscosity

    if density is not None and viscosity is not None:

        if st.session_state.system == "SI":
            rho_si = density
            mu_si = viscosity
        else:
            rho_si = density * 16.018463
            mu_si = viscosity * 47.88026


# --------------------------------------------------
# WATER PROPERTY DISPLAY
# --------------------------------------------------

if st.session_state.fluid_mode == "Water":

    if rho_si is not None and mu_si is not None:

        if st.session_state.system == "SI":
            rho_display = rho_si
            mu_display = mu_si
        else:
            rho_display = rho_si / 16.018463
            mu_display = mu_si / 47.88026

        st.caption(
            f"Water density: {rho_display:.4f} {density_unit}  |  "
            f"Dynamic viscosity: {mu_display:.8f} {viscosity_unit}"
        )

    elif st.session_state.temperature is None:
        st.caption(
            "Enter the water temperature to determine its density "
            "and dynamic viscosity."
        )


# --------------------------------------------------
# REYNOLDS NUMBER CALCULATION
# --------------------------------------------------

diameter = st.session_state.diameter
velocity = st.session_state.velocity

# Convert diameter and velocity into SI units
if diameter is not None and velocity is not None:

    if st.session_state.system == "SI":
        diameter_m = diameter
        velocity_m_s = velocity
    else:
        diameter_m = diameter * 0.3048
        velocity_m_s = velocity * 0.3048

else:
    diameter_m = None
    velocity_m_s = None


valid = (
    diameter_m is not None
    and velocity_m_s is not None
    and rho_si is not None
    and mu_si is not None
    and diameter_m > 0
    and velocity_m_s > 0
    and rho_si > 0
    and mu_si > 0
)

st.divider()

st.markdown(
    '<div class="section-label">CALCULATION RESULT</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# RESULT DISPLAY
# --------------------------------------------------

if valid:

    reynolds = (
        rho_si * velocity_m_s * diameter_m
    ) / mu_si

    if reynolds < 2300:
        regime = "Laminar Flow"
        explanation = "The flow is generally smooth and orderly."
    elif reynolds <= 4000:
        regime = "Transitional Flow"
        explanation = "The flow is in the transition region."
    else:
        regime = "Turbulent Flow"
        explanation = "The flow is generally irregular and mixed."

    result_col, regime_col = st.columns([1.5, 1])

    with result_col:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">REYNOLDS NUMBER</div>
                <div class="result-number">{reynolds:,.2f}</div>
                <div class="small-muted">Dimensionless quantity</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with regime_col:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">FLOW REGIME</div>
                <div class="result-regime">{regime}</div>
                <div class="small-muted">{explanation}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Full mode details
    if not st.session_state.simple_mode:

        st.subheader("Calculation Details")

        st.latex(
            r"Re = \frac{\rho V D}{\mu}"
        )

        st.write("Substituting the SI values:")

        st.latex(
            rf"Re = \frac{{({rho_si:.4f})({velocity_m_s:.5f})"
            rf"({diameter_m:.5f})}}{{{mu_si:.8f}}}"
        )

        st.latex(rf"Re = {reynolds:,.2f}")

        st.subheader("Flow Regime Guide")

        g1, g2, g3 = st.columns(3)

        with g1:
            st.metric("Laminar", "Re < 2,300")

        with g2:
            st.metric("Transitional", "2,300–4,000")

        with g3:
            st.metric("Turbulent", "Re > 4,000")

else:

    st.markdown(
        """
        <div class="result-card">
            <div class="result-label">REYNOLDS NUMBER</div>
            <div class="result-number">—</div>
            <div class="small-muted">
                Enter the required values above to calculate.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="result-card">
            <div class="result-label">FLOW REGIME</div>
            <div class="result-regime">—</div>
            <div class="small-muted">
                The flow classification will appear here.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:10px 0;">
        <div class="small-muted">
            RCulator | Reynolds Number Calculator
        </div>
        <div class="small-muted">
            A Chemical Engineering Project
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
