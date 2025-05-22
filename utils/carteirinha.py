import streamlit as st
from utils.pdf_utils import gerar_carteirinha_pdf_por_id
import requests
import os

def aba_carteirinha():
    st.title("🪪 Gerar Carteirinha")
    # Buscar alunos da API
    try:
        response = requests.get("http://localhost:8000/alunos/")
        if response.status_code == 200:
            alunos = response.json()
        else:
            alunos = []
    except Exception:
        alunos = []

    if not alunos:
        st.warning("Nenhum aluno cadastrado.")
        return

    nomes = [a['nome'] for a in alunos]
    selected_nome = st.selectbox("Selecione o aluno para gerar a carteirinha", ["Selecione..."] + nomes)
    if selected_nome != "Selecione...":
        aluno = next(a for a in alunos if a['nome'] == selected_nome)
        aluno_id = aluno['id']
        carteirinha_id = None
        # Buscar carteirinha_id do aluno
        try:
            resp = requests.get(f"http://localhost:8000/carteirinha/por_aluno/{aluno_id}")
            if resp.status_code == 200:
                carteirinha_id = resp.json().get("carteirinha_id")
            else:
                st.error("Carteirinha não encontrada para este aluno.")
                return
        except Exception as e:
            st.error(f"Erro ao buscar carteirinha: {e}")
            return
        if st.button("Gerar Carteirinha em PDF"):
            foto_path = os.path.join("static", "fotos", f"{aluno_id}.jpg")
            output_path = os.path.join("data", f"carteirinha_{aluno_id}.pdf")
            try:
                gerar_carteirinha_pdf_por_id(carteirinha_id, foto_path, output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Baixar PDF da Carteirinha", f, file_name=f"carteirinha_{aluno_id}.pdf")
                st.success("Carteirinha gerada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao gerar carteirinha: {e}")
