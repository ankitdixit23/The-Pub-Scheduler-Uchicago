import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pub Attendant Scheduler", layout="wide")

# -----------------------------
# Initialize session storage
# -----------------------------
if "attendants" not in st.session_state:
    st.session_state.attendants = pd.DataFrame(columns=["Name", "Max Hours"])

if "availability" not in st.session_state:
    st.session_state.availability = pd.DataFrame(columns=["Name", "Day"])

if "schedule" not in st.session_state:
    st.session_state.schedule = pd.DataFrame(columns=["Day", "Shift", "Assigned To"])

# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("Pub Scheduler")
page = st.sidebar.radio(
    "Menu",
    ["Attendant Availability", "Manager: Add Attendants", "Manager: Build Schedule", "Schedule Calendar"]
)

# -----------------------------
# Shift definitions
# -----------------------------
shift_options = {
    "Monday": [
        "3:45 PM – 8:00 PM",
        "8:00 PM – 12:15 AM",
    ],
    "Tuesday": [
        "3:45 PM – 8:00 PM",
        "8:00 PM – 12:15 AM",
    ],
    "Wednesday": [
        "3:45 PM – 8:00 PM",
        "8:00 PM – 12:15 AM",
    ],
    "Thursday": [
        "3:45 PM – 8:00 PM",
        "8:00 PM – 12:15 AM",
    ],
    "Friday": [
        "3:45 PM – 8:30 PM",
        "8:30 PM – 1:15 AM",
    ],
    "Saturday": [
        "3:45 PM – 8:00 PM",
        "8:00 PM – 12:15 AM",
    ],
}

# -----------------------------
# Attendant Availability Page
# -----------------------------
if page == "Attendant Availability":
    st.title("Submit Availability")

    if st.session_state.attendants.empty:
        st.info("Manager must add attendants first.")
    else:
        person = st.selectbox("Your Name", st.session_state.attendants["Name"])
        days = list(shift_options.keys())
        available_days = st.multiselect("Select days you can work", days)

        if st.button("Submit Availability"):
            st.session_state.availability = st.session_state.availability[
                st.session_state.availability["Name"] != person
            ]

            for d in available_days:
                new_row = pd.DataFrame([[person, d]], columns=["Name", "Day"])
                st.session_state.availability = pd.concat(
                    [st.session_state.availability, new_row], ignore_index=True
                )

            st.success("Availability updated")

    st.subheader("Current Availability")
    st.dataframe(st.session_state.availability, use_container_width=True)

# -----------------------------
# Manager — Add Attendants
# -----------------------------
if page == "Manager: Add Attendants":
    st.title("Add Pub Attendants")

    name = st.text_input("Attendant Name")
    max_hours = st.number_input("Max Weekly Hours", min_value=1, max_value=40, value=10)

    if st.button("Add Attendant"):
        if name:
            new_row = pd.DataFrame([[name, max_hours]], columns=["Name", "Max Hours"])
            st.session_state.attendants = pd.concat(
                [st.session_state.attendants, new_row], ignore_index=True
            )
            st.success(f"Added {name}")

    st.dataframe(st.session_state.attendants, use_container_width=True)

# -----------------------------
# Manager — Build Schedule
# -----------------------------
if page == "Manager: Build Schedule":
    st.title("Build Weekly Schedule")

    day = st.selectbox("Day", list(shift_options.keys()))
    shift = st.selectbox("Shift", shift_options[day])

    available_people = st.session_state.availability[
        st.session_state.availability["Day"] == day
    ]["Name"].unique()

    if len(available_people) > 0:
        assigned = st.selectbox("Assign Attendant", available_people)

        if st.button("Add Shift"):
            new_row = pd.DataFrame(
                [[day, shift, assigned]],
                columns=["Day", "Shift", "Assigned To"],
            )
            st.session_state.schedule = pd.concat(
                [st.session_state.schedule, new_row], ignore_index=True
            )
            st.success("Shift added")
    else:
        st.warning("No attendants available for this day")

# -----------------------------
# Calendar View
# -----------------------------
if page == "Schedule Calendar":
    st.title("Weekly Schedule Calendar")

    if st.session_state.schedule.empty:
        st.info("No schedule created yet.")
    else:
        calendar_df = st.session_state.schedule.pivot_table(
            index="Shift",
            columns="Day",
            values="Assigned To",
            aggfunc="first",
        )

        st.dataframe(calendar_df, use_container_width=True)

        csv = st.session_state.schedule.to_csv(index=False).encode("utf-8")
        st.download_button("Download Schedule CSV", csv, "schedule.csv", "text/csv")