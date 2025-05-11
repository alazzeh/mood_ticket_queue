import streamlit as st 
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import math
import plotly.graph_objects as go

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("mood_of_the_ticket_queue").sheet1


## Creating a scoring map for the Mood (Emojis)
mood_score_map = {
    "🎉": 5,
    "😊": 4,
    "😐": 3,
    "😕": 2,
    "😠": 1
}
score_to_emoji = {v: k for k, v in mood_score_map.items()}

# Designing the log

st.title('😊 Ticket Queue Mood Check')
with st.form("mood_logger"):
    mood = st.radio("How does the queue feel?", ["😊", "😠", "😕", "🎉", "😐"])
    st.caption("🎉: joyful | 😊: happy | 😐: neutral | 😕: sad | 😠: frustrated")
    note = st.text_input("Optional note").strip()
    submitted = st.form_submit_button("Log Mood")
    if submitted:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score = mood_score_map[mood]
        sheet.append_row([date_time, mood, note, score])
        st.success(f"✅ Mood '{mood}' logged!")
        
## Loading the data

data = sheet.get_all_records()
df = pd.DataFrame(data)
df['score'] = pd.to_numeric(df['score'], errors='coerce')
df['date_time'] = pd.to_datetime(df['date_time'])
df = df.set_index('date_time')

## Computing today's average and median score (Mood) 

today = pd.Timestamp.now().normalize()
today_avg = df.loc[df.index.normalize() == today, 'score'].mean()
today_avg = today_avg if not pd.isna(today_avg) else 0

today_median = df.loc[df.index.normalize() == today, 'score'].median()
today_median = today_avg if not pd.isna(today_median) else 0

seven_days_ago = pd.Timestamp.now() - pd.Timedelta(days=7)
last_7_days = df[df.index >= seven_days_ago]
rolling_7d_avg = last_7_days['score'].mean()

score = math.ceil(today_avg)
emoji = score_to_emoji.get(score, "❓")






# Vibe Metric & Date Filter + Bar Chart
# ------------------------

a,b = st.columns(2)
with a:
  st.metric("Today's Vibe", f"{round(today_avg, 2)} {'/ 5'} {emoji}", f"{round(today_avg - rolling_7d_avg, 2)} vs 7d avg")
with b:
    selected_date = st.date_input("Filter by date", pd.Timestamp.now().date())
    filtered_df = df[df.index.normalize() == pd.to_datetime(selected_date)]
    filtered_median = filtered_df['score'].median()
    median_emoji = score_to_emoji.get(int(round(filtered_median)), "❓") if not pd.isna(filtered_median) else "❓"
    
    st.write(f"**Overall mood on {selected_date}:** {median_emoji}")

# Mood bar chart based on selected date
mood_counts = filtered_df['score'].map(score_to_emoji).value_counts()
all_moods = ["😠", "😕", "😐", "😊", "🎉"]
mood_counts = mood_counts.reindex(all_moods).fillna(0).astype(int)

chart_data = pd.DataFrame({
    'Mood': mood_counts.index,
    'Count': mood_counts.values
}).set_index('Mood')

st.bar_chart(chart_data)









