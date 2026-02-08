import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Pub Scheduler", layout="wide")

# -------------------------
# GOOGLE SHEETS STORAGE
# -------------------------
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("Pub Scheduler Winter 2026").sheet1
    return sheet

def read_sheet():
    sheet = connect_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# -------------------------
# HEADER
# -------------------------
_, c, _ = st.columns([1,2,1])
with c:
    st.image("img1.jpg", width=380)

# -------------------------
# SHIFT MAP
# -------------------------
shift_map = {
    "Monday": ["3:45–8:00", "8:00–12:15"],
    "Tuesday": ["3:45–8:00", "8:00–12:15"],
    "Wednesday": ["3:45–8:00", "8:00–12:15"],
    "Thursday": ["3:45–8:00", "8:00–12:15"],
    "Friday": ["3:45–8:30", "8:30–1:15"],
    "Saturday": ["3:45–8:00", "8:00–12:15"],
}

page = st.sidebar.radio("Menu", ["Submit Availability","Calendar View"])

# -------------------------
# SUBMIT PAGE
# -------------------------
if page == "Submit Availability":
    st.title("Pub Attendant Availability")

    left, right = st.columns([3,1])

    with left:
        name = st.text_input("Full Name")
        email = st.text_input("UChicago Email")
        tshirt = st.selectbox("T-Shirt Size", ["XS","S","M","L","XL","XXL"])

    with right:
        st.image("img2.jpg", width=150)

    selected = []
    st.subheader("Weekly Shift Selection")

    cols = st.columns(6)
    for col, (day, shifts) in zip(cols, shift_map.items()):
        with col:
            st.markdown(f"**{day}**")
            for s in shifts:
                if st.checkbox(s, key=f"{day}{s}"):
                    selected.append((day, s))

    if st.button("Submit"):
        if not name:
            st.error("Enter name")
        elif "@uchicago.edu" not in email:
            st.error("Use UChicago email")
        elif len(selected) == 0 or len(selected) > 4:
            st.error("Select 1–4 shifts")
        else:
            sheet = connect_sheet()

            for d, s in selected:
                sheet.append_row([name, email, tshirt, d, s])

            st.success("Availability saved permanently!")

# -------------------------
# CALENDAR VIEW
# -------------------------
else:
    st.title("Availability Calendar")

    df = read_sheet()

    if df.empty:
        st.info("No availability yet.")
    else:
        calendar = df.pivot_table(
            index="Shift",
            columns="Day",
            values="Name",
            aggfunc=lambda x: ", ".join(x),
        )

        st.dataframe(calendar, width="stretch")

        st.subheader("T-Shirt Sizes")
        st.dataframe(
            df[["Name","Email","Tshirt"]].drop_duplicates(),
            width="stretch"
        )

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("Made by ankitdixit@uchicago.edu")
