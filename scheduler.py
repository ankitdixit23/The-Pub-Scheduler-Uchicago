import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Pub Scheduler", layout="wide")

# -------------------------
# GOOGLE SHEETS CONNECTION
# -------------------------
@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_dict = st.secrets["gcp_service_account"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, scope
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(
        "1xOjW0SiEzDZzBjJy2qc0GxXlhd9RrE7ynSdqaYSMdWQ"
    ).sheet1

    return sheet


def read_sheet():
    sheet = connect_sheet()
    data = sheet.get_all_records()

    if not data:
        return pd.DataFrame(
            columns=["Name", "Email", "Tshirt", "Day", "Shift"]
        )

    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip()
    return df


# -------------------------
# HEADER
# -------------------------
_, c, _ = st.columns([1, 2, 1])
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

page = st.sidebar.radio(
    "Menu",
    ["Submit Availability", "Calendar View", "My Schedule", "Admin"]
)

# -------------------------
# SUBMIT AVAILABILITY
# -------------------------
if page == "Submit Availability":
    st.title("Pub Attendant Availability")

    left, right = st.columns([3, 1])

    with left:
        name = st.text_input("Full Name")
        email = st.text_input("UChicago Email")
        tshirt = st.selectbox("T-Shirt Size", ["XS", "S", "M", "L", "XL", "XXL"])

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
        df = read_sheet()

        if not name:
            st.error("Enter name")
        elif "@uchicago.edu" not in email:
            st.error("Use UChicago email")
        elif email in df["Email"].values:
            st.error("You already submitted availability.")
        elif len(selected) == 0 or len(selected) > 4:
            st.error("Select 1–4 shifts")
        else:
            sheet = connect_sheet()

            for d, s in selected:
                sheet.append_row([name, email, tshirt, d, s])

            st.success("Availability saved!")

# -------------------------
# CALENDAR VIEW
# -------------------------
elif page == "Calendar View":
    st.title("Availability Calendar")

    df = read_sheet()

    if df.empty:
        st.info("No availability yet.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total attendants", df["Email"].nunique())
        col2.metric("Total shift selections", len(df))
        col3.metric("Days covered", df["Day"].nunique())

        calendar = df.pivot_table(
            index="Shift",
            columns="Day",
            values="Name",
            aggfunc=lambda x: ", ".join(x),
        )

        st.dataframe(calendar, use_container_width=True)

        st.subheader("T-Shirt Sizes")
        st.dataframe(
            df[["Name", "Email", "Tshirt"]].drop_duplicates(),
            use_container_width=True,
        )

# -------------------------
# MY SCHEDULE
# -------------------------
elif page == "My Schedule":
    st.title("My Schedule")

    email_lookup = st.text_input("Enter your UChicago email")

    if email_lookup:
        df = read_sheet()
        user_df = df[df["Email"] == email_lookup]

        if user_df.empty:
            st.info("No shifts found.")
        else:
            st.dataframe(user_df[["Day", "Shift"]])

# -------------------------
# ADMIN PAGE
# -------------------------
elif page == "Admin":
    st.title("Admin Panel")

    password = st.text_input("Admin password", type="password")

    if password == st.secrets["admin_password"]:
        df = read_sheet()
        st.dataframe(df, use_container_width=True)

        if st.button("Reset Quarter"):
            sheet = connect_sheet()
            sheet.resize(rows=1)  # keeps header row
            st.success("Quarter reset — headers preserved.")
    else:
        st.info("Enter admin password to continue.")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("Made by ankitdixit@uchicago.edu")
