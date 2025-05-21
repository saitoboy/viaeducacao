import streamlit as st
import pandas as pd
import requests

def aba_gestao():
    st.title("🛠️ Gestão de Dados Cadastrais")

    aba = st.selectbox("O que deseja adicionar?", [
        "Distrito", "Transportador", "Instituição de Ensino", "Curso"
    ])

    def get_existing(endpoint):
        try:
            resp = requests.get(f"http://localhost:8000/{endpoint}/")
            if resp.status_code == 200:
                return resp.json()
            else:
                return []
        except Exception:
            return []

    if aba == "Distrito":
        nome = st.text_input("Nome do Distrito")
        if st.button("Adicionar Distrito"):
            if nome.strip():
                resp = requests.post("http://localhost:8000/distritos/", json={"nome": nome})
                if resp.status_code == 200:
                    st.success("Distrito adicionado com sucesso!")
                else:
                    st.error(f"Erro: {resp.json().get('detail', 'Erro desconhecido')}")
            else:
                st.warning("Preencha o nome do distrito.")
        st.markdown("#### Distritos já cadastrados")
        distritos = get_existing("distritos")
        if distritos:
            df_distritos = pd.DataFrame(distritos, columns=["Nome"])
            st.table(df_distritos)
            selected = st.selectbox("Selecione um distrito para excluir", ["Selecione..."] + df_distritos["Nome"].tolist(), key="excluir_distrito")
            if selected != "Selecione...":
                confirma = st.checkbox(f"Confirmar exclusão de '{selected}'", key="confirma_excluir_distrito")
                if confirma and st.button(f"Excluir '{selected}'", key="btn_excluir_distrito"):
                    try:
                        resp = requests.delete(f"http://localhost:8000/distritos/{selected}")
                        if resp.status_code == 200:
                            st.success("Distrito excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao excluir: {resp.text}")
                    except Exception as e:
                        st.error(f"Erro ao conectar com a API: {e}")
        else:
            st.info("Nenhum distrito cadastrado.")

    elif aba == "Transportador":
        nome = st.text_input("Nome do Transportador")
        if st.button("Adicionar Transportador"):
            if nome.strip():
                resp = requests.post("http://localhost:8000/transportadores/", json={"nome": nome})
                if resp.status_code == 200:
                    st.success("Transportador adicionado com sucesso!")
                else:
                    st.error(f"Erro: {resp.json().get('detail', 'Erro desconhecido')}")
            else:
                st.warning("Preencha o nome do transportador.")
        st.markdown("#### Transportadores já cadastrados")
        transportadores = get_existing("transportadores")
        if transportadores:
            df_transportadores = pd.DataFrame(transportadores, columns=["Nome"])
            st.table(df_transportadores)
            selected = st.selectbox("Selecione um transportador para excluir", ["Selecione..."] + df_transportadores["Nome"].tolist(), key="excluir_transportador")
            if selected != "Selecione...":
                confirma = st.checkbox(f"Confirmar exclusão de '{selected}'", key="confirma_excluir_transportador")
                if confirma and st.button(f"Excluir '{selected}'", key="btn_excluir_transportador"):
                    try:
                        resp = requests.delete(f"http://localhost:8000/transportadores/{selected}")
                        if resp.status_code == 200:
                            st.success("Transportador excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao excluir: {resp.text}")
                    except Exception as e:
                        st.error(f"Erro ao conectar com a API: {e}")
        else:
            st.info("Nenhum transportador cadastrado.")

    elif aba == "Instituição de Ensino":
        nome = st.text_input("Nome da Instituição de Ensino")
        if st.button("Adicionar Instituição"):
            if nome.strip():
                resp = requests.post("http://localhost:8000/instituicoes/", json={"nome": nome})
                if resp.status_code == 200:
                    st.success("Instituição adicionada com sucesso!")
                else:
                    st.error(f"Erro: {resp.json().get('detail', 'Erro desconhecido')}")
            else:
                st.warning("Preencha o nome da instituição.")
        st.markdown("#### Instituições já cadastradas")
        instituicoes = get_existing("instituicoes")
        if instituicoes:
            df_instituicoes = pd.DataFrame(instituicoes, columns=["Nome"])
            st.table(df_instituicoes)
            selected = st.selectbox("Selecione uma instituição para excluir", ["Selecione..."] + df_instituicoes["Nome"].tolist(), key="excluir_instituicao")
            if selected != "Selecione...":
                confirma = st.checkbox(f"Confirmar exclusão de '{selected}'", key="confirma_excluir_instituicao")
                if confirma and st.button(f"Excluir '{selected}'", key="btn_excluir_instituicao"):
                    try:
                        resp = requests.delete(f"http://localhost:8000/instituicoes/{selected}")
                        if resp.status_code == 200:
                            st.success("Instituição excluída com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao excluir: {resp.text}")
                    except Exception as e:
                        st.error(f"Erro ao conectar com a API: {e}")
        else:
            st.info("Nenhuma instituição cadastrada.")

    elif aba == "Curso":
        nome = st.text_input("Nome do Curso")
        if st.button("Adicionar Curso"):
            if nome.strip():
                resp = requests.post("http://localhost:8000/cursos/", json={"nome": nome})
                if resp.status_code == 200:
                    st.success("Curso adicionado com sucesso!")
                else:
                    st.error(f"Erro: {resp.json().get('detail', 'Erro desconhecido')}")
            else:
                st.warning("Preencha o nome do curso.")
        st.markdown("#### Cursos já cadastrados")
        cursos = get_existing("cursos")
        if cursos:
            df_cursos = pd.DataFrame(cursos, columns=["Nome"])
            st.table(df_cursos)
            selected = st.selectbox("Selecione um curso para excluir", ["Selecione..."] + df_cursos["Nome"].tolist(), key="excluir_curso")
            if selected != "Selecione...":
                confirma = st.checkbox(f"Confirmar exclusão de '{selected}'", key="confirma_excluir_curso")
                if confirma and st.button(f"Excluir '{selected}'", key="btn_excluir_curso"):
                    try:
                        resp = requests.delete(f"http://localhost:8000/cursos/{selected}")
                        if resp.status_code == 200:
                            st.success("Curso excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao excluir: {resp.text}")
                    except Exception as e:
                        st.error(f"Erro ao conectar com a API: {e}")
        else:
            st.info("Nenhum curso cadastrado.")
