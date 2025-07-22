# realtime_dashboard.py

import streamlit as st
import pandas as pd
import time
import os

# ✅ Use relative path for deployment
LOG_PATH = 'logs/predictions_log.csv'

st.set_page_config(page_title="Real-Time Fraud Detection", layout="wide")
st.title("🚨 Real-Time Fraud Detection Dashboard")

# Initialize session state to track the last row seen
if "last_index" not in st.session_state:
    st.session_state.last_index = -1

placeholder = st.empty()

while True:
    if os.path.exists(LOG_PATH):
        try:
            df = pd.read_csv(LOG_PATH)

            # Skip if file is still empty (no headers or no data)
            if df.empty or len(df.columns) == 0:
                with placeholder.container():
                    st.warning("⏳ Log file is empty. Waiting for predictions...")
                time.sleep(2)
                continue

            # Show only new rows
            new_rows = df[st.session_state.last_index + 1:]

            if not new_rows.empty:
                with placeholder.container():
                    st.success("✅ New Predictions Received:")
                    st.dataframe(new_rows, use_container_width=True)
                st.session_state.last_index = new_rows.index[-1]
            else:
                with placeholder.container():
                    st.info("⏳ Waiting for new predictions...")

        except pd.errors.EmptyDataError:
            with placeholder.container():
                st.warning("⚠️ Log file exists but is completely empty.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

    else:
        with placeholder.container():
            st.warning("📁 Log file not found. Run the simulation to generate predictions.")

    time.sleep(2)
