import streamlit as st
from streamlit_option_menu import option_menu
import os
from datetime import date
import pandas as pd
from dotenv import load_dotenv
import requests
import plotly.express as px
import psycopg2
from utils.alunos import aba_alunos
from utils.matriculas import aba_matriculas
from utils.relatorios import aba_relatorios
from utils.gestao import aba_gestao
from utils.carteirinha import aba_carteirinha

load_dotenv()  # Carrega as variáveis do .env

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

def get_options(table, column):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT {column} FROM {table} ORDER BY {column}")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ["Selecione..."] + results

import requests

def get_options_api(endpoint):
    try:
        response = requests.get(f"http://localhost:8000/{endpoint}/")
        if response.status_code == 200:
            return ["Selecione..."] + response.json()
        else:
            return ["Selecione..."]
    except Exception:
        return ["Selecione..."]

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,700&display=swap');
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    escolha = option_menu(
        "ViaEducação",
        options=["Matrículas", "Relatórios", "Alunos", "Gestão", "Carteirinha"],
        icons=["file-earmark-text", "bar-chart", "people", "gear", "credit-card-2-front-fill"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#f0f2f5ff",
                "box-shadow": "none",
                "font-family": "'Source Sans Pro', sans-serif"
            },
            "icon": {"color": "#2c3e50"},
            "nav-link": {
                "text-align": "left",
                "margin":"2px",
                "--hover-color": "#eee",
                "background-color": "#f0f2f5ff",
                "font-family": "'Source Sans Pro', sans-serif"
            },
            "nav-link-selected": {
                "background-color": "#f0f2f5ff",
                "color": "#000",
                "font-family": "'Source Sans Pro', sans-serif"
            },
            "menu-title": {
                "color": "#2c3e50",
                "margin-bottom": "10px",
                "background-color": "#f0f2f5ff",
                "font-family": "'Source Sans Pro', sans-serif"
            }
        }
    )
    st.markdown("---")
    st.sidebar.caption("Desenvolvido por Projetos e Inovação")

if escolha == "Matrículas":
    aba_matriculas(get_options_api)
elif escolha == "Alunos":
    aba_alunos()
elif escolha == "Relatórios":
    aba_relatorios()
elif escolha == "Gestão":
    aba_gestao()
elif escolha == "Carteirinha":
    aba_carteirinha()
