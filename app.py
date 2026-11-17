import streamlit as st
import math

st.set_page_config(page_title="RCulator", page_icon="〰️", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
.stApp { background: #fbfcff; color: #172554; }
.block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 3rem; }
h1, h2, h3 { color: #14264f; }
.rc-brand { font-size: 2.15rem; font-weight: 800; letter-spacing: -1.5px; color: #14264f; }
.rc-sub { color: #64748b; margin-top: -10px; font-size: .95rem; }
.section-title { font-weight: 800; letter-spacing: .08em; color: #243b68; font-size: .83rem; margin: 1.1rem 0 .5rem; }
div[data-testid="stMetric"] { background: white; border: 1.5px solid #263d70; border-radius: 10px; padding: 15px 17px; }
div[data-testid="stMetric"] label { color: #64748b !important; }
div[data-testid="stMetricValue"] { color: #172554 !important; font-family: 'DM Mono', monospace; }
div[data-testid="stForm"] { border: 1.5px solid #263d70; border-radius: 10px; padding: 16px; background: white; }
div[data-testid="stSelectbox"], div[data-testid="stNumberInput"] { margin-bottom: .25rem; }
.rc-note { color: #64748b; font-size: .82rem; }
.rc-result { border: 1.5px solid #263d70; border-radius: 10px; background: white; padding: 18px; }
</style>
""", unsafe_allow_html=True)

# Approximate liquid-water properties at atmospheric pressure.
# Values: temperature (°C), density (kg/m³), dynamic viscosity (Pa·s)
WATER_TABLE = [
    (0, 999.84, 1.792e-3), (5, 999.97, 1.519e-3),
    (10, 999.70, 1.307e-3), (15, 999.10, 1.138e-3),
    (20, 998.21, 1.002e-3), (25, 997.05, 0.890e-3),
    (30, 995.65, 0.798e-3), (35, 994.03, 0.719e-3),
    (40, 992.22, 0.653e-3), (45, 990.21, 0.596e-3),
    (50, 988.04, 0.547e-3), (55, 985.69, 0.504e-3),
    (60, 983.20, 0.466e-3), (65, 980.55, 0.433e-3),
    (70, 977.76, 0.404e-3), (75, 974.84, 0.378e-3),
    (80, 971.80, 0.355e-3), (85, 968.65, 0.333e-3),
    (90, 965.31, 0.315e-3), (95, 961.89, 0.297e-3),
    (100, 958.35, 0.282e-3)
]

def water_properties(temp_c):
    if temp_c < 0 or temp_c > 100:
        raise ValueError("The built-in water property table supports 0 to 100 °C.")
    for i in range(len(WATER_TABLE) - 1):
        t0, rho0, mu0 = WATER_TABLE[i]
        t1, rho1, mu1 = WATER_TABLE[i + 1]
        if t0 <= temp_c <= t1:
            f = (temp_c - t0) / (t1 - t0)
            return rho0 + f * (rho1 - rho0), mu0 + f * (mu1 - mu0)
    return WATER_TABLE[-1][1], WATER_TABLE[-1][2]

def to_celsius(value, unit):
    if unit == "°C": return value
    if unit == "°F": return (value - 32) * 5 / 9
    if unit == "K": return value - 273.15
    if unit == "°R": return value * 5 / 9 - 273.15
    return value

def to_meters(value, unit):
    return value * {"m": 1, "cm": 0.01, "mm": 0.001, "in": 0.0254, "ft": 0.3048}.get(unit, 1)

def to_m_per_s(value, unit):
    return value * {"m/s": 1, "cm/s": 0.01, "mm/s": 0.001, "ft/s": 0.3048, "km/h": 1/3.6}.get(unit, 1)

def density_to_si(value, unit):
    return value * {"kg/m³": 1, "g/cm³": 1000, "lbm/ft³": 16.018463}.get(unit, 1)

def viscosity_to_si(value, unit):
    return value * {"Pa·s": 1, "mPa·s (cP)": 1e-3, "P": 0.1, "lbm/(ft·s)": 1.488164}.get(unit, 1)

def fmt(value, digits=4):
    return f"{value:,.{digits}g}"

st.markdown('<div class="rc-brand">RCulator<span style="color:#5574b9">.</span></div>', unsafe_allow_html=True)
st.markdown('<div class="rc-sub">A Reynolds Number calculator for fluid-flow problems</div>', unsafe_allow_html=True)
st.divider()

left, right = st.columns([1.12, 0.88], gap="large")

with left:
    st.markdown('<div class="section-title">INPUTS</div>', unsafe_allow_html=True)
    system = st.selectbox("Unit system", ["SI", "English"], help="Choose a system for the displayed input and output units. You can still choose individual units.")
    fluid_mode = st.selectbox("Fluid / property source", ["Water (properties vary with temperature)", "Custom fluid (enter properties)"])
    a, b = st.columns(2)
    with a:
        diameter = st.number_input("Diameter", min_value=0.000001, value=0.050, step=0.005, format="%.6f")
        diameter_unit = st.selectbox("Diameter unit", ["m", "cm", "mm", "in", "ft"] if system == "SI" else ["ft", "in", "m", "cm", "mm"], index=0 if system == "SI" else 0)
    with b:
        velocity = st.number_input("Velocity", min_value=0.000001, value=1.000, step=0.1, format="%.6f")
        velocity_unit = st.selectbox("Velocity unit", ["m/s", "cm/s", "mm/s", "ft/s", "km/h"] if system == "SI" else ["ft/s", "m/s", "km/h", "cm/s", "mm/s"])
    temp_col, temp_unit_col = st.columns(2)
    with temp_col:
        temperature = st.number_input("Temperature", value=20.0, step=1.0, format="%.2f")
    with temp_unit_col:
        temp_unit = st.selectbox("Temperature unit", ["°C", "K", "°F", "°R"])

    if fluid_mode.startswith("Custom"):
        st.markdown('<div class="section-title">CUSTOM FLUID PROPERTIES</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            rho_value = st.number_input("Density", min_value=0.000001, value=998.2, format="%.6f")
            rho_unit = st.selectbox("Density unit", ["kg/m³", "g/cm³", "lbm/ft³"])
        with c2:
            mu_value = st.number_input("Dynamic viscosity", min_value=0.000000001, value=0.001002, format="%.9f")
            mu_unit = st.selectbox("Viscosity unit", ["Pa·s", "mPa·s (cP)", "P", "lbm/(ft·s)"])
    else:
        st.caption("Built-in water properties are interpolated from a reference table at atmospheric pressure (0–100 °C).")

    calculate = st.button("Calculate Reynolds Number", type="primary", use_container_width=True)

with right:
    st.markdown('<div class="section-title">OUTPUTS</div>', unsafe_allow_html=True)
    result_area = st.container()

if calculate:
    try:
        D = to_meters(diameter, diameter_unit)
        V = to_m_per_s(velocity, velocity_unit)
        T_C = to_celsius(temperature, temp_unit)
        if fluid_mode.startswith("Water"):
            rho, mu = water_properties(T_C)
        else:
            rho = density_to_si(rho_value, rho_unit)
            mu = viscosity_to_si(mu_value, mu_unit)
        if D <= 0 or V < 0 or rho <= 0 or mu <= 0:
            raise ValueError("Diameter, density, and viscosity must be greater than zero; velocity cannot be negative.")
        Re = rho * V * D / mu
        if Re < 2300:
            regime = "Laminar"
            explanation = "Viscous forces dominate the flow."
        elif Re <= 4000:
            regime = "Transitional"
            explanation = "The flow is in the transition region."
        else:
            regime = "Turbulent"
            explanation = "Inertial effects dominate the flow."
        with result_area:
            st.metric("Reynolds Number (Re)", f"{Re:,.2f}")
            r1, r2 = st.columns(2)
            r1.metric("Density, ρ", f"{rho:,.3f} kg/m³")
            r2.metric("Dynamic viscosity, μ", f"{mu:.5g} Pa·s")
            st.markdown(f"""
            <div class="rc-result">
              <div class="section-title" style="margin-top:0">FLOW REGIME</div>
              <div style="font-size:1.55rem;font-weight:800;color:#172554">{regime}</div>
              <div style="color:#64748b;font-size:.9rem">{explanation}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Calculation**")
            st.latex(r"Re = \frac{\rho V D}{\mu}")
            st.latex(rf"Re = \frac{{({rho:.4g})({V:.4g})({D:.4g})}}{{{mu:.4g}}} = {Re:.4g}")
            st.caption("For internal flow in a circular pipe, common guide ranges are Re < 2,300 (laminar), 2,300–4,000 (transitional), and Re > 4,000 (turbulent).")
    except ValueError as e:
        with result_area:
            st.error(str(e))
else:
    with result_area:
        st.markdown("""
        <div class="rc-result">
          <div class="section-title" style="margin-top:0">REYNOLDS NUMBER</div>
          <div style="font-family:'DM Mono',monospace;font-size:2rem;color:#94a3b8">— — —</div>
          <div class="rc-note">Enter your values and select Calculate to view the result.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Formula**")
        st.latex(r"Re = \frac{\rho V D}{\mu}")
        st.caption("ρ = fluid density · V = average flow velocity · D = pipe diameter · μ = dynamic viscosity")

st.divider()
st.caption("RCulator • Initial functional build • Verify fluid-property data and flow-regime criteria against your course reference before using results in submitted work.")
