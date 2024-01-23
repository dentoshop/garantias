import os
from datetime import datetime
import time
import pandas as pd
from copy import copy
from pathlib import Path
import re
import numpy as np
import sys
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account


#----------------------------------------------------------------------

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY ={
    "type": "service_account",
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
    "universe_domain": "googleapis.com"
}

SPREADSHEET_ID = '1E3VWyZKoUdTUBPoZlNmudeGoiXx7uBNFTIzDuHX0iY8'
RANGE_NAME_GET="Fill!A:W"

creds = None
creds = service_account.Credentials.from_service_account_info(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Llamada a la api
result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_GET)
        .execute()
    )
# Extraemos values del resultado
values = result.get('values',[])
st.write(pd.dataframe(values))


