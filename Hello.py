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

st.title("a")
#----------------------------------------------------------------------

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY ={
    "type": "service_account",
    "project_id": "dentoshoppostventa",
    "private_key_id": "a9b4fde133b51028ebd7f7e679e6013949af807f",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCI88iEU6wflloE\no5YScgqgp00mb1bs8mgFrOrfSQwIz7gLElv6iWZ9yCrfpFTgsWSU/CVz15U5HBzy\npxz0sBNaXz5FHclMpBqsl2RjliJgmVnMavZHUJ3kmqQwBHWJnPe6Sx9dfYqk4bOR\n8rvEuHK2E+GYo2dftcTM6R6B8zGSI7f+GWVgUhZHRRqk636/0VupsIg+KnvIeHVn\nO/P4W5+rTqkUJ0z2CxQYJ78yJ0328E1gJZkelW1aolNPmQ/H0u1y6mVw7CFHI3rD\nTGjM4FY/n9V1Rzz5ESr2A0hGFbixc2Spa3RHMEVyj1n/jew3MgnZMD6KZFM9T/WL\nvvn+eVfDAgMBAAECggEAAIV5EnPlGFuwrQrYY+qWOsVYSFitKorDtZ3SaRY0mwX7\na+NegUYrozfzXdWY0yApw11wYRAFi+mc/JmBRTc0Y6gwKwAxh36qcVTEN5LXP6nl\nyx7vIBdg+oFSNbKWpfb4hHeLv4XeVMFdNyWG7HlNSn8p4TRiDN26yZLroFAGNMm3\nmRmEeO5geiy7mm1Ut7J3Zws/NkKIJlo8mzeXgATDzMk5kyQ9rIzNcAREGeEV2bWG\nLiC0Nfvk+NuA01kharsQaBgSu32jvvDkByeXf8XJszRp8tdJSEBCFdSNaq6UMQh0\ntFlNzueXcf3adjueZ1Pq6i1QpO5LbJ6Pgb5viQECXQKBgQC9i9Pec4wI71lPF77p\nFBPXNt9gPdrPTmNAzOmJQQxBvTd0WnG4+iSKFZuIvZnC9A0fO1YJyPGrsEzTMyK0\nveuVgusFvJ4EEOUwHLeXF/nimmCNkpTYsPwBX4SKSKI1XwgRClCqPgLLZyB+82fp\npmzgkVhmuRPT3zzIXXVweObtbQKBgQC494oy12GXzrpCaNEeG2QmCoT3Qbp5zlXj\nl420eoBKYgJQkNs32pP0ZFOotgdoViBYDltEwMELSF8PZd69rprC/2i4570yrSAO\nESr6X/TYNMcTS6BPNZKCQCpaOPd9kFgZ2ZS6bli5kxQZCPzT71mwn1W3wfyCiKvt\nxCZddqYL7wKBgArt/CqQmRuOyaSQ5vZDrR000c6X4n0ftQNwjWrXsGA+C+uOp44W\nBnNb6ZsJ68rdDcCmSEDKMH1I7jUjdrXbWbFGWkz7YlUzsDOFBGUXAda6NiUTtbeF\nBRMDMf5TT98p+qoY4Svf5YNbD/miCXTkntSYLPPHakhGUBfxo6r3ncFFAoGALUAZ\n5iA89ueTN6Xu6t+mm4vdRaQl26C38GrmNu31Lr1VdaJKjxqBMbvNn6uQmlzfoss4\nVtSVJY55+wlf+aWapPPZCctfxOMHwYk/q2sIOlCHF1hcCqS/h+/srI/dNDG46/IH\n6agPOq8Zrpo9SBf5KDWCwebKQKDw9sUS4bCiJK8CgYAp55qLNDTIK0zUmFfcTXEo\nw/C9qlh+wGKHRHcGlPrkxcwLf7RtyTDsE7JTzJKJz4dHbxf0wlbW4Jf9SW4QB5ci\nLule3G9v3Rb3MDgWXIKhy9s0r0Dy+/4ZsVHE7MRNqdbwGcinseSct7SLA4o1dI8r\nnxqmc7yWPGi2HwDJikBc9Q==\n-----END PRIVATE KEY-----\n",
    "client_email": "dentoshop-postventa@dentoshoppostventa.iam.gserviceaccount.com",
    "client_id": "106616072052974732776",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dentoshop-postventa%40dentoshoppostventa.iam.gserviceaccount.com",
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
print(values)

