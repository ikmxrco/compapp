
import math
import streamlit as st
from pathlib import Path

# ==========================================================
# RCULATOR | REYNOLDS NUMBER CALCULATOR
# Chemical Engineering Computational Tool
# ==========================================================

st.set_page_config(
    page_title="RCulator | Reynolds Number Calculator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"

# ==========================================================
# FLUID DATABASE
# Density: DIPPR 105, except water (polynomial)
# Viscosity: DIPPR 101
# Temperature: Kelvin
# ==========================================================

FLUIDS = {
    "Acetic acid": {
        "formula": "C2H4O2", "MW": 60.052,
        "d": (1.4486, 0.25892, 591.95, 0.2529, 0),
        "v": (-9.03, 1212.3, -0.322, 0, 0)
    },
    "Acetone": {
        "formula": "C3H6O", "MW": 58.07914,
        "d": (1.2332, 0.25886, 508.2, 0.2913, 0),
        "v": (-14.918, 1023.4, 0.5961, 0, 0)
    },
    "Benzene": {
        "formula": "C6H6", "MW": 78.11184,
        "d": (1.0259, 0.26666, 562.05, 0.28394, 0),
        "v": (7.5117, 294.68, -2.794, 0, 0)
    },
    "Butane": {
        "formula": "C4H10", "MW": 58.1222,
        "d": (1.0677, 0.27188, 425.12, 0.28688, 0),
        "v": (-7.2471, 534.82, -0.57469, -4.66e-27, 10)
    },
    "Carbon tetrachloride": {
        "formula": "CCl4", "MW": 153.8227,
        "d": (0.99835, 0.274, 556.35, 0.287, 0),
        "v": (-8.0738, 1121.1, -0.4726, 0, 0)
    },
    "Chlorobenzene": {
        "formula": "C6H5Cl", "MW": 112.5569,
        "d": (0.8711, 0.26805, 632.35, 0.2799, 0),
        "v": (0.15772, 540.5, -1.6075, 0, 0)
    },
    "Chloroform": {
        "formula": "CHCl3", "MW": 119.37764,
        "d": (1.0841, 0.2581, 536.4, 0.2741, 0),
        "v": (-14.109, 1049.2, 0.5377, 0, 0)
    },
    "Cyclohexane": {
        "formula": "C6H12", "MW": 84.15948,
        "d": (0.88998, 0.27376, 553.8, 0.28571, 0),
        "v": (-33.763, 2497.2, 3.2236, 0, 0)
    },
    "Diethyl ether": {
        "formula": "C4H10O", "MW": 74.1216,
        "d": (0.9554, 0.26847, 466.7, 0.2814, 0),
        "v": (10.197, -63.8, -3.226, 0, 0)
    },
    "Ethanol": {
        "formula": "C2H6O", "MW": 46.06844,
        "d": (1.6288, 0.27469, 514, 0.23178, 0),
        "v": (7.875, 781.98, -3.0418, 0, 0)
    },
    "Ethyl acetate": {
        "formula": "C4H8O2", "MW": 88.10512,
        "d": (0.8996, 0.25856, 523.3, 0.278, 0),
        "v": (14.354, -154.6, -3.7887, 0, 0)
    },
    "Ethylene glycol": {
        "formula": "C2H6O2", "MW": 62.06784,
        "d": (1.315, 0.25125, 720, 0.21868, 0),
        "v": (-290.36, 14251, 42.486, -0.000040369, 2)
    },
    "Heptane": {
        "formula": "C7H16", "MW": 100.20194,
        "d": (0.61259, 0.26211, 540.2, 0.28141, 0),
        "v": (-98.159, 3592.6, 14.197, -0.000029555, 2)
    },
    "Hexane": {
        "formula": "C6H14", "MW": 86.17536,
        "d": (0.70824, 0.26411, 507.6, 0.27537, 0),
        "v": (-56.569, 2140.5, 7.5175, -0.000017676, 2)
    },
    "Methanol": {
        "formula": "CH4O", "MW": 32.04186,
        "d": (2.3267, 0.27073, 512.5, 0.24713, 0),
        "v": (-25.317, 1789.2, 2.069, 0, 0)
    },
    "Octane": {
        "formula": "C8H18", "MW": 114.22852,
        "d": (0.5266, 0.25693, 568.7, 0.28571, 0),
        "v": (-98.805, 3905.5, 14.103, -0.000025112, 2)
    },
    "1-Propanol": {
        "formula": "C3H8O", "MW": 60.09502,
        "d": (1.2457, 0.27281, 536.8, 0.23994, 0),
        "v": (23.467, 116.07, -5.3372, 2880100000, -4.0267)
    },
    "2-Propanol": {
        "formula": "C3H8O", "MW": 60.095,
        "d": (1.1799, 0.2644, 508.3, 0.24653, 0),
        "v": (-8.8918, 2357.6, -0.91376, 0, 0)
    },
    "Toluene": {
        "formula": "C7H8", "MW": 92.13842,
        "d": (0.8792, 0.27136, 591.75, 0.29241, 0),
        "v": (-226.08, 6805.7, 37.542, -0.060853, 1)
    },
    "Water": {
        "formula": "H2O", "MW": 18.01528,
        "d": (-13.851, 0.64038, -0.0019124, 0.0000018211, 0),
        "v": (-52.843, 3703.6, 5.866, -5.88e-29, 10)
    }
}

# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "system": "SI",
    "previous_system": "SI",
    "simple_mode": True,
    "dark_mode": False,
    "fluid": "Water",
    "diameter": None,
    "velocity": None,
    "temperature": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# UNIT CONVERSION
# ==========================================================

def change_units():
    old = st.session_state.previous_system
    new = st.session_state.system

    if old == new:
        return

    if old == "SI" and new == "English":

        if st.session_state.diameter is not None:
            st.session_state.diameter /= 0.3048

        if st.session_state.velocity is not None:
            st.session_state.velocity /= 0.3048

        if st.session_state.temperature is not None:
            st.session_state.temperature = (
                st.session_state.temperature * 9 / 5
            ) + 32

    elif old == "English" and new == "SI":

        if st.session_state.diameter is not None:
            st.session_state.diameter *= 0.3048

        if st.session_state.velocity is not None:
            st.session_state.velocity *= 0.3048

        if st.session_state.temperature is not None:
            st.session_state.temperature = (
                st.session_state.temperature - 32
            ) * 5 / 9

    st.session_state.previous_system = new


def reset_inputs():
    st.session_state.diameter = None
    st.session_state.velocity = None
    st.session_state.temperature = None


# ==========================================================
# CORRELATIONS
# ==========================================================

def calculate_molar_density(fluid, temperature_k):
    """
    Returns molar density in mol/dm3.

    Non-water:
    DIPPR Equation 105:
    rho_m = C1 / C2^(1+(1-T/C3)^C4) + C5

    Water:
    Polynomial:
    C1 + C2*T + C3*T^2 + C4*T^3 + C5*T^4
    """

    c1, c2, c3, c4, c5 = FLUIDS[fluid]["d"]

    if fluid == "Water":
        result = (
            c1
            + c2 * temperature_k
            + c3 * temperature_k**2
            + c4 * temperature_k**3
            + c5 * temperature_k**4
        )
    else:
        if c3 == 0 or c2 <= 0:
            raise ValueError("Invalid density coefficients.")

        base = 1 - temperature_k / c3

        if base < 0 and not float(c4).is_integer():
            raise ValueError(
                "Temperature is outside the density correlation range."
            )

        result = c1 / (
            c2 ** (1 + base ** c4)
        ) + c5

    if not math.isfinite(result) or result <= 0:
        raise ValueError("Invalid density result.")

    return result


def calculate_viscosity(fluid, temperature_k):
    """
    DIPPR Equation 101:

    ln(mu) = C1 + C2/T + C3*ln(T) + C4*T^C5

    Returns dynamic viscosity in Pa.s.
    """

    c1, c2, c3, c4, c5 = FLUIDS[fluid]["v"]

    if temperature_k <= 0:
        raise ValueError("Temperature must be above absolute zero.")

    exponent = (
        c1
        + c2 / temperature_k
        + c3 * math.log(temperature_k)
    )

    if c4 != 0:
        exponent += c4 * (temperature_k ** c5)

    if not math.isfinite(exponent) or exponent > 700 or exponent < -700:
        raise ValueError("Viscosity correlation is outside its valid range.")

    result = math.exp(exponent)

    if not math.isfinite(result) or result <= 0:
        raise ValueError("Invalid viscosity result.")

    return result


def calculate_properties(fluid, temperature_k):
    data = FLUIDS[fluid]

    molar_density = calculate_molar_density(
        fluid, temperature_k
    )

    # mol/dm3 x g/mol = g/dm3
    # Numerically equivalent to kg/m3

    density = molar_density * data["MW"]

    viscosity = calculate_viscosity(
        fluid, temperature_k
    )

    return molar_density, density, viscosity


# ==========================================================
# THEME
# ==========================================================

if st.session_state.dark_mode:
    bg = "#101827"
    panel = "#192538"
    panel2 = "#223249"
    text = "#F1F5F9"
    muted = "#A7B4C5"
    accent = "#38BDF8"
    border = "#30445E"
    input_bg = "#223249"
else:
    bg = "#F3F6FA"
    panel = "#FFFFFF"
    panel2 = "#EDF3F8"
    text = "#172B4D"
    muted = "#60728A"
    accent = "#087EBD"
    border = "#DCE5EF"
    input_bg = "#FFFFFF"


st.markdown(
    f"""
    <style>

    .stApp {{
        background: {bg};
        color: {text};
    }}

    [data-testid="stHeader"] {{
        background: {bg};
    }}

    [data-testid="stMainBlockContainer"] {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }}

    h1, h2, h3, h4, p, label {{
        color: {text};
    }}

    .brand {{
        color: {accent};
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 0;
    }}

    .subtitle {{
        color: {muted};
        font-size: 0.88rem;
        margin-top: -12px;
    }}

    .section-label {{
        color: {muted};
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }}

    .panel {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
    }}

    .result-number {{
        color: {accent};
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 850;
        line-height: 1.2;
        overflow-wrap: anywhere;
        margin: 7px 0;
    }}

    .result-label {{
        color: {muted};
        font-size: 0.73rem;
        font-weight: 800;
        letter-spacing: 1.3px;
    }}

    .result-description {{
        color: {muted};
        font-size: 0.83rem;
    }}

    .regime-name {{
        color: {text};
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 8px;
    }}

    .property-card {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 13px;
        padding: 15px;
        min-height: 105px;
    }}

    .property-value {{
        color: {text};
        font-size: 1.15rem;
        font-weight: 750;
        margin-top: 8px;
        overflow-wrap: anywhere;
    }}

    .property-unit {{
        color: {muted};
        font-size: 0.76rem;
    }}

    .small-muted {{
        color: {muted};
        font-size: 0.8rem;
    }}

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {{
        background: {input_bg};
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
        background: {panel};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 14px;
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
        min-height: 42px;
        font-weight: 650;
    }}

    div[data-testid="stExpander"] {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 12px;
    }}

    hr {{
        border-color: {border};
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HEADER
# ==========================================================

header1, header2, header3, header4 = st.columns(
    [3.2, 1.2, 1.2, 1.0],
    vertical_alignment="center"
)

with header1:
    logo_col, title_col = st.columns(
        [0.75, 4],
        vertical_alignment="center"
    )

    with logo_col:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=65)
        else:
            st.markdown(
                f'<h2 style="color:{accent};">R</h2>',
                unsafe_allow_html=True
            )

    with title_col:
        st.markdown(
            '<div class="brand">CHEMICAL ENGINEERING TOOL</div>',
            unsafe_allow_html=True
        )
        st.title("RCulator")
        st.markdown(
            '<div class="subtitle">Reynolds Number Calculator</div>',
            unsafe_allow_html=True
        )

with header2:
    st.selectbox(
        "Unit System",
        ["SI", "English"],
        key="system",
        on_change=change_units
    )

with header3:
    st.toggle(
        "Simple Mode",
        key="simple_mode"
    )

with header4:
    st.toggle(
        "Dark Mode",
        key="dark_mode"
    )


st.divider()


# ==========================================================
# UNIT LABELS
# ==========================================================

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
    density_unit = "lbm/ft³"
    viscosity_unit = "lbm/(ft·s)"


# ==========================================================
# CALCULATION INPUTS
# ==========================================================

st.markdown(
    '<div class="section-label">01 / CALCULATION INPUTS</div>',
    unsafe_allow_html=True
)

input_left, input_right = st.columns(
    [1.6, 1],
    gap="large"
)

with input_left:

    st.markdown("#### Operating Conditions")

    c1, c2 = st.columns(2)

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

    st.number_input(
        f"Fluid Temperature ({temperature_unit})",
        value=None,
        key="temperature",
        placeholder="Enter temperature",
        format="%.2f",
        min_value=-273.15 if st.session_state.system == "SI" else -459.67
    )

with input_right:

    st.markdown("#### Fluid Selection")

    fluid = st.selectbox(
        "Select Fluid",
        list(FLUIDS.keys()),
        key="fluid"
    )

    fluid_data = FLUIDS[fluid]

    st.markdown(
        f"""
        <div class="panel">
            <div class="result-label">SELECTED FLUID</div>
            <h3 style="margin:8px 0;">{fluid}</h3>
            <div class="small-muted">
                Chemical Formula: <b>{fluid_data['formula']}</b>
            </div>
            <div class="small-muted">
                Molar Mass: <b>{fluid_data['MW']} g/mol</b>
            </div>
            <div class="small-muted">
                Database: <b>20 available fluids</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Reset Inputs",
        use_container_width=True,
        on_click=reset_inputs
    ):
        pass


# ==========================================================
# CONVERT TEMPERATURE TO KELVIN
# ==========================================================

temperature = st.session_state.temperature

temperature_k = None

if temperature is not None:

    if st.session_state.system == "SI":
        temperature_k = temperature + 273.15
    else:
        temperature_k = (
            temperature + 459.67
        ) * 5 / 9


# ==========================================================
# CALCULATE FLUID PROPERTIES
# ==========================================================

molar_density = None
density_si = None
viscosity_si = None
property_error = None

if temperature_k is not None:

    try:
        (
            molar_density,
            density_si,
            viscosity_si
        ) = calculate_properties(
            fluid,
            temperature_k
        )

    except (ValueError, OverflowError, ZeroDivisionError) as e:
        property_error = str(e)


# ==========================================================
# DISPLAY FLUID PROPERTIES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">02 / FLUID PROPERTIES</div>',
    unsafe_allow_html=True
)

if density_si is not None and viscosity_si is not None:

    if st.session_state.system == "SI":
        density_display = density_si
        viscosity_display = viscosity_si

    else:
        density_display = density_si / 16.018463
        viscosity_display = viscosity_si * 0.020885434

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(
            f"""
            <div class="property-card">
                <div class="result-label">MOLAR DENSITY</div>
                <div class="property-value">
                    {molar_density:,.5f}
                </div>
                <div class="property-unit">mol/dm³</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p2:
        st.markdown(
            f"""
            <div class="property-card">
                <div class="result-label">MASS DENSITY</div>
                <div class="property-value">
                    {density_display:,.5f}
                </div>
                <div class="property-unit">{density_unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        st.markdown(
            f"""
            <div class="property-card">
                <div class="result-label">DYNAMIC VISCOSITY</div>
                <div class="property-value">
                    {viscosity_display:.7g}
                </div>
                <div class="property-unit">{viscosity_unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Fluid properties are automatically calculated "
        "using the selected fluid and temperature."
    )

elif temperature is None:

    st.info(
        "Enter a temperature to automatically calculate "
        "molar density, mass density, and dynamic viscosity."
    )

else:

    st.error(
        f"Fluid property calculation failed: {property_error}"
    )


# ==========================================================
# REYNOLDS NUMBER
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">03 / CALCULATION RESULT</div>',
    unsafe_allow_html=True
)

diameter = st.session_state.diameter
velocity = st.session_state.velocity

diameter_m = None
velocity_m_s = None

if diameter is not None:
    diameter_m = (
        diameter if st.session_state.system == "SI"
        else diameter * 0.3048
    )

if velocity is not None:
    velocity_m_s = (
        velocity if st.session_state.system == "SI"
        else velocity * 0.3048
    )


valid = (
    diameter_m is not None
    and velocity_m_s is not None
    and density_si is not None
    and viscosity_si is not None
    and diameter_m > 0
    and velocity_m_s > 0
    and density_si > 0
    and viscosity_si > 0
)


if valid:

    reynolds = (
        density_si
        * velocity_m_s
        * diameter_m
    ) / viscosity_si

    if reynolds < 2300:
        regime = "Laminar Flow"
        explanation = (
            "The fluid moves in smooth, orderly layers."
        )
        regime_color = "#16A34A"

    elif reynolds <= 4000:
        regime = "Transitional Flow"
        explanation = (
            "The flow is between laminar and turbulent."
        )
        regime_color = "#D97706"

    else:
        regime = "Turbulent Flow"
        explanation = (
            "The flow is irregular, with significant mixing."
        )
        regime_color = "#DC2626"

    result_col, regime_col = st.columns(
        [1.5, 1],
        gap="medium"
    )

    with result_col:

        st.markdown(
            f"""
            <div class="panel" style="min-height:190px;">
                <div class="result-label">
                    REYNOLDS NUMBER
                </div>
                <div class="result-number">
                    {reynolds:,.2f}
                </div>
                <div class="result-description">
                    Dimensionless quantity
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with regime_col:

        st.markdown(
            f"""
            <div class="panel" style="min-height:190px;">
                <div class="result-label">
                    FLOW CLASSIFICATION
                </div>
                <div class="regime-name"
                     style="color:{regime_color};">
                    {regime}
                </div>
                <div class="result-description">
                    {explanation}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ======================================================
    # FLOW REGIME GUIDE
    # ======================================================

    st.markdown("#### Flow Regime Reference")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.metric("Laminar", "Re < 2,300")

    with g2:
        st.metric("Transitional", "2,300–4,000")

    with g3:
        st.metric("Turbulent", "Re > 4,000")


    # ======================================================
    # ADVANCED CALCULATION DETAILS
    # ======================================================

    if not st.session_state.simple_mode:

        st.divider()

        st.markdown("### Calculation Breakdown")

        with st.expander(
            "1. Fluid Property Correlations",
            expanded=True
        ):

            if fluid == "Water":
                st.write("Water density polynomial:")
                st.latex(
                    r"\rho_m=C_1+C_2T+C_3T^2+C_4T^3+C_5T^4"
                )
            else:
                st.write("Density correlation (DIPPR 105):")
                st.latex(
                    r"\rho_m=\frac{C_1}"
                    r"{C_2^{[1+(1-T/C_3)^{C_4}]}}+C_5"
                )

            st.write("Dynamic viscosity correlation (DIPPR 101):")
            st.latex(
                r"\ln(\mu)=C_1+\frac{C_2}{T}"
                r"+C_3\ln(T)+C_4T^{C_5}"
            )

            st.write(
                f"Temperature: {temperature_k:.4f} K"
            )

            st.write(
                f"Molar density: {molar_density:.6f} mol/dm³"
            )

            st.write(
                f"Molar mass: {fluid_data['MW']} g/mol"
            )

            st.write(
                f"Mass density: {density_si:.6f} kg/m³"
            )

            st.write(
                f"Dynamic viscosity: {viscosity_si:.9g} Pa·s"
            )

        with st.expander(
            "2. Reynolds Number Substitution",
            expanded=True
        ):

            st.latex(
                r"Re=\frac{\rho VD}{\mu}"
            )

            st.write("Substituting SI values:")

            st.latex(
                rf"Re=\frac{{({density_si:.5f})"
                rf"({velocity_m_s:.6f})"
                rf"({diameter_m:.6f})}}"
                rf"{{{viscosity_si:.8g}}}"
            )

            st.latex(
                rf"Re={reynolds:,.2f}"
            )

        with st.expander("3. Flow Classification"):

            st.write(
                f"Calculated Reynolds Number: {reynolds:,.2f}"
            )

            st.write(f"Classification: {regime}")

            st.write(explanation)


else:

    missing = []

    if diameter is None:
        missing.append("pipe diameter")

    elif diameter <= 0:
        missing.append("positive pipe diameter")

    if velocity is None:
        missing.append("flow velocity")

    elif velocity <= 0:
        missing.append("positive flow velocity")

    if temperature is None:
        missing.append("fluid temperature")

    elif property_error:
        missing.append("valid fluid properties")

    st.markdown(
        """
        <div class="panel">
            <div class="result-label">
                REYNOLDS NUMBER
            </div>
            <div class="result-number">—</div>
            <div class="result-description">
                Complete the required inputs to calculate.
            </div>
            <hr>
            <div class="result-label">
                FLOW CLASSIFICATION
            </div>
            <div class="regime-name">
                Awaiting Input
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if missing:
        st.caption(
            "Required: " + ", ".join(missing)
        )


# ==========================================================
# IMPORTANT NOTES
# ==========================================================

with st.expander("About RCulator and calculation assumptions"):

    st.markdown(
        """
        **Calculation basis**

        - Density is calculated in mol/dm³ and converted
          into kg/m³ using molar mass.
        - Dynamic viscosity is calculated in Pa·s.
        - Reynolds Number is dimensionless.
        - English display uses lbm/ft³ and lbm/(ft·s).
        - Calculations are internally performed using SI units.

        **Flow classification**

        - Laminar: Re < 2,300
        - Transitional: 2,300 ≤ Re ≤ 4,000
        - Turbulent: Re > 4,000

        **Important:** Correlations must only be used within
        their published temperature and phase validity ranges.
        These ranges have not yet been supplied with the
        coefficient tables.
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    f"""
    <div style="text-align:center;padding:15px 0;">
        <div style="font-weight:800;color:{accent};">
            RCulator
        </div>
        <div class="small-muted">
            Reynolds Number Calculator
        </div>
        <div class="small-muted">
            A Chemical Engineering Computational Project
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
