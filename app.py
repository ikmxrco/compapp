
import math
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RCulator | Reynolds Number Calculator",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# FLUID DATABASE
# =========================================================

FLUIDS = {
    "Acetic acid": {
        "formula": "C2H4O2",
        "molar_mass": 60.052,
        "density": [1.4486, 0.25892, 591.95, 0.2529, 0],
        "viscosity": [-9.03, 1212.3, -0.322, 0, 0]
    },
    "Acetone": {
        "formula": "C3H6O",
        "molar_mass": 58.07914,
        "density": [1.2332, 0.25886, 508.2, 0.2913, 0],
        "viscosity": [-14.918, 1023.4, 0.5961, 0, 0]
    },
    "Benzene": {
        "formula": "C6H6",
        "molar_mass": 78.11184,
        "density": [1.0259, 0.26666, 562.05, 0.28394, 0],
        "viscosity": [7.5117, 294.68, -2.794, 0, 0]
    },
    "Butane": {
        "formula": "C4H10",
        "molar_mass": 58.1222,
        "density": [1.0677, 0.27188, 425.12, 0.28688, 0],
        "viscosity": [-7.2471, 534.82, -0.57469, -4.66e-27, 10]
    },
    "Carbon tetrachloride": {
        "formula": "CCl4",
        "molar_mass": 153.8227,
        "density": [0.99835, 0.274, 556.35, 0.287, 0],
        "viscosity": [-8.0738, 1121.1, -0.4726, 0, 0]
    },
    "Chlorobenzene": {
        "formula": "C6H5Cl",
        "molar_mass": 112.5569,
        "density": [0.8711, 0.26805, 632.35, 0.2799, 0],
        "viscosity": [0.15772, 540.5, -1.6075, 0, 0]
    },
    "Chloroform": {
        "formula": "CHCl3",
        "molar_mass": 119.37764,
        "density": [1.0841, 0.2581, 536.4, 0.2741, 0],
        "viscosity": [-14.109, 1049.2, 0.5377, 0, 0]
    },
    "Cyclohexane": {
        "formula": "C6H12",
        "molar_mass": 84.15948,
        "density": [0.88998, 0.27376, 553.8, 0.28571, 0],
        "viscosity": [-33.763, 2497.2, 3.2236, 0, 0]
    },
    "Diethyl ether": {
        "formula": "C4H10O",
        "molar_mass": 74.1216,
        "density": [0.9554, 0.26847, 466.7, 0.2814, 0],
        "viscosity": [10.197, -63.8, -3.226, 0, 0]
    },
    "Ethanol": {
        "formula": "C2H6O",
        "molar_mass": 46.06844,
        "density": [1.6288, 0.27469, 514, 0.23178, 0],
        "viscosity": [7.875, 781.98, -3.0418, 0, 0]
    },
    "Ethyl acetate": {
        "formula": "C4H8O2",
        "molar_mass": 88.10512,
        "density": [0.8996, 0.25856, 523.3, 0.278, 0],
        "viscosity": [14.354, -154.6, -3.7887, 0, 0]
    },
    "Ethylene glycol": {
        "formula": "C2H6O2",
        "molar_mass": 62.06784,
        "density": [1.315, 0.25125, 720, 0.21868, 0],
        "viscosity": [-290.36, 14251, 42.486, -0.000040369, 2]
    },
    "Heptane": {
        "formula": "C7H16",
        "molar_mass": 100.20194,
        "density": [0.61259, 0.26211, 540.2, 0.28141, 0],
        "viscosity": [-98.159, 3592.6, 14.197, -0.000029555, 2]
    },
    "Hexane": {
        "formula": "C6H14",
        "molar_mass": 86.17536,
        "density": [0.70824, 0.26411, 507.6, 0.27537, 0],
        "viscosity": [-56.569, 2140.5, 7.5175, -0.000017676, 2]
    },
    "Methanol": {
        "formula": "CH4O",
        "molar_mass": 32.04186,
        "density": [2.3267, 0.27073, 512.5, 0.24713, 0],
        "viscosity": [-25.317, 1789.2, 2.069, 0, 0]
    },
    "Octane": {
        "formula": "C8H18",
        "molar_mass": 114.22852,
        "density": [0.5266, 0.25693, 568.7, 0.28571, 0],
        "viscosity": [-98.805, 3905.5, 14.103, -0.000025112, 2]
    },
    "1-Propanol": {
        "formula": "C3H8O",
        "molar_mass": 60.09502,
        "density": [1.2457, 0.27281, 536.8, 0.23994, 0],
        "viscosity": [23.467, 116.07, -5.3372, 2880100000, -4.0267]
    },
    "2-Propanol": {
        "formula": "C3H8O",
        "molar_mass": 60.095,
        "density": [1.1799, 0.2644, 508.3, 0.24653, 0],
        "viscosity": [-8.8918, 2357.6, -0.91376, 0, 0]
    },
    "Toluene": {
        "formula": "C7H8",
        "molar_mass": 92.13842,
        "density": [0.8792, 0.27136, 591.75, 0.29241, 0],
        "viscosity": [-226.08, 6805.7, 37.542, -0.060853, 1]
    },
    "Water": {
        "formula": "H2O",
        "molar_mass": 18.01528,
        "density": [-13.851, 0.64038, -0.0019124, 0.0000018211, 0],
        "viscosity": [-52.843, 3703.6, 5.866, -5.88e-29, 10]
    }
}

# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "simple_mode" not in st.session_state:
    st.session_state.simple_mode = False

# =========================================================
# THEME
# =========================================================

dark = st.session_state.dark_mode

if dark:
    bg = "#101820"
    panel = "#192833"
    panel2 = "#203541"
    text = "#F1F5F9"
    muted = "#A9BAC7"
    accent = "#35C6B0"
    border = "#344B59"
    input_bg = "#203541"
else:
    bg = "#F3F7F8"
    panel = "#FFFFFF"
    panel2 = "#EAF2F3"
    text = "#172B35"
    muted = "#617782"
    accent = "#159C91"
    border = "#D8E4E7"
    input_bg = "#FFFFFF"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    [data-testid="stHeader"] {{
        background-color: {bg};
    }}

    [data-testid="stToolbar"] {{
        right: 1rem;
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }}

    h1, h2, h3, h4, p, label, span {{
        color: {text};
    }}

    .main-title {{
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: {text};
        margin-bottom: 0;
    }}

    .subtitle {{
        color: {muted};
        font-size: 0.95rem;
        margin-top: 0.25rem;
    }}

    .section-title {{
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
        color: {text};
    }}

    .panel {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 1.2rem 1.3rem;
        margin-bottom: 1rem;
    }}

    .metric-card {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 1rem 1.15rem;
        min-height: 112px;
    }}

    .metric-label {{
        color: {muted};
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
    }}

    .metric-value {{
        color: {text};
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        overflow-wrap: anywhere;
    }}

    .metric-unit {{
        color: {muted};
        font-size: 0.8rem;
        margin-top: 0.15rem;
    }}

    .result-card {{
        background: {panel2};
        border: 1px solid {accent};
        border-radius: 18px;
        padding: 1.4rem;
        text-align: center;
        margin: 0.5rem 0 1rem 0;
    }}

    .result-label {{
        color: {muted};
        font-size: 0.9rem;
        font-weight: 600;
    }}

    .result-number {{
        color: {accent};
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0.25rem 0;
    }}

    .result-regime {{
        color: {text};
        font-size: 1.05rem;
        font-weight: 700;
    }}

    .small-note {{
        color: {muted};
        font-size: 0.8rem;
    }}

    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {{
        background-color: {input_bg};
        color: {text};
        border-radius: 10px;
    }}

    div[data-testid="stNumberInput"] input {{
        border-color: {border};
    }}

    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {{
        color: {text};
    }}

    div.stButton > button {{
        border-radius: 10px;
        border: 1px solid {border};
        font-weight: 600;
        min-height: 2.5rem;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: {accent};
        border-color: {accent};
        color: white;
    }}

    div[data-testid="stExpander"] {{
        border: 1px solid {border};
        border-radius: 12px;
        background: {panel};
    }}

    hr {{
        border-color: {border};
    }}

    footer {{
        visibility: hidden;
    }}

    .footer {{
        text-align: center;
        color: {muted};
        font-size: 0.78rem;
        padding-top: 1.5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CALCULATION FUNCTIONS
# =========================================================

def calculate_density(fluid_name, temperature_c):
    """
    Returns:
        molar_density: mol/dm3
        mass_density: kg/m3
    """

    fluid = FLUIDS[fluid_name]
    c1, c2, c3, c4, c5 = fluid["density"]

    temperature_k = temperature_c + 273.15

    if temperature_k <= 0:
        raise ValueError("Temperature must be above absolute zero.")

    if fluid_name == "Water":
        molar_density = (
            c1
            + c2 * temperature_k
            + c3 * temperature_k**2
            + c4 * temperature_k**3
            + c5 * temperature_k**4
        )

    else:
        base = 1 - (temperature_k / c3)

        if base < 0 and not float(c4).is_integer():
            raise ValueError("Invalid temperature for density calculation.")

        exponent = 1 + (base ** c4)

        molar_density = c1 / (c2 ** exponent) + c5

    molar_mass = fluid["molar_mass"]

    # mol/dm3 × g/mol = g/dm3
    # Numerically, g/dm3 = kg/m3
    mass_density = molar_density * molar_mass

    if (
        not math.isfinite(molar_density)
        or not math.isfinite(mass_density)
        or molar_density <= 0
        or mass_density <= 0
    ):
        raise ValueError("Invalid density result.")

    return molar_density, mass_density


def calculate_viscosity(fluid_name, temperature_c):
    """
    DIPPR 101:
    ln(mu) = C1 + C2/T + C3*ln(T) + C4*T^C5

    Returns viscosity in Pa.s.
    """

    fluid = FLUIDS[fluid_name]
    c1, c2, c3, c4, c5 = fluid["viscosity"]

    temperature_k = temperature_c + 273.15

    if temperature_k <= 0:
        raise ValueError("Temperature must be above absolute zero.")

    try:
        ln_mu = (
            c1
            + (c2 / temperature_k)
            + (c3 * math.log(temperature_k))
            + (c4 * temperature_k**c5)
        )

        viscosity = math.exp(ln_mu)

    except (ValueError, OverflowError, ZeroDivisionError):
        raise ValueError("Unable to calculate viscosity at this temperature.")

    if not math.isfinite(viscosity) or viscosity <= 0:
        raise ValueError("Invalid viscosity result.")

    return viscosity


def get_reynolds_number(density, velocity, diameter, viscosity):
    return (density * velocity * diameter) / viscosity


def classify_flow(reynolds):
    if reynolds < 2300:
        return "Laminar Flow", "The flow is generally smooth and orderly."

    elif reynolds <= 4000:
        return "Transitional Flow", "The flow is in the transition region."

    else:
        return "Turbulent Flow", "The flow is generally irregular and mixing."


def format_number(value, decimals=4):
    if value is None:
        return "--"

    if not math.isfinite(value):
        return "--"

    if value != 0 and (abs(value) >= 1e7 or abs(value) < 1e-4):
        return f"{value:.4e}"

    return f"{value:,.{decimals}f}"


# =========================================================
# RESET FUNCTION
# =========================================================

def reset_inputs():
    st.session_state.diameter = None
    st.session_state.velocity = None
    st.session_state.temperature = None
    st.session_state.fluid = "Select a fluid"


# =========================================================
# HEADER
# =========================================================

# Centered logo above the app name
logo_col = st.columns([1, 2, 1])[1]

with logo_col:
    st.image(
        "assets/logo.png",
        use_container_width=True
    )

# Centered app name and subtitle
st.markdown(
    """
    <div style="text-align: center;">
        <div class="main-title">RCulator</div>
        <div class="subtitle">
            Reynolds Number Calculator | Chemical Engineering
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# Display settings underneath the centered header
dark_col, mode_col = st.columns(2)

with dark_col:
    st.toggle(
        "Dark Mode",
        key="dark_mode"
    )

with mode_col:
    st.toggle(
        "Simple Mode",
        key="simple_mode"
    )

st.markdown("---")

# =========================================================
# SETTINGS
# =========================================================

settings_col, reset_col = st.columns([4, 1])

with settings_col:
    unit_system = st.selectbox(
        "Unit System",
        ["SI Units", "English Units"],
        help="Choose the units used for your inputs and displayed results."
    )

with reset_col:
    st.write("")
    st.write("")
    st.button(
        "Reset Inputs",
        on_click=reset_inputs,
        use_container_width=True
    )

# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">01 | Input Parameters</div>',
    unsafe_allow_html=True
)

input_col1, input_col2 = st.columns(2)

with input_col1:
    fluid_options = ["Select a fluid"] + list(FLUIDS.keys())

    selected_fluid = st.selectbox(
        "Select Fluid",
        fluid_options,
        key="fluid"
    )

    if selected_fluid != "Select a fluid":
        st.caption(
            f"Chemical formula: {FLUIDS[selected_fluid]['formula']}"
        )

    if unit_system == "SI Units":
        diameter_label = "Pipe Diameter (m)"
        velocity_label = "Flow Velocity (m/s)"
        temperature_label = "Temperature (°C)"
    else:
        diameter_label = "Pipe Diameter (ft)"
        velocity_label = "Flow Velocity (ft/s)"
        temperature_label = "Temperature (°F)"

    diameter = st.number_input(
        diameter_label,
        min_value=0.0,
        value=None,
        placeholder="Enter pipe diameter",
        key="diameter",
        format="%.6f"
    )

    velocity = st.number_input(
        velocity_label,
        min_value=0.0,
        value=None,
        placeholder="Enter flow velocity",
        key="velocity",
        format="%.6f"
    )

with input_col2:
    temperature = st.number_input(
        temperature_label,
        value=None,
        placeholder="Enter fluid temperature",
        key="temperature",
        format="%.2f"
    )

    st.markdown(
        f"""
        <div class="panel">
            <div class="section-title">Calculation Overview</div>
            <p class="small-note">
                RCulator automatically calculates the fluid density
                and dynamic viscosity using the selected fluid and
                temperature.
            </p>
            <p class="small-note">
                The Reynolds Number is calculated using the SI
                equivalent of the entered parameters.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# INPUT CONVERSION TO SI
# =========================================================

diameter_m = None
velocity_m_s = None
temperature_c = None

if diameter is not None:
    if unit_system == "SI Units":
        diameter_m = diameter
    else:
        diameter_m = diameter * 0.3048

if velocity is not None:
    if unit_system == "SI Units":
        velocity_m_s = velocity
    else:
        velocity_m_s = velocity * 0.3048

if temperature is not None:
    if unit_system == "SI Units":
        temperature_c = temperature
    else:
        temperature_c = (temperature - 32) * 5 / 9

# =========================================================
# CALCULATIONS
# =========================================================

calculation_ready = (
    selected_fluid != "Select a fluid"
    and diameter_m is not None
    and velocity_m_s is not None
    and temperature_c is not None
    and diameter_m > 0
    and velocity_m_s > 0
)

density_molar = None
density_si = None
viscosity_si = None
reynolds = None
regime = None
regime_description = None
calculation_error = None

if calculation_ready:
    try:
        density_molar, density_si = calculate_density(
            selected_fluid,
            temperature_c
        )

        viscosity_si = calculate_viscosity(
            selected_fluid,
            temperature_c
        )

        reynolds = get_reynolds_number(
            density_si,
            velocity_m_s,
            diameter_m,
            viscosity_si
        )

        regime, regime_description = classify_flow(reynolds)

    except (ValueError, OverflowError, ZeroDivisionError) as error:
        calculation_error = str(error)

# =========================================================
# RESULTS SECTION
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">02 | Calculated Results</div>',
    unsafe_allow_html=True
)

if calculation_error:
    st.error(calculation_error)

elif not calculation_ready:
    st.info(
        "Select a fluid and enter the pipe diameter, flow velocity, "
        "and temperature to calculate the Reynolds Number."
    )

else:
    # -----------------------------------------------------
    # DISPLAY UNIT CONVERSIONS
    # -----------------------------------------------------

    if unit_system == "SI Units":
        density_display = density_si
        density_unit = "kg/m³"

        viscosity_display = viscosity_si
        viscosity_unit = "Pa·s"

        diameter_display = diameter_m
        diameter_unit = "m"

        velocity_display = velocity_m_s
        velocity_unit = "m/s"

        temperature_display = temperature_c
        temperature_unit = "°C"

    else:
        density_display = density_si * 0.06242796
        density_unit = "lbm/ft³"

        # Pa.s to lbm/(ft.s)
        viscosity_display = viscosity_si * 0.671968975
        viscosity_unit = "lbm/(ft·s)"

        diameter_display = diameter_m / 0.3048
        diameter_unit = "ft"

        velocity_display = velocity_m_s / 0.3048
        velocity_unit = "ft/s"

        temperature_display = temperature_c * 9 / 5 + 32
        temperature_unit = "°F"

    # -----------------------------------------------------
    # REYNOLDS NUMBER RESULT
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">REYNOLDS NUMBER</div>
            <div class="result-number">{format_number(reynolds, 2)}</div>
            <div class="result-regime">{regime}</div>
            <div class="small-note">{regime_description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # FLUID PROPERTIES
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Fluid Properties</div>',
        unsafe_allow_html=True
    )

    prop1, prop2, prop3 = st.columns(3)

    with prop1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">MASS DENSITY</div>
                <div class="metric-value">
                    {format_number(density_display, 4)}
                </div>
                <div class="metric-unit">{density_unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with prop2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">DYNAMIC VISCOSITY</div>
                <div class="metric-value">
                    {format_number(viscosity_display, 6)}
                </div>
                <div class="metric-unit">{viscosity_unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with prop3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">MOLAR DENSITY</div>
                <div class="metric-value">
                    {format_number(density_molar, 4)}
                </div>
                <div class="metric-unit">mol/dm³</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # INPUT SUMMARY
    # -----------------------------------------------------

    st.write("")
    st.markdown(
        '<div class="section-title">Input Summary</div>',
        unsafe_allow_html=True
    )

    sum1, sum2, sum3 = st.columns(3)

    with sum1:
        st.metric(
            "Pipe Diameter",
            f"{format_number(diameter_display, 4)} {diameter_unit}"
        )

    with sum2:
        st.metric(
            "Flow Velocity",
            f"{format_number(velocity_display, 4)} {velocity_unit}"
        )

    with sum3:
        st.metric(
            "Temperature",
            f"{format_number(temperature_display, 2)} {temperature_unit}"
        )

    # =====================================================
    # ADVANCED MODE
    # =====================================================

    if not st.session_state.simple_mode:

        st.markdown("---")

        st.markdown(
            '<div class="section-title">03 | Calculation Details</div>',
            unsafe_allow_html=True
        )

        with st.expander("Density Calculation", expanded=False):

            if selected_fluid == "Water":
                st.markdown("**Water density correlation**")

                st.latex(
                    r"\rho_m=C_1+C_2T+C_3T^2+C_4T^3+C_5T^4"
                )

            else:
                st.markdown("**Density correlation**")

                st.latex(
                    r"\rho_m=\frac{C_1}"
                    r"{C_2^{[1+(1-T/C_3)^{C_4}]}}+C_5"
                )

            st.write(f"Fluid: {selected_fluid}")
            st.write(f"Temperature: {temperature_c:.4f} °C")
            st.write(f"Temperature: {temperature_c + 273.15:.4f} K")

            st.write(
                f"Molar density: {density_molar:.6f} mol/dm³"
            )

            st.write(
                f"Molar mass: {FLUIDS[selected_fluid]['molar_mass']} g/mol"
            )

            st.latex(
                r"\rho=\rho_m \times M"
            )

            st.write(
                f"Mass density = {density_molar:.6f} "
                f"× {FLUIDS[selected_fluid]['molar_mass']}"
            )

            st.success(
                f"Mass density = {density_si:.6f} kg/m³"
            )

        with st.expander("Viscosity Calculation", expanded=False):

            st.markdown("**DIPPR 101 viscosity correlation**")

            st.latex(
                r"\ln(\mu)=C_1+\frac{C_2}{T}"
                r"+C_3\ln(T)+C_4T^{C_5}"
            )

            st.write(f"Fluid: {selected_fluid}")
            st.write(f"Temperature: {temperature_c + 273.15:.4f} K")

            st.success(
                f"Dynamic viscosity = {viscosity_si:.8e} Pa·s"
            )

        with st.expander("Reynolds Number Calculation", expanded=True):

            st.latex(
                r"Re=\frac{\rho vD}{\mu}"
            )

            st.write("Where:")

            st.markdown(
                """
                - **Re** = Reynolds Number
                - **ρ** = Mass density (kg/m³)
                - **v** = Flow velocity (m/s)
                - **D** = Pipe diameter (m)
                - **μ** = Dynamic viscosity (Pa·s)
                """
            )

            st.markdown("**Substitution:**")

            st.latex(
                rf"Re=\frac{{({density_si:.6f})"
                rf"({velocity_m_s:.6f})"
                rf"({diameter_m:.6f})}}"
                rf"{{{viscosity_si:.6e}}}"
            )

            st.success(
                f"Final Reynolds Number = {reynolds:,.2f}"
            )

        with st.expander("Flow Regime Classification", expanded=False):

            st.write(f"Calculated Reynolds Number: {reynolds:,.2f}")

            st.markdown(
                """
                | Reynolds Number | Flow Regime |
                |---|---|
                | Re < 2,300 | Laminar |
                | 2,300 ≤ Re ≤ 4,000 | Transitional |
                | Re > 4,000 | Turbulent |
                """
            )

            st.info(f"Classification: {regime}")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        <b>RCulator</b> | Reynolds Number Calculator
        <br>
        Chemical Engineering Project
    </div>
    """,
    unsafe_allow_html=True
)
