import streamlit as st
from utils.pdf_utils import gerar_carteirinha_pdf_por_id
from slugify import slugify
import requests
import os
from io import BytesIO
import unicodedata
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

def slugify_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome = nome.replace(' ', '_')
    return nome

def aba_carteirinha():
    st.title("🪪 Gerar Carteirinha")
    # Buscar alunos da API
    try:
        response = requests.get(f"{API_URL}/alunos/")
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
            resp = requests.get(f"{API_URL}/carteirinha/por_aluno/{aluno_id}")
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
            nome_slug = slugify(aluno['nome'])
            output_path = os.path.join("data", f"carteirinha_{nome_slug}.pdf")
            try:
                gerar_carteirinha_pdf_por_id(carteirinha_id, foto_path, output_path)
                with open(output_path, "rb") as f:
                    pdf_bytes = f.read()
                st.success("Carteirinha gerada com sucesso! Clique no botão abaixo para baixar o PDF.")
                # Exibir preview do PDF
                base64_pdf = pdf_bytes.encode('base64') if hasattr(pdf_bytes, 'encode') else None
                if not base64_pdf:
                    import base64
                    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                st.download_button(
                    label="Clique aqui para baixar a carteirinha em PDF",
                    data=pdf_bytes,
                    file_name=f"carteirinha_{nome_slug}.pdf",
                    mime="application/pdf",
                    key=f"download_{aluno_id}"
                )
            except Exception as e:
                st.error(f"Erro ao gerar carteirinha: {e}")
