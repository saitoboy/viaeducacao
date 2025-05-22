import streamlit as st
import pandas as pd
import requests
from datetime import date, datetime
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

def parse_data(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%d").date()
    except Exception:
        return date.today()

def get_options_api(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}/")
        if response.status_code == 200:
            return ["Selecione..."] + response.json()
        else:
            return ["Selecione..."]
    except Exception:
        return ["Selecione..."]

def aba_alunos():
    st.title("👨‍🎓 Alunos")
    try:
        response = requests.get(f"{API_URL}/alunos/")
        if response.status_code == 200:
            alunos = response.json()
            if alunos:
                # Campo de busca com ícone de lupa
                st.markdown("---")
                st.subheader("Buscar aluno")
                search_col1, search_col2 = st.columns([0.08, 0.92])
                with search_col1:
                    st.markdown('<span style="font-size: 1.5em;">🔍</span>', unsafe_allow_html=True)
                with search_col2:
                    search = st.text_input(
                        label="Buscar aluno por nome ou CPF",
                        placeholder="Digite nome ou CPF para buscar",
                        key="search_aluno",
                        label_visibility="collapsed"
                    )
                if search:
                    alunos_filtrados = [a for a in alunos if search.lower() in a['nome'].lower() or search in a['cpf']]
                else:
                    alunos_filtrados = alunos
                df_filtrado = pd.DataFrame(alunos_filtrados)
                st.markdown("---")
                st.subheader("Lista de alunos")
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                # Seleção por selectbox (simulação de clique na linha)
                nomes = df_filtrado['nome'].tolist() if not df_filtrado.empty else []
                selected_nome = st.selectbox("Clique para selecionar um aluno da lista", ["Selecione..."] + nomes, key="selectbox_aluno")
                if selected_nome != "Selecione...":
                    aluno = next(a for a in alunos_filtrados if a['nome'] == selected_nome)
                    # Estado de confirmação de exclusão por aluno
                    if 'confirma_excluir_id' not in st.session_state:
                        st.session_state['confirma_excluir_id'] = None
                    with st.form(key="edit_aluno_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_nome = st.text_input("Nome do aluno", value=aluno['nome'])
                            novo_email = st.text_input("E-mail", value=aluno['email'])
                            cpf_raw = st.text_input("CPF", value=''.join(filter(str.isdigit, aluno['cpf'])), max_chars=11, key="cpf_edit", help="Apenas números")
                            cpf_raw = ''.join(filter(str.isdigit, cpf_raw))[:11]
                            novo_cpf = format_cpf(cpf_raw)
                            novo_data_nasc = st.date_input(
                                "Data de nascimento",
                                value=parse_data(aluno.get('data_nascimento', '')),
                                min_value=date(1900, 1, 1),
                                max_value=date.today()
                            )
                            novo_rg = st.text_input("RG", value=aluno.get('rg', ''), max_chars=11, key="rg_edit", help="Máx. 11 caracteres (ex: 1234567, 12345678, 123456789, RGM12345678)")
                            novo_rg = novo_rg.strip().replace(" ", "")[:11]
                            tel_raw = st.text_input("Telefone", value=''.join(filter(str.isdigit, aluno.get('telefone', ''))), max_chars=11, key="tel_edit", help="Apenas números")
                            tel_raw = ''.join(filter(str.isdigit, tel_raw))[:11]
                            novo_telefone = format_telefone(tel_raw)
                        with col2:
                            distritos = get_options_api("distritos")
                            transportadores = get_options_api("transportadores")
                            instituicoes = get_options_api("instituicoes")
                            cursos = get_options_api("cursos")
                            periodos = [
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
                            dias_opcoes = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Todos os dias"]
                            novo_distrito = st.selectbox("Distrito/Localidade", distritos, index=distritos.index(aluno.get('distrito')) if aluno.get('distrito') in distritos else 0)
                            novo_transportador = st.selectbox("Transportador", transportadores, index=transportadores.index(aluno.get('transportador')) if aluno.get('transportador') in transportadores else 0)
                            novo_instituicao = st.selectbox("Instituição de ensino", instituicoes, index=instituicoes.index(aluno.get('instituicao')) if aluno.get('instituicao') in instituicoes else 0)
                            novo_curso = st.selectbox("Curso", cursos, index=cursos.index(aluno.get('curso')) if aluno.get('curso') in cursos else 0)
                            novo_periodo = st.selectbox("Período/Semestre", periodos, index=periodos.index(aluno.get('periodo')) if aluno.get('periodo') in periodos else 0)
                            dias_valor = aluno.get('dias', [])
                            if isinstance(dias_valor, str):
                                dias_valor = [d.strip() for d in dias_valor.split(',') if d.strip()]
                            novo_dias = st.multiselect("🗓️ Dias de utilização", dias_opcoes, default=dias_valor)
                            # Lógica: se marcar todos os dias da semana, vira 'Todos os dias'
                            dias_semana = dias_opcoes[:-1]
                            if set(dias_semana).issubset(set(novo_dias)):
                                novo_dias = ["Todos os dias"]
                            elif "Todos os dias" in novo_dias and len(novo_dias) > 1:
                                novo_dias = ["Todos os dias"]
                            novo_data_validade = st.date_input(
                                "Data de validade",
                                value=parse_data(aluno.get('data_validade', '')),
                                min_value=date(1900, 1, 1),
                                max_value=date(2100, 12, 31)
                            )
                            novo_observacao = st.text_input("Observação", value=aluno.get('observacao', ''))
                        col3, col4 = st.columns(2)
                        with col3:
                            atualizar = st.form_submit_button("Atualizar")
                        with col4:
                            deletar = st.form_submit_button("Excluir", type="secondary")
                    if atualizar:
                        # Atualiza dados do aluno
                        payload_aluno = {
                            "nome": novo_nome,
                            "email": novo_email,
                            "cpf": novo_cpf,
                            "data_nascimento": str(novo_data_nasc),
                            "rg": novo_rg,
                            "telefone": novo_telefone
                        }
                        try:
                            resp_aluno = requests.put(f"{API_URL}/alunos/{aluno['id']}", json=payload_aluno)
                            # Atualiza dados da carteirinha
                            # Buscar carteirinha_id
                            resp_carteirinha_id = requests.get(f"{API_URL}/carteirinha/por_aluno/{aluno['id']}")
                            if resp_carteirinha_id.status_code == 200:
                                carteirinha_id = resp_carteirinha_id.json().get("carteirinha_id")
                                payload_carteirinha = {
                                    "distrito": novo_distrito,
                                    "transportador": novo_transportador,
                                    "instituicao": novo_instituicao,
                                    "curso": novo_curso,
                                    "periodo": novo_periodo,
                                    "dias": novo_dias,
                                    "data_validade": str(novo_data_validade),
                                    "observacao": novo_observacao
                                }
                                requests.put(f"{API_URL}/carteirinha/{carteirinha_id}", json=payload_carteirinha)
                            if resp_aluno.status_code == 200:
                                st.success("Aluno atualizado com sucesso!", icon="✅")
                                st.rerun()
                            else:
                                st.error(f"Erro ao atualizar: {resp_aluno.text}")
                        except Exception as e:
                            st.error(f"Erro ao conectar com a API: {e}")
                    # Confirmação de exclusão sem modal
                    if deletar:
                        st.session_state['confirma_excluir_id'] = aluno['id']
                    if st.session_state.get('confirma_excluir_id') == aluno['id']:
                        confirma = st.checkbox(f"Confirmar exclusão de {aluno['nome']} ({aluno['cpf']})", key=f"confirma_excluir_{aluno['id']}")
                        if confirma:
                            try:
                                resp = requests.delete(f"{API_URL}/alunos/{aluno['id']}")
                                if resp.status_code == 200:
                                    st.success("Aluno excluído com sucesso!", icon="🗑️")
                                    st.session_state['confirma_excluir_id'] = None
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao excluir: {resp.text}")
                            except Exception as e:
                                st.error(f"Erro ao conectar com a API: {e}")
            else:
                st.info("Nenhum aluno cadastrado.")
        else:
            st.error("Erro ao buscar alunos na API.")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
