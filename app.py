
import streamlit as st

st.set_page_config(
    page_title="RCulator",
    page_icon="R",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "system": "SI",
    "previous_system": "SI",
    "dark_mode": False,
    "simple_mode": True,
    "diameter": 0.05,
    "velocity": 2.0,
    "temperature": 20.0,
    "density": 998.2,
    "viscosity": 0.001002,
    "fluid_mode": "Water",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# UNIT SWITCHING
# =====================================================

def change_units():
    old = st.session_state.previous_system
    new = st.session_state.system

    if old == new:
        return

    if old == "SI" and new == "English":
        st.session_state.diameter /= 0.0254
        st.session_state.velocity /= 0.3048
        st.session_state.temperature = (
            st.session_state.temperature * 9 / 5 + 32
        )
        st.session_state.density /= 16.018463
        st.session_state.viscosity /= 1.488164

    elif old == "English" and new == "SI":
        st.session_state.diameter *= 0.0254
        st.session_state.velocity *= 0.3048
        st.session_state.temperature = (
            (st.session_state.temperature - 32) * 5 / 9
        )
        st.session_state.density *= 16.018463
        st.session_state.viscosity *= 1.488164

    st.session_state.previous_system = new


# =====================================================
# WATER PROPERTIES
# =====================================================

water_temps = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

water_density = [
    999.84, 999.70, 998.21, 995.65, 992.22,
    988.04, 983.20, 977.76, 971.80, 965.31, 958.35
]

water_viscosity = [
    0.001792, 0.001307, 0.001002, 0.000798,
    0.000653, 0.000547, 0.000466, 0.000404,
    0.000355, 0.000315, 0.000282
]


def interpolate(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]

    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            fraction = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + fraction * (ys[i + 1] - ys[i])

    return ys[-1]


# =====================================================
# THEME
# =====================================================

if st.session_state.dark_mode:
    colors = {
        "bg": "#101827",
        "panel": "#1B293D",
        "input": "#213149",
        "text": "#F1F5F9",
        "muted": "#B2C0D1",
        "accent": "#55B8F0",
        "border": "#35465D",
    }
else:
    colors = {
        "bg": "#F3F6FA",
        "panel": "#FFFFFF",
        "input": "#FFFFFF",
        "text": "#172B45",
        "muted": "#53657C",
        "accent": "#087DBB",
        "border": "#D5E0EB",
    }

st.markdown(
    f"""
    <style>
    .stApp,
    [data-testid="stAppViewContainer"] {{
        background: {colors["bg"]} !important;
        color: {colors["text"]} !important;
    }}

    [data-testid="stHeader"] {{
        background: {colors["bg"]} !important;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }}

    /* Text */

    .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp p, .stApp label,
    .stApp [data-testid="stMarkdownContainer"] {{
        color: {colors["text"]} !important;
    }}

    .stApp [data-testid="stCaptionContainer"],
    .stApp small {{
        color: {colors["muted"]} !important;
    }}

    /* Input fields */

    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div {{
        background: {colors["input"]} !important;
        border: 1px solid {colors["border"]} !important;
        border-radius: 8px !important;
    }}

    [data-baseweb="input"] input {{
        color: {colors["text"]} !important;
        -webkit-text-fill-color: {colors["text"]} !important;
    }}

    [data-baseweb="select"] *,
    [data-baseweb="popover"] * {{
        color: {colors["text"]} !important;
    }}

    [data-baseweb="popover"] ul {{
        background: {colors["panel"]} !important;
    }}

    [data-testid="stNumberInput"] button {{
        background: {colors["input"]} !important;
        color: {colors["text"]} !important;
        border-color: {colors["border"]} !important;
    }}

    /* Metrics */

    [data-testid="stMetric"] {{
        background: {colors["panel"]} !important;
        border: 1px solid {colors["border"]} !important;
        border-radius: 12px;
        padding: 12px;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {{
        color: {colors["muted"]} !important;
    }}

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {{
        color: {colors["text"]} !important;
    }}

    /* Containers */

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {colors["panel"]} !important;
        border-color: {colors["border"]} !important;
        border-radius: 12px !important;
    }}

    /* Buttons */

    .stButton button {{
        background: {colors["panel"]} !important;
        color: {colors["text"]} !important;
        border-color: {colors["border"]} !important;
        border-radius: 8px !important;
    }}

    /* RCulator styling */

    .brand {{
        color: {colors["accent"]} !important;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2.5px;
    }}

    .subtitle {{
        color: {colors["muted"]} !important;
        font-size: 13px;
        margin-top: -10px;
    }}

    .result-number {{
        color: {colors["accent"]} !important;
        font-size: clamp(32px, 5vw, 48px);
        font-weight: 850;
        letter-spacing: -1px;
    }}

    .result-label {{
        color: {colors["muted"]} !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }}

    .simple-info {{
        color: {colors["muted"]} !important;
        font-size: 12px;
    }}

    hr {{
        border-color: {colors["border"]} !important;
    }}

    /* Phone layout */

    @media (max-width: 640px) {{
        .block-container {{
            padding: 0.7rem 0.7rem 1.5rem 0.7rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# HEADER - CONTROLS HAVE THEIR OWN SPACE
# =====================================================

st.markdown(
    '<div class="brand">ENGINEERING CALCULATOR</div>',
    unsafe_allow_html=True
)

header1, header2, header3, header4 = st.columns([2.2, 1, 1, 1])

with header1:
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


# =====================================================
# UNIT LABELS
# =====================================================

system = st.session_state.system

if system == "SI":
    d_unit = "m"
    v_unit = "m/s"
    t_unit = "°C"
    rho_unit = "kg/m³"
    mu_unit = "Pa·s"
else:
    d_unit = "in"
    v_unit = "ft/s"
    t_unit = "°F"
    rho_unit = "lbm/ft³"
    mu_unit = "lbm/(ft·s)"


# =====================================================
# SIMPLE MODE
# =====================================================

if st.session_state.simple_mode:

    st.markdown("### Flow parameters")

    # Five compact columns: all essential inputs in one row.
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")

    with c1:
        diameter = st.number_input(
            f"Diameter ({d_unit})",
            min_value=0.000001,
            format="%.5f",
            key="diameter"
        )

    with c2:
        velocity = st.number_input(
            f"Velocity ({v_unit})",
            min_value=0.000001,
            format="%.5f",
            key="velocity"
        )

    with c3:
        st.selectbox(
            "Fluid",
            ["Water", "Custom"],
            key="fluid_mode"
        )

    if st.session_state.fluid_mode == "Water":

        with c4:
            temperature = st.number_input(
                f"Temperature ({t_unit})",
                min_value=0.0 if system == "SI" else 32.0,
                max_value=100.0 if system == "SI" else 212.0,
                step=1.0,
                key="temperature"
            )

        if system == "SI":
            temp_c = temperature
        else:
            temp_c = (temperature - 32) * 5 / 9

        rho_si = interpolate(temp_c, water_temps, water_density)
        mu_si = interpolate(temp_c, water_temps, water_viscosity)

        if system == "SI":
            rho_display = rho_si
            mu_display = mu_si
        else:
            rho_display = rho_si / 16.018463
            mu_display = mu_si / 1.488164

        with c5:
            st.markdown("**Water properties**")
            st.caption(f"ρ = {rho_display:.3f} {rho_unit}")
            st.caption(f"μ = {mu_display:.6f} {mu_unit}")

    else:
        with c4:
            rho_display = st.number_input(
                f"Density ({rho_unit})",
                min_value=0.000001,
                format="%.5f",
                key="density"
            )

        with c5:
            mu_display = st.number_input(
                f"Viscosity ({mu_unit})",
                min_value=0.000000001,
                format="%.8f",
                key="viscosity"
            )

        if system == "SI":
            rho_si = rho_display
            mu_si = mu_display
        else:
            rho_si = rho_display * 16.018463
            mu_si = mu_display * 1.488164

    # Convert dimensions to SI.

    if system == "SI":
        diameter_si = diameter
        velocity_si = velocity
    else:
        diameter_si = diameter * 0.0254
        velocity_si = velocity * 0.3048

    valid = (
        diameter_si > 0
        and velocity_si > 0
        and rho_si > 0
        and mu_si > 0
    )

    if valid:
        reynolds = rho_si * velocity_si * diameter_si / mu_si

        if reynolds < 2300:
            regime = "Laminar"
            regime_range = "Re < 2,300"
        elif reynolds <= 4000:
            regime = "Transitional"
            regime_range = "2,300–4,000"
        else:
            regime = "Turbulent"
            regime_range = "Re > 4,000"

    else:
        reynolds = 0
        regime = "Invalid inputs"
        regime_range = "Check your values"

    st.divider()
    st.markdown("### Calculation result")

    # Main result displayed side by side.

    result1, result2 = st.columns([1.5, 1], gap="medium")

    with result1:
        with st.container(border=True):
            st.markdown(
                '<div class="result-label">REYNOLDS NUMBER</div>',
                unsafe_allow_html=True
            )

            if valid:
                st.markdown(
                    f'<div class="result-number">{reynolds:,.2f}</div>',
                    unsafe_allow_html=True
                )
                st.caption("Dimensionless")
            else:
                st.warning("Check your input values.")

    with result2:
        with st.container(border=True):
            st.markdown("**FLOW REGIME**")

            if valid:
                st.subheader(regime)
                st.caption(regime_range)
            else:
                st.caption("Waiting for valid inputs")

    # Compact flow reference, without additional cards.

    st.caption(
        "FLOW GUIDE     •     LAMINAR: Re < 2,300"
        "     •     TRANSITIONAL: 2,300–4,000"
        "     •     TURBULENT: Re > 4,000"
    )

    st.caption("RCulator | Reynolds Number Calculator")


# =====================================================
# FULL MODE
# =====================================================

else:

    st.markdown("### Flow regime reference")

    f1, f2, f3 = st.columns(3)

    with f1:
        with st.container(border=True):
            st.markdown("**LAMINAR**")
            st.markdown("Re < 2,300")
            st.caption("Smooth, orderly flow.")

    with f2:
        with st.container(border=True):
            st.markdown("**TRANSITIONAL**")
            st.markdown("2,300–4,000")
            st.caption("Unstable flow region.")

    with f3:
        with st.container(border=True):
            st.markdown("**TURBULENT**")
            st.markdown("Re > 4,000")
            st.caption("Irregular, mixed flow.")

    st.divider()
    st.markdown("### Flow conditions")

    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.markdown("**Geometry and velocity**")

            diameter = st.number_input(
                f"Pipe diameter ({d_unit})",
                min_value=0.000001,
                format="%.5f",
                key="diameter"
            )

            velocity = st.number_input(
                f"Average velocity ({v_unit})",
                min_value=0.000001,
                format="%.5f",
                key="velocity"
            )

    with right:
        with st.container(border=True):
            st.markdown("**Fluid properties**")

            st.selectbox(
                "Fluid",
                ["Water", "Custom"],
                key="fluid_mode"
            )

            if st.session_state.fluid_mode == "Water":

                temperature = st.number_input(
                    f"Water temperature ({t_unit})",
                    min_value=0.0 if system == "SI" else 32.0,
                    max_value=100.0 if system == "SI" else 212.0,
                    step=1.0,
                    key="temperature"
                )

                if system == "SI":
                    temp_c = temperature
                else:
                    temp_c = (temperature - 32) * 5 / 9

                rho_si = interpolate(temp_c, water_temps, water_density)
                mu_si = interpolate(temp_c, water_temps, water_viscosity)

                if system == "SI":
                    rho_display = rho_si
                    mu_display = mu_si
                else:
                    rho_display = rho_si / 16.018463
                    mu_display = mu_si / 1.488164

                p1, p2 = st.columns(2)

                with p1:
                    st.metric("Density", f"{rho_display:.4f}")
                    st.caption(rho_unit)

                with p2:
                    st.metric("Viscosity", f"{mu_display:.6f}")
                    st.caption(mu_unit)

            else:
                rho_display = st.number_input(
                    f"Density ({rho_unit})",
                    min_value=0.000001,
                    format="%.5f",
                    key="density"
                )

                mu_display = st.number_input(
                    f"Viscosity ({mu_unit})",
                    min_value=0.000000001,
                    format="%.8f",
                    key="viscosity"
                )

                if system == "SI":
                    rho_si = rho_display
                    mu_si = mu_display
                else:
                    rho_si = rho_display * 16.018463
                    mu_si = mu_display * 1.488164

    # Calculation

    if system == "SI":
        diameter_si = diameter
        velocity_si = velocity
    else:
        diameter_si = diameter * 0.0254
        velocity_si = velocity * 0.3048

    valid = (
        diameter_si > 0
        and velocity_si > 0
        and rho_si > 0
        and mu_si > 0
    )

    if valid:
        reynolds = rho_si * velocity_si * diameter_si / mu_si

        if reynolds < 2300:
            regime = "Laminar"
            regime_range = "Re < 2,300"
            description = "Smooth, orderly fluid motion."
        elif reynolds <= 4000:
            regime = "Transitional"
            regime_range = "2,300–4,000"
            description = "Flow is in the transition region."
        else:
            regime = "Turbulent"
            regime_range = "Re > 4,000"
            description = "Irregular flow with increased mixing."

    else:
        reynolds = 0
        regime = "Invalid inputs"
        regime_range = "Check your values"
        description = ""

    st.divider()
    st.markdown("### Calculation results")

    if valid:
        r1, r2 = st.columns([1.5, 1])

        with r1:
            with st.container(border=True):
                st.markdown(
                    '<div class="result-label">REYNOLDS NUMBER</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="result-number">{reynolds:,.2f}</div>',
                    unsafe_allow_html=True
                )

        with r2:
            with st.container(border=True):
                st.markdown("**FLOW CLASSIFICATION**")
                st.subheader(regime)
                st.caption(regime_range)
                st.caption(description)

        with st.expander("View calculation details"):
            st.latex(r"Re = \frac{\rho V D}{\mu}")

            st.write(f"Density: {rho_si:.6f} kg/m³")
            st.write(f"Velocity: {velocity_si:.6f} m/s")
            st.write(f"Diameter: {diameter_si:.6f} m")
            st.write(f"Viscosity: {mu_si:.9f} Pa·s")

            st.latex(
                rf"Re = \frac{{({rho_si:.4f})({velocity_si:.4f})({diameter_si:.6f})}}{{{mu_si:.9f}}}"
            )
            st.latex(rf"Re = {reynolds:,.2f}")

    else:
        st.warning("Check your input values.")

    st.caption("RCulator | Reynolds Number Calculator | Chemical Engineering")
