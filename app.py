import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Cadence",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Sample Behaviour Profiles
# -----------------------------
users = {
    "User 1": {
        "hours": [8,9,10,14,15,18,19,20],
        "devices": ["iPhone","Desktop"],
        "locations": ["Mumbai","Delhi"]
    },
    "User 2": {
        "hours": [7,8,12,13,19,20,21],
        "devices": ["Android","Laptop"],
        "locations": ["Bangalore","Hyderabad"]
    },
    "User 3": {
        "hours": [6,7,11,12,17,18,22,23],
        "devices": ["iPad","Windows PC"],
        "locations": ["Pune","Singapore"]
    }
}

# -----------------------------
# Risk Scoring Engine
# -----------------------------
def check(user, hour, device, location, velocity):
    score = 0
    reasons = []
    data = users[user]

    if hour not in data["hours"]:
        score += 30
        reasons.append("⏰ Unusual login time (+30)")

    if device not in data["devices"]:
        score += 25
        reasons.append("📱 New device detected (+25)")

    if location not in data["locations"]:
        score += 25
        reasons.append("📍 Unfamiliar location (+25)")

    if velocity:
        score += 20
        reasons.append("⚡ Impossible travel detected (+20)")

    if score < 30:
        return score, "✅ ALLOW", "Low Risk", reasons
    elif score < 70:
        return score, "⚠️ CHALLENGE", "Medium Risk", reasons
    else:
        return score, "❌ BLOCK", "High Risk", reasons

# -----------------------------
# Header
# -----------------------------
st.title("🛡️ Cadence")
st.caption("Powered by Behavioral Trust Validator™")

st.write(
    "Continuous behavioral intelligence for fraud prevention. "
    "This MVP demonstrates how behavioral signals can be used to evaluate "
    "session trust and detect suspicious login attempts."
)

# -----------------------------
# Sidebar
# -----------------------------
mode = st.sidebar.radio(
    "Navigation",
    [
        "🧪 Demo Scenarios",
        "🔍 Custom Login Test",
        "📘 About Cadence"
    ]
)

# -----------------------------
# Demo Mode
# -----------------------------
if mode == "🧪 Demo Scenarios":

    st.subheader("Demo Scenarios")

    demo = st.selectbox(
        "Select a login attempt",
        [
            "Normal Login",
            "Suspicious Login",
            "High Risk Login"
        ]
    )

    if demo == "Normal Login":
        user, hour, device, location, velocity = "User 1", 9, "iPhone", "Mumbai", False

    elif demo == "Suspicious Login":
        user, hour, device, location, velocity = "User 2", 3, "Tablet", "Bangalore", False

    else:
        user, hour, device, location, velocity = "User 3", 2, "Unknown Device", "London", True

    score, action, level, reasons = check(
        user,
        hour,
        device,
        location,
        velocity
    )

    st.info("Login Session Details")

    c1, c2 = st.columns(2)

    with c1:
        st.write("**User:**", user)
        st.write("**Login Time:**", f"{hour}:00")
        st.write("**Device:**", device)

    with c2:
        st.write("**Location:**", location)
        st.write(
            "**Timestamp:**",
            datetime.now().strftime("%d-%m-%Y %H:%M")
        )

    st.divider()

    m1, m2, m3 = st.columns(3)

    m1.metric("Trust Risk Score", f"{score}/100")
    m2.metric("Risk Level", level)
    m3.metric("Recommended Action", action)

    if reasons:
        st.warning("Behavioral anomalies detected")

        for r in reasons:
            st.write("-", r)

    else:
        st.success(
            "Behavior matches the user's trusted profile."
        )

# -----------------------------
# Custom Test
# -----------------------------
elif mode == "🔍 Custom Login Test":

    st.subheader("Simulate Your Own Login Scenario")

    user = st.selectbox(
        "Select User",
        list(users.keys())
    )

    hour = st.slider(
        "Login Hour",
        0,
        23,
        10
    )

    device = st.text_input(
        "Device",
        "iPhone"
    )

    location = st.text_input(
        "Location",
        "Mumbai"
    )

    velocity = st.checkbox(
        "Impossible travel detected?"
    )

    if st.button("Analyze Session"):

        score, action, level, reasons = check(
            user,
            hour,
            device,
            location,
            velocity
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Trust Risk Score",
            f"{score}/100"
        )

        c2.metric(
            "Risk Level",
            level
        )

        c3.metric(
            "Recommended Action",
            action
        )

        if reasons:

            st.warning(
                "Behavioral anomalies detected:"
            )

            for r in reasons:
                st.write("-", r)

        else:

            st.success(
                "No unusual behavioral signals detected."
            )

# -----------------------------
# About
# -----------------------------
else:

    st.subheader("About Cadence")

    st.info(
        "Cadence is an AI-powered behavioral intelligence platform that "
        "continuously evaluates user behavior during a digital session "
        "to generate a dynamic Trust Score."
    )

    st.markdown("""
### Behavioral Signals Monitored

- ⏰ Login Time
- 📱 Device Consistency
- 📍 Location Patterns
- ⚡ Impossible Travel Detection

### Decision Engine

Cadence evaluates these behavioral signals to generate a real-time Trust Risk Score and recommends one of three actions:

- ✅ Allow
- ⚠️ Challenge (Step-up Authentication)
- ❌ Block

Unlike traditional authentication systems that verify users only during login, Cadence continuously evaluates behavioral trust throughout the session.
""")

    st.subheader("Risk Score Model")

    st.table({
        "Behavioral Signal": [
            "Login Time",
            "Device",
            "Location",
            "Impossible Travel"
        ],
        "Maximum Risk Points": [
            30,
            25,
            25,
            20
        ]
    })

    st.success("""
0–29 → Allow

30–69 → Challenge

70–100 → Block
""")

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Cadence MVP • Powered by Behavioral Trust Validator™ • "
    "ThinkForBharat 1.0 – National Open Innovation Ideathon"
)