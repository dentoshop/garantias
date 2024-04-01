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
import random
import plotly.express as px
import plotly.graph_objects as go


st.image("LOGO DENTOSHOP.png", width=100)
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

    
with empp:
    passw=st.text_input("Contraseña:",type="password")

    if passw==st.secrets["password"]:
        tab1, tab2 , tab3 = st.tabs(["Llenado", "Modificar","Dashboard"])

        with tab1:

            #id=int(df_fix.iloc[maxrow-3,0])+1
            def id_gen(list):
                while True:
                    random_number = random.randint(100000, 999999)
                    if random_number not in list:
                        return random_number

            id=int(id_gen(df_fix["ID"]))

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

                #Garantia=st.selectbox("¿Tiene garantía?",["Si","No"])

                monto_pago=st.number_input("Costo de la evaluacion",step=0.01)

            

            valores=[id,fecha_ing1.strftime("%d/%m/%Y"),Nom_Apell,Dni,Ruc,Num,Email,Num_sn,Nom_Equip,Accesorios,Obs,Motivo,"",monto_pago,"Recepcion",0,"No","","","","","",'']
            #valores=[id,fecha_ing1.strftime("%d/%m/%Y"),Nom_Apell,Dni,Ruc,Num,Email,Num_sn,Nom_Equip,Accesorios,Obs,Motivo,Garantia,monto_pago,"Recepcion",0,"No","","","","",""]
            
            boton_fill=st.button("Llenar", on_click=llenar, args=(valores,RANGE_NAME_FILL,))

            on = st.toggle('Mostrar ultimos 10 ingresos')

            if on:
                
                showli=copy(df_fix)
                showli.replace(to_replace=['null',None], value='', inplace=True)
                st.dataframe(showli[-10:],hide_index=True)



        with tab2:
            #num_sn_buscar=st.selectbox("Ingresar número de serie",df_fix["NUM_SN"].drop_duplicates())

            id_buscar=st.selectbox("Selecciona el ID",df_fix["ID"].drop_duplicates())   
            row_mod=df_fix[df_fix['ID'] == id_buscar].index[0]

            
            valores_mod=df_fix[df_fix['ID'] == id_buscar].iloc[0].values.tolist()
            valores_mod2=copy(valores_mod)
  
            st.write(f"Nombre:  {valores_mod[2]}")
            st.write(f"DNI:  {valores_mod[3]}")
            st.write(f"RUC:  {valores_mod[4]}")
            st.write(f"Número:  {valores_mod[5]}")
            st.write(f"Email:  {valores_mod[6]}")
            st.write(f"Nombre del Equipo:  {valores_mod[8]}")
            st.write(f"Observaciones:  {valores_mod[10]}")
            st.write(f"Motivo:  {valores_mod[11]}")


        #############################################

            #st.write(f"Garantia:  {valores_mod[12]}")



        #############################################
            lista_estado_mod=['Recepcion','Evaluacion','Falta de repuesto','Reparacion','Listo para Entrega','Entregado']

            try:
                if valores_mod[14] in lista_estado_mod:
                    lista_estado_mod.remove(valores_mod[14])
                    lista_estado_mod=[valores_mod[14]]+lista_estado_mod
            except:
                pass
            
            
            if valores_mod[12]=='Si':
                indx=0
            elif valores_mod[12]=='No':
                indx=1
            else:
                indx=None

            Garantia=st.selectbox("¿Tiene garantía?",["Si","No"],index=indx,placeholder='Escoge una opcion')

            estado_mod=st.selectbox("Estado",lista_estado_mod)

            
            fecha_mod=st.date_input("Fecha de Modificacion",format="DD/MM/YYYY")
            fecha_mod=pd.to_datetime(fecha_mod).strftime("%d/%m/%Y")


            
            lista_devo=['No','Si']

            try:
                if valores_mod[16] in lista_devo:
                    lista_devo.remove(valores_mod[16])
                    lista_devo=[valores_mod[16]]+lista_devo
            except:
                pass


            diag=st.text_input("Ingresar diagnostico",value=valores_mod[21])
            valores_mod2[21]=diag


            monto_pago_mod=st.number_input("Costo de la evaluacion",step=0.01,value=float(valores_mod[13] or 0.00))

            costo_reparacion=st.number_input('Costo de la reparacion',step=0.01,value=float(valores_mod[15] or 0.00))


            devo=st.selectbox("¿Pidio devolucion?",lista_devo)
                      

            
            if estado_mod == 'Recepcion':
                valores_mod2[17] = valores_mod[17]
                valores_mod2[18] = valores_mod[18]
                valores_mod2[19] = valores_mod[19]
                valores_mod2[20] = valores_mod[20]
                valores_mod2[22] = valores_mod[22]
            elif estado_mod == 'Evaluacion':
                valores_mod2[17] = fecha_mod
                valores_mod2[18] = valores_mod[18]
                valores_mod2[19] = valores_mod[19]
                valores_mod2[20] = valores_mod[20]
                valores_mod2[22] = valores_mod[22]
            elif estado_mod=='Falta de repuesto':
                valores_mod2[17] = valores_mod[17]
                valores_mod2[18] = valores_mod[18]
                valores_mod2[19] = valores_mod[19]
                valores_mod2[20] = valores_mod[20]
                valores_mod2[22] = fecha_mod
            elif estado_mod == 'Reparacion':
                valores_mod2[17] = valores_mod[17]
                valores_mod2[18] = fecha_mod
                valores_mod2[19] = valores_mod[19]
                valores_mod2[20] = valores_mod[20]
                valores_mod2[22] = valores_mod[22]
            elif estado_mod == 'Listo para Entrega':
                valores_mod2[17] = valores_mod[17]
                valores_mod2[18] = valores_mod[18]
                valores_mod2[19] = fecha_mod
                valores_mod2[20] = valores_mod[20]
                valores_mod2[22] = valores_mod[22]
            elif estado_mod == 'Entregado':
                valores_mod2[17] = valores_mod[17]
                valores_mod2[18] = valores_mod[18]
                valores_mod2[19] = valores_mod[19]
                valores_mod2[20] = fecha_mod
                valores_mod2[22] = valores_mod[22]



            valores_mod2[14]=estado_mod
            valores_mod2[13]=monto_pago_mod
            valores_mod2[15]=costo_reparacion
            valores_mod2[16]=devo
            
            valores_mod2[12]=Garantia


            RANGE_NAME_MOD=f"Fill!A{row_mod+2}"

            #boton_mod=st.button("Modificar", on_click=llenar, args=(valores_mod2,RANGE_NAME_MOD,))

            if st.button('Modificar'):
                
                llenar(valores_mod2,RANGE_NAME_MOD)
                st.rerun()
            




            a=df_fix.iloc[row_mod]
            a=pd.DataFrame(a)
            a.replace(to_replace=['null',None], value='', inplace=True)
            a.columns=[""]
            a_last=a.iloc[-1]
            a=a.drop(a.index[-1])
            a=pd.concat([a.iloc[:16], pd.DataFrame([a_last]), a.iloc[16:]])




            st.dataframe(a,use_container_width=True,height=842)

        with tab3:

            st.link_button('Dashboard','https://app.powerbi.com/view?r=eyJrIjoiNzMyNTNjMTktZGY1OS00MGE1LTlkYjctMTQ1YWYzOTdlNWNlIiwidCI6IjI0Mjk4MDU0LWI1YTYtNGNhMy05OGMyLTlmZDdlY2FjMWJmYSJ9')

    else: 
        st.write("Contraseña incorrecta")
        

    st.divider()
    st.caption('Contacto: franco.valero@pucp.edu.pe | 912085519')

        

with clien:

    
    id_client=st.text_input("Ingresa tu ID")
    try:
        df_client=df_fix[df_fix["ID"] == str(id_client)]
        columns_client={"NOMBRE_CLIENTE":"Nombre","NUM_SN":"Numero de Serie","DIAGNOSTICO":'Diagnostico',"ESTADO":"Estado","FECHA_INGRESO":"Recepcion","FECHA_EVALUACIÓN":"Evaluacion","FECHA_REPUESTO":"Falta de repuesto","FECHA_REPAR":"Reparacion","FECHA_LISTO":"Listo para Entrega","FECHA_ENTREGA":"Entregado"}
        df_client_new=pd.DataFrame(df_client[list(columns_client.keys())])
        df_client_new.rename(columns=columns_client, inplace=True)
        df_client_new.replace(to_replace=['null',None], value='', inplace=True)

        new_rows=["","","",""]


        for i in range(2,8):
                if str(df_client_new.iloc[ 0, i + 2]) != "":
                    new_rows.append("✅")
                else:
                    new_rows.append("")
    
        df_client_new=df_client_new.T
        df_client_new[''] = new_rows
        #df_client_new=df_client_new.T
        #df_client_new=df_client_new.reset_index()
        exclusion=['','null',None]  
        if df_client_new.iloc[df_client_new.index.get_loc("Falta de repuesto"), 1] in exclusion:
            df_client_new.drop(index="Falta de repuesto", inplace=True) 

        st.table(df_client_new)
        

    except:
        st.write("Ingresa un numero valido")





