"""
Google Sheets loader for Real Estate AI.
"""

import pandas as pd
import gspread
from google.colab import auth
from google.auth import default

def load_sheet_as_dataframe(sheet_id: str, worksheet_name: str = None) -> pd.DataFrame:
    # Authenticate user to Google Drive and Sheets
    auth.authenticate_user()
    creds, _ = default()
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)

    worksheet = sheet.worksheet(worksheet_name) if worksheet_name else sheet.sheet1

    data = worksheet.get_all_records()
    return pd.DataFrame(data)
