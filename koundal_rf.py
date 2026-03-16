import streamlit as st

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="Koundal RF Audit Engine", layout="wide")

st.title("📡 Koundal Global Wireless RF Audit Engine")
st.write("Lead Engineer: **Amit Koundal** | GSM • LTE • NR Diagnostic Suite")
st.divider()

# -----------------------------
# KPI EVALUATION FUNCTIONS
# -----------------------------

def evaluate_rsrp(val):
    if val >= -80:
        return "🟢 Excellent", 100
    elif val >= -90:
        return "🟢 Good", 80
    elif val >= -100:
        return "🟡 Fair", 60
    elif val >= -110:
        return "🟠 Poor", 40
    else:
        return "🔴 Very Poor", 20


def evaluate_rsrq(val):
    if val >= -10:
        return "🟢 Good", 100
    elif val >= -15:
        return "🟡 Fair", 60
    else:
        return "🔴 Poor", 30


def evaluate_sinr(val):
    if val >= 20:
        return "🟢 Excellent", 100
    elif val >= 13:
        return "🟢 Good", 80
    elif val >= 0:
        return "🟡 Fair", 60
    else:
        return "🔴 Poor", 20


def evaluate_rxlev(val):
    if val >= -65:
        return "🟢 Excellent", 100
    elif val >= -75:
        return "🟢 Good", 80
    elif val >= -85:
        return "🟡 Fair", 60
    else:
        return "🔴 Poor", 30


def evaluate_rxqual(val):
    if val <= 2:
        return "🟢 Good", 100
    elif val <= 4:
        return "🟡 Moderate", 60
    else:
        return "🔴 Poor", 30


# -----------------------------
# SIDEBAR TECHNOLOGY SELECT
# -----------------------------

tech = st.sidebar.radio(
    "Select Network Technology:",
    ["NR (5G)", "LTE (4G)", "GSM (2G)"]
)

# -----------------------------
# 5G NR SECTION
# -----------------------------

if tech == "NR (5G)":

    st.header("5G NR Serving Cell Audit")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Frequency Info")

        band = st.text_input("NR Band", "n78")
        arfcn = st.number_input("NR ARFCN", value=627312)
        gscn = st.number_input("GSCN", value=7711)

    with c2:
        st.subheader("Signal KPIs")

        rsrp = st.number_input("SS-RSRP (dBm)", value=-100.0)
        rsrq = st.number_input("SS-RSRQ (dB)", value=-12.0)
        sinr = st.number_input("SS-SINR (dB)", value=10.0)

    with c3:
        st.subheader("Beam Info")

        beam = st.text_input("Serving Beam", "Beam_01")
        pci = st.number_input("NR PCI", value=320)

    st.divider()

    # KPI Evaluation
    rsrp_q, rsrp_score = evaluate_rsrp(rsrp)
    rsrq_q, rsrq_score = evaluate_rsrq(rsrq)
    sinr_q, sinr_score = evaluate_sinr(sinr)

    st.subheader("📊 KPI Evaluation")

    k1, k2, k3 = st.columns(3)

    k1.metric("RSRP Quality", rsrp_q)
    k2.metric("RSRQ Quality", rsrq_q)
    k3.metric("SINR Quality", sinr_q)

    health = (rsrp_score + rsrq_score + sinr_score) / 3

    st.subheader("📡 RF Health Score")
    st.progress(int(health))
    st.write("RF Health Score:", round(health, 1), "/ 100")

    # Diagnostic Engine
    st.subheader("🧠 AI RF Diagnosis")

    if rsrp < -105:
        st.error("Cell Edge Coverage Detected")

    if sinr < 3:
        st.error("High Interference Detected")

    if rsrq < -15:
        st.warning("Network Load or Interference")

    if health > 80:
        st.success("Cell Performance Excellent")

# -----------------------------
# LTE SECTION
# -----------------------------

elif tech == "LTE (4G)":

    st.header("LTE Serving Cell Audit")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Cell Identity")

        band = st.text_input("LTE Band", "Band 3")
        earfcn = st.number_input("EARFCN DL", value=1300)
        pci = st.number_input("PCI", value=124)

    with c2:
        st.subheader("Network Info")

        tac = st.number_input("TAC", value=4501)
        bandwidth = st.selectbox("Bandwidth MHz", [5,10,15,20])

    with c3:
        st.subheader("Radio KPIs")

        rsrp = st.number_input("RSRP dBm", value=-95.0)
        rsrq = st.number_input("RSRQ dB", value=-11.0)
        sinr = st.number_input("SINR dB", value=10.0)

    st.divider()

    rsrp_q, rsrp_score = evaluate_rsrp(rsrp)
    rsrq_q, rsrq_score = evaluate_rsrq(rsrq)
    sinr_q, sinr_score = evaluate_sinr(sinr)

    st.subheader("📊 KPI Evaluation")

    k1, k2, k3 = st.columns(3)

    k1.metric("RSRP", rsrp_q)
    k2.metric("RSRQ", rsrq_q)
    k3.metric("SINR", sinr_q)

    health = (rsrp_score + rsrq_score + sinr_score) / 3

    st.subheader("📡 RF Health Score")

    st.progress(int(health))
    st.write("RF Health Score:", round(health,1), "/100")

    st.subheader("🧠 Expert Diagnosis")

    if rsrp < -105 and sinr < 3:
        st.error("Cell Edge + Interference")

    if rsrq < -15:
        st.warning("High PRB Load or Neighbor Interference")

    if sinr < 0:
        st.error("Severe Interference (Possible PIM)")

    if health > 80:
        st.success("Cell Performance Healthy")

# -----------------------------
# GSM SECTION
# -----------------------------

elif tech == "GSM (2G)":

    st.header("GSM Legacy RF Audit")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("Frequency")

        arfcn = st.number_input("BCCH ARFCN", value=62)
        bsic = st.number_input("BSIC", value=34)

    with c2:
        st.subheader("Cell Identity")

        lac = st.number_input("LAC", value=1023)
        cell = st.number_input("Cell ID", value=5521)

    with c3:
        st.subheader("Radio Quality")

        rxlev = st.number_input("RxLev", value=-85.0)
        rxqual = st.slider("RxQual",0,7,2)

    st.divider()

    rxlev_q, lev_score = evaluate_rxlev(rxlev)
    rxqual_q, qual_score = evaluate_rxqual(rxqual)

    st.subheader("📊 KPI Evaluation")

    k1, k2 = st.columns(2)

    k1.metric("Signal Level", rxlev_q)
    k2.metric("Signal Quality", rxqual_q)

    health = (lev_score + qual_score) / 2

    st.subheader("📡 RF Health Score")

    st.progress(int(health))
    st.write("RF Health Score:", round(health,1), "/100")

    st.subheader("🧠 Expert Diagnosis")

    if rxqual > 4:
        st.error("High BER detected")

    if rxlev < -90:
        st.warning("Coverage Weak")

    if health > 80:
        st.success("GSM Cell Healthy")


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.info(
"💡 Amit Koundal Vision: Unified RF KPI baseline across 2G / 4G / 5G networks."
)