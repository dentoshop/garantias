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
RANGE_NAME_GET="Fill!A:V"


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
maxrow=df_index[-1]+3

RANGE_NAME_FILL=f"Fill!A{maxrow}"

def llenar(valores,rangea):
    filling = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=rangea,
        valueInputOption='USER_ENTERED',
        body={'values': [valores]}
    )
    return filling.execute()


empp, clien = st.tabs(["Empresa","Seguimiento - Cliente"])

with clien:
    st.write("")
with empp:
    passw=st.text_input("Contraseña:",type="password")

    if passw==st.secrets["password"]:
        tab1, tab2 = st.tabs(["Llenado", "Modificar"])

        with tab1:

            id=int(df_fix.iloc[maxrow-3,0])+1
            st.subheader(f"ID: {id}",)


            col1, col2 = st.columns(2)

            with col1:
                
                fecha_ing=st.date_input("Fecha",format="DD/MM/YYYY")
                fecha_ing1=pd.to_datetime(fecha_ing)

                Dni=st.text_input("DNI")

                Nom_emp=st.text_input("Empresa")

                Num=st.text_input("Número de celular")

                Num_sn=st.text_input("Numero de Serie")
                
                Accesorios=st.text_input("Accesorios")

                Obs=st.text_input("Observaciones") 

                

            with col2:
                
                Nombres=st.text_input("Nombres")

                Apellidos=st.text_input("Apellidos")

                Nom_Apell= Nombres+", "+Apellidos

                Ruc=st.text_input("RUC")

                Email=st.text_input("Email")

                Nom_Equip=st.text_input("Nombre del Equipo")

                Motivo=st.text_input("Motivo de Ingreso")

                Garantia=st.selectbox("¿Tiene garantía?",["Si","No"])

                if Garantia=="Si":
                    monto_pago=0
                elif Garantia=="No":

                    with col1:
                        monto_pago=st.number_input("Costo de la evaluacion",step=0.01)

            

            valores=[id,fecha_ing1.strftime("%d/%m/%Y"),Nom_Apell,Dni,Ruc,Num,Email,Num_sn,Nom_Equip,Accesorios,Obs,Motivo,Garantia,monto_pago,"Recepcion",0,"No","No Entregado","","","",""]
            
            boton_fill=st.button("Llenar", on_click=llenar, args=(valores,RANGE_NAME_FILL,))


            on = st.toggle('Mostrar ultimos 10 ingresos')

            if on:
            
                st.table(df_fix[-10:])



        with tab2:
            num_sn_buscar=st.selectbox("Ingresar número de serie",df_fix["NUM_SN"])

            id_buscar=st.selectbox("Selecciona el ID",df_fix[df_fix['NUM_SN'] == num_sn_buscar]["ID"])   
            row_mod=df_fix[df_fix['ID'] == id_buscar].index[0]

            
            valores_mod=df_fix[(df_fix['ID'] == str(row_mod)) & (df_fix['NUM_SN'] == num_sn_buscar)].iloc[0].values.tolist()
            valores_mod2=copy(valores_mod)
  
            st.write(f"Nombre:  {valores_mod[2]}")
            st.write(f"DNI:  {valores_mod[3]}")
            st.write(f"RUC:  {valores_mod[4]}")
            st.write(f"Número:  {valores_mod[5]}")
            st.write(f"Email:  {valores_mod[6]}")
            st.write(f"Nombre del Equipo:  {valores_mod[8]}")
            st.write(f"Observaciones:  {valores_mod[10]}")
            st.write(f"Motivo:  {valores_mod[11]}")
            st.write(f"Garantia:  {valores_mod[12]}")


            try:
                estado_mod=st.selectbox("Estado",['Recepcion','Evaluacion','Reparacion','Listo para Entrega','Entregado'],placeholder=valores_mod[14])
            except Exception:
                estado_mod=st.selectbox("Estado",['Recepcion','Evaluacion','Reparacion','Listo para Entrega','Entregado'],placeholder="")
            
            fecha_mod=st.date_input("Fecha de Modificacion",format="DD/MM/YYYY")
            fecha_mod=pd.to_datetime(fecha_mod).strftime("%d/%m/%Y")

            if valores_mod[12] == "No":
                
                costo_reparacion=st.number_input('Costo de la reparacion')

            else:

                costo_reparacion=0

            devo=st.selectbox("¿Habra devolucion?",['Si','No'])
            result=st.selectbox("Entrega",['Entregado','No Entregado'])
            

            
            if estado_mod == 'Recepcion':
                valores_mod2[18]=valores_mod[18]
                valores_mod2[19]=valores_mod[19]
                valores_mod2[20]=valores_mod[20]
                valores_mod2[21]=valores_mod[21]
            if estado_mod == 'Evaluacion':
                valores_mod2[18]=fecha_mod
                valores_mod2[19]=valores_mod[19]
                valores_mod2[20]=valores_mod[20]
                valores_mod2[21]=valores_mod[21]
            elif estado_mod == 'Reparacion':
                valores_mod2[18]=valores_mod[18]
                valores_mod2[19]=fecha_mod
                valores_mod2[20]=valores_mod[20]
                valores_mod2[21]=valores_mod[21]
            elif estado_mod == 'Listo para Entrega':
                valores_mod2[18]=valores_mod[18]
                valores_mod2[19]=valores_mod[19]
                valores_mod2[20]=fecha_mod
                valores_mod2[21]=valores_mod[21]
            elif estado_mod == 'Entregado':
                valores_mod2[18]=valores_mod[18]
                valores_mod2[19]=valores_mod[19]
                valores_mod2[20]=valores_mod[20]
                valores_mod2[21]=fecha_mod

            valores_mod2[14]=estado_mod
            valores_mod2[15]=costo_reparacion
            valores_mod2[16]=devo
            valores_mod2[17]=result


            RANGE_NAME_MOD=f"Fill!A{row_mod+2}"

            boton_mod=st.button("Modificar", on_click=llenar, args=(valores_mod2,RANGE_NAME_MOD,))

            a=df_fix.iloc[row_mod]
            a.replace(to_replace=['null',None], value='', inplace=True)
            st.table(a)

    else: "Contraseña incorrecta"
            


