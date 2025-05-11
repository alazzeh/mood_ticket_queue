# 📝 Mood of the Ticket Queue

A quick internal tool to log and visualize the emotional vibe of a support ticket queue throughout the day. Built for operational awareness and team sentiment tracking.

## Features

- 📌 Log mood using emojis (`🎉 😊 😐 😕 😠`)
- 🗒 Optional note field for context
- 📊 Auto-updating bar chart of today's mood counts
- 📅 Date filter to view mood trends historically
- 📈 Daily average and 7-day mood comparison

## Tech Stack

- Python + [Streamlit](https://streamlit.io)
- Google Sheets (as backend database)
- gspread + OAuth2 for integration
- Plotly for charts

## Setup

1. Clone this repo
2. Add your Google service account key to `.streamlit/secrets.toml`:

```toml
[GOOGLE_SERVICE_ACCOUNT_JSON]
# Paste your JSON key here as a multiline string

