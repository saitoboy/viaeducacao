import streamlit as st
import pandas as pd
import requests

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

def aba_alunos():
    st.title("👨‍🎓 Alunos")
    try:
        response = requests.get("http://localhost:8000/alunos/")
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
                        novo_nome = st.text_input("Nome", value=aluno['nome'])
                        novo_email = st.text_input("E-mail", value=aluno['email'])
                        # CPF: só aceita dígitos, formata apenas ao salvar
                        cpf_raw = st.text_input("CPF", value=''.join(filter(str.isdigit, aluno['cpf'])), max_chars=11, key="cpf_edit", help="Apenas números")
                        cpf_raw = ''.join(filter(str.isdigit, cpf_raw))[:11]
                        novo_cpf = format_cpf(cpf_raw)
                        novo_data_nasc = st.text_input("Data de nascimento", value=aluno.get('data_nascimento', ''))
                        # RG: aceita até 11 caracteres (letras e números), remove espaços extras
                        novo_rg = st.text_input("RG", value=aluno.get('rg', ''), max_chars=11, key="rg_edit", help="Máx. 11 caracteres (ex: 1234567, 12345678, 123456789, RGM12345678)")
                        novo_rg = novo_rg.strip().replace(" ", "")[:11]
                        # Telefone: só aceita dígitos, formata apenas ao salvar
                        tel_raw = st.text_input("Telefone", value=''.join(filter(str.isdigit, aluno.get('telefone', ''))), max_chars=11, key="tel_edit", help="Apenas números")
                        tel_raw = ''.join(filter(str.isdigit, tel_raw))[:11]
                        novo_telefone = format_telefone(tel_raw)
                        col1, col2 = st.columns(2)
                        with col1:
                            atualizar = st.form_submit_button("Atualizar")
                        with col2:
                            deletar = st.form_submit_button("Excluir", type="secondary")
                    if atualizar:
                        payload = {
                            "nome": novo_nome,
                            "email": novo_email,
                            "cpf": novo_cpf,
                            "data_nascimento": novo_data_nasc,
                            "rg": novo_rg,
                            "telefone": novo_telefone
                        }
                        try:
                            resp = requests.put(f"http://localhost:8000/alunos/{aluno['id']}", json=payload)
                            if resp.status_code == 200:
                                st.success("Aluno atualizado com sucesso!", icon="✅")
                                st.rerun()
                            else:
                                st.error(f"Erro ao atualizar: {resp.text}")
                        except Exception as e:
                            st.error(f"Erro ao conectar com a API: {e}")
                    # Confirmação de exclusão sem modal
                    if deletar:
                        st.session_state['confirma_excluir_id'] = aluno['id']
                    if st.session_state.get('confirma_excluir_id') == aluno['id']:
                        confirma = st.checkbox(f"Confirmar exclusão de {aluno['nome']} ({aluno['cpf']})", key=f"confirma_excluir_{aluno['id']}")
                        if confirma:
                            try:
                                resp = requests.delete(f"http://localhost:8000/alunos/{aluno['id']}")
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
