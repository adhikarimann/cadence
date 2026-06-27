
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Behavioral Trust Validator", page_icon="🔐", layout="wide")

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

def check(user, hour, device, location, velocity):
    score = 0
    reasons = []
    data = users[user]

    if hour not in data["hours"]:
        score += 30
        reasons.append("⏰ Login time is unusual (+30)")
    if device not in data["devices"]:
        score += 25
        reasons.append("📱 New device detected (+25)")
    if location not in data["locations"]:
        score += 25
        reasons.append("📍 New location detected (+25)")
    if velocity:
        score += 20
        reasons.append("⚡ Impossible travel detected (+20)")

    if score < 30:
        return score, "✅ ALLOW", "Low Risk", reasons
    elif score < 70:
        return score, "⚠️ CHALLENGE", "Medium Risk", reasons
    return score, "❌ BLOCK", "High Risk", reasons

st.title("🔐 Behavioral Trust Validator")
st.write("Detect suspicious login attempts using simple behavioural analysis.")

mode = st.sidebar.radio(
    "Navigation",
    ["🧪 Demo Scenarios", "🔍 Custom Login Test", "📘 System Overview"]
)

if mode == "🧪 Demo Scenarios":
    st.subheader("Choose a Demo")

    demo = st.selectbox(
        "Select a login attempt",
        ["Normal Login", "Suspicious Login", "High Risk Login"]
    )

    if demo == "Normal Login":
        user, hour, device, location, velocity = "User 1", 9, "iPhone", "Mumbai", False
    elif demo == "Suspicious Login":
        user, hour, device, location, velocity = "User 2", 3, "Tablet", "Bangalore", False
    else:
        user, hour, device, location, velocity = "User 3", 2, "Unknown Device", "London", True

    score, action, level, reasons = check(user, hour, device, location, velocity)

    st.info("Sample login details")

    c1, c2 = st.columns(2)
    with c1:
        st.write("**User:**", user)
        st.write("**Time:**", f"{hour}:00")
        st.write("**Device:**", device)
    with c2:
        st.write("**Location:**", location)
        st.write("**Date & Time:**", datetime.now().strftime("%d-%m-%Y %H:%M"))

    st.divider()

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Score", f"{score}/100")
    m2.metric("Risk Level", level)
    m3.metric("Decision", action)

    if reasons:
        st.warning("Risk factors found:")
        for r in reasons:
            st.write("-", r)
    else:
        st.success("Everything looks normal. Login can be allowed safely.")

elif mode == "🔍 Custom Login Test":
    st.subheader("Test Your Own Login Scenario")
    st.write("Change the details below and see how the risk score changes.")

    user = st.selectbox("Select User", list(users.keys()))
    hour = st.slider("Login Hour", 0, 23, 10)
    device = st.text_input("Device Name", "iPhone")
    location = st.text_input("Location", "Mumbai")
    velocity = st.checkbox("Impossible travel?")

    if st.button("Analyze Login"):
        score, action, level, reasons = check(user, hour, device, location, velocity)

        c1, c2, c3 = st.columns(3)
        c1.metric("Risk Score", f"{score}/100")
        c2.metric("Risk Level", level)
        c3.metric("Decision", action)

        if reasons:
            st.warning("Why was this login flagged?")
            for r in reasons:
                st.write("-", r)
        else:
            st.success("No unusual behaviour detected.")

else:
    st.subheader("How the System Works")

    st.info(
        "The system compares every login attempt with the user's normal behaviour "
        "and gives a risk score."
    )

    st.markdown("""
- ⏰ Checks login time
- 📱 Checks device
- 📍 Checks location
- ⚡ Checks impossible travel
- 📊 Calculates a risk score
- 🔐 Decides whether to Allow, Challenge or Block
""")

    st.subheader("Risk Score")

    st.table({
        "Check": ["Time", "Device", "Location", "Travel"],
        "Maximum Points": [30, 25, 25, 20]
    })

    st.success("""
0 - 29 : Allow

30 - 69 : Challenge (OTP)

70 - 100 : Block
""")

st.divider()
st.caption("PSB Hackathon 2026 • IIT (ISM) Dhanbad")
