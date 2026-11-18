import os
import pandas as pd
import streamlit as st

class DataLogger:
    def __init__(self, filename="study_data.csv"):
        self.filename = filename
        self.fieldnames = [
            "participant_id", "timestamp", "trial_number", "condition",
            "puzzle_type", "complexity", "time_taken", "time_to_hint",
            "correct_answer", "user_answer", "hints_used",
            "has_ai_assistance", "is_hallucinated", "confidence_level",
            "response_correct"
        ]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.fieldnames)
            df.to_csv(self.filename, index=False)

    def log_trial(self, **kwargs):
        try:
            df_new = pd.DataFrame([kwargs])
            df_new.to_csv(self.filename, mode='a', header=not os.path.exists(self.filename), index=False)
        except Exception as e:
            st.warning(f"Local CSV logging warning: {e}")

        try:
            from streamlit_gsheets import GSheetsConnection
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_df = conn.read(ttl=0)
            updated_df = pd.concat(
                [existing_df, pd.DataFrame([kwargs])],
                ignore_index=True
            )
            conn.update(data=updated_df)

        except Exception as cloud_err:
            st.error(f"Google Sheets connection failed: {cloud_err}")

    def get_all_data(self):
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        return pd.DataFrame(columns=self.fieldnames)
