import streamlit as st
from datetime import date
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

def format_cpf(cpf):
    digits = ''.join(filter(str.isdigit, cpf))[:11]
    if len(digits) <= 3:
        return digits
    elif len(digits) <= 6:
        return f"{digits[:3]}.{digits[3:]}"
    elif len(digits) <= 9:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
    else:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"

def format_telefone(telefone):
    digits = ''.join(filter(str.isdigit, telefone))[:11]
    if len(digits) <= 2:
        return f"({digits}"
    elif len(digits) <= 7:
        return f"({digits[:2]}) {digits[2:]}"
    elif len(digits) <= 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    else:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:11]}"

def aba_matriculas(get_options_api):
    st.title("📝 Matrículas")
    # --- CADASTRO ---
    st.markdown("#### 👤 Cadastro do Aluno")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do aluno")
        email = st.text_input("E-mail")
        # CPF: só aceita dígitos, formata apenas ao salvar
        cpf_raw = st.text_input("CPF", value="", max_chars=11, key="cpf_matricula", help="Apenas números")
        cpf_raw = ''.join(filter(str.isdigit, cpf_raw))[:11]
        # Não exibe mais o valor formatado abaixo
    with col2:
        data_nasc = st.date_input(
            "Data de nascimento",
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )
        # RG: aceita até 11 caracteres (letras e números), remove espaços extras
        rg = st.text_input("RG", value="", max_chars=11, key="rg_matricula", help="Máx. 11 caracteres (ex: 1234567, 12345678, 123456789, RGM12345678)")
        rg = rg.strip().replace(" ", "")[:11]
        # Telefone: só aceita dígitos, formata apenas ao salvar
        tel_raw = st.text_input("Telefone", value="", max_chars=11, key="tel_matricula", help="Apenas números")
        tel_raw = ''.join(filter(str.isdigit, tel_raw))[:11]
        # Não exibe mais o valor formatado abaixo

    # --- IDENTIFICAÇÃO DA LINHA DO TRANSPORTE ---
    st.markdown("#### 🚌 Identificação da Linha do Transporte")
    col3, col4 = st.columns(2)
    with col3:
        distrito = st.selectbox(
            "Distrito/Localidade",
            get_options_api("distritos")
        )
    with col4:
        transportador = st.selectbox(
            "Transportador",
            get_options_api("transportadores")
        )

    # --- INSTITUIÇÃO DE ENSINO E INFORMAÇÕES DO CURSO ---
    st.markdown("#### 🎓 Instituição de Ensino e Informações do Curso")
    col5, col6 = st.columns([2,1])
    with col5:
        instituicao = st.selectbox(
            "Instituição de ensino",
            get_options_api("instituicoes")
        )

    col7, col8 = st.columns([2,1])
    with col7:
        curso = st.selectbox(
            "Curso",
            get_options_api("cursos")
        )

    periodo = st.selectbox(
        "Período/Semestre",
        [
            "Selecione...",
            "1º PERÍODO/SEMESTRE",
            "2º PERÍODO/SEMESTRE",
            "3º PERÍODO/SEMESTRE",
            "4º PERÍODO/SEMESTRE",
            "5º PERÍODO/SEMESTRE",
            "6º PERÍODO/SEMESTRE",
            "7º PERÍODO/SEMESTRE",
            "8º PERÍODO/SEMESTRE",
            "9º PERÍODO/SEMESTRE",
            "10º PERÍODO/SEMESTRE"
        ]
    )

    dias_opcoes = [
        "Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Todos os dias"
    ]
    dias = st.multiselect(
        "🗓️ Dias de utilização",
        dias_opcoes
    )
    # Lógica: se marcar todos os dias da semana, vira 'Todos os dias'
    dias_semana = dias_opcoes[:-1]
    if set(dias_semana).issubset(set(dias)):
        dias = ["Todos os dias"]
    elif "Todos os dias" in dias and len(dias) > 1:
        dias = ["Todos os dias"]

    # --- INSTITUIÇÃO DE ENSINO E INFORMAÇÕES DO CURSO (parte inferior) ---
    st.markdown("#### 📅 Validade e Observação")
    col9, col10 = st.columns(2)
    with col9:
        data_validade = st.date_input("Data de validade", value=date.today())
    with col10:
        observacao = st.text_input("Observação")

    # --- BOTÕES ---
    col11, col12 = st.columns([1,1])
    with col11:
        if st.button("Salvar"):
            payload = {
                "nome": nome,
                "email": email,
                "cpf": format_cpf(cpf_raw),
                "data_nasc": str(data_nasc),
                "rg": rg,
                "telefone": format_telefone(tel_raw),
                "distrito": distrito,
                "transportador": transportador,
                "instituicao": instituicao,
                "curso": curso,
                "periodo": periodo,
                "dias": dias,
                "data_validade": str(data_validade),
                "observacao": observacao
            }
            try:
                response = requests.post(f"{API_URL}/carteirinha/", json=payload)
                if response.status_code == 200:
                    st.success("Dados salvos com sucesso!")
                else:
                    st.error(f"Erro: {response.json()['detail']}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")
    with col12:
        if st.button("Cancelar"):
            st.warning("Operação cancelada.")
