import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pub Scheduler", layout="wide")

# Header image
_, c, _ = st.columns([1,2,1])
with c:
    st.image("img1.jpg", width=380)

# Storage
if "availability" not in st.session_state:
    st.session_state.availability = pd.DataFrame(
        columns=["Name","Email","Tshirt","Day","Shift"]
    )

# Shift schedule
shift_map = {
    d: ["3:45–8:00", "8:00–12:15"] for d in
    ["Monday","Tuesday","Wednesday","Thursday","Saturday"]
}
shift_map["Friday"] = ["3:45–8:30", "8:30–1:15"]

# Sidebar
page = st.sidebar.radio("Menu", ["Submit Availability","Calendar View"])

# -------------------------
# Submit Availability
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
            df = st.session_state.availability
            df = df[df.Email != email]
            for d, s in selected:
                df.loc[len(df)] = [name, email, tshirt, d, s]
            st.session_state.availability = df
            st.success("Saved!")

# -------------------------
# Calendar View
# -------------------------
else:
    st.title("Availability Calendar")

    df = st.session_state.availability
    if df.empty:
        st.info("No availability yet.")
    else:
        st.dataframe(
            df.pivot_table(index="Shift", columns="Day",
                           values="Name",
                           aggfunc=lambda x: ", ".join(x)),
            use_container_width=True
        )

        st.subheader("T-Shirt Sizes")
        st.dataframe(
            df[["Name","Email","Tshirt"]].drop_duplicates(),
            use_container_width=True
        )

st.markdown("---")
st.caption("Made by ankitdixit@uchicago.edu")
