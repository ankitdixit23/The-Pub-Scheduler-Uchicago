# Pub Scheduler — UChicago Pub Attendant Scheduling App

A lightweight scheduling app built with **Streamlit + Google Sheets** to collect attendant availability, approve shifts, and publish the final schedule.

Built for **The Pub at the University of Chicago**.

---

## Live App

Launch the scheduler here:

https://the-pub-scheduler-uchicago-tmupxwmkkcq3m3vuondgcr.streamlit.app/

---

## Features

### Attendants
- Submit availability
- Select up to 4 shifts
- One submission per email
- View approved schedule
- Check personal schedule

### Admin
- Password-protected admin panel
- Multi-shift approval workflow
- Dashboard metrics
- Quarterly reset (headers preserved)
- Google Sheets backend

---

## App Workflow

Submit Availability  
→ Google Sheet stores responses  
→ Admin approves shifts  
→ Approved schedule appears in dashboard  
→ Users check "My Schedule"

---

## Google Sheet Format

Header row must be:

Name | Email | Tshirt | Day | Shift | Approved


Example:

Ankit Dixit | ankit@uchicago.edu | M | Monday | 3:45–8:00 | Yes


---

## Project Structure

the-pub-scheduler-uchicago/
│
├── scheduler.py
├── requirements.txt
├── img1.jpg
├── img2.jpg
└── README.md


---

## Run Locally

Install dependencies:

```
pip install -r requirements.txt
Run app:

streamlit run scheduler.py
Deployment
This app is deployed using Streamlit Cloud with Google Sheets as the backend.

Steps:

Push repo to GitHub

Deploy via Streamlit Cloud

Add secrets in app settings

Share Google Sheet with service account

Tech Stack
Streamlit

Pandas

gspread

Google Sheets API

OAuth2 Service Account
```

Author
Ankit Dixit
University of Chicago
MPP Candidate (2026)

License
Internal scheduling tool for The Pub.