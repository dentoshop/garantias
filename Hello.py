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

st.title("Dentoshop")
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
df=pd.DataFrame(values[1:], columns=values[0])
df_fix=df[df["ID"] != '']
df_index=df_fix.index
maxrow=df_index[-1]+2

empp, clien = st.tabs(["Empresa","Seguimiento - Cliente"])

with clien:
    st.write("")
with empp:
    passw=st.text_input("Contraseña:",type="password")

    if passw==st.secrets["password"]:
        tab1, tab2, tab3, tab4 = st.tabs(["Llenado", "Modificar", "Status",""])

        with tab1:

            st.subheader(f"ID: {int(df_fix.iloc[maxrow-2,0])+1}",)
            id=int(df_fix.iloc[maxrow-2,0])+1

            col1, col2 = st.columns(2)

            with col1:
                
                fecha_ing=st.date_input("Fecha",format="DD/MM/YYYY")
                fecha_ing1=pd.to_datetime(fecha_ing)

                Dni=st.text_input("DNI")

                Nom_emp=st.text_input("Empresa")

                Num=st.text_input("Número")

                Num_sn=st.text_input("Numero de Serie")
                
                Accesorios=st.text_input("Accesorios")

                Obs=st.text_input("Observaciones") 

                Garantia=st.selectbox("¿Tiene garantía?",["Si","No"]) 

            with col2:
                
                Nombres=st.text_input("Nombres")

                Apellidos=st.text_input("Apellidos") 
                
                Ruc=st.text_input("RUC")

                Email=st.text_input("Email")

                Nom_Equip=st.text_input("Nombre del Equipo")

                Motivo=st.text_input("Motivo de Ingreso")

                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")

                Motivoa=st.text_input("Motivo de Ingraeso")

        with tab2:
            
           st.write("a")   

        with tab3:
            
            st.write("a")  

        with tab4:
            
            st.write("a")  

    else: "Contraseña incorrecta"
            
st.write(df)

