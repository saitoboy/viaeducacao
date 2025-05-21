# ViaEducação 🚍

Sistema completo para cadastro, gestão e geração de carteirinhas de transporte escolar, desenvolvido com **Streamlit** (frontend) e **FastAPI** (backend), integrando banco de dados **PostgreSQL**.

## ✨ Funcionalidades

- Cadastro, busca, edição e exclusão de alunos
- Cadastro e gestão de distritos, transportadores, instituições e cursos
- Geração de carteirinhas de transporte escolar
- Relatórios dinâmicos com gráficos e tabelas (alunos por distrito, transportador, dia etc)
- Exclusão segura com confirmação e exclusão em cascata
- Máscara automática para CPF e telefone
- Interface moderna, responsiva e com emojis para melhor experiência

## 🚀 Como rodar o projeto

1. **Clone o repositório:**
   ```
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO
   ```

2. **Configure o ambiente:**
   - Coloque a logo em `template/logo.png` (opcional)
   - Renomeie `.env.example` para `.env` e configure as variáveis de acesso ao PostgreSQL

3. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```

4. **Execute o backend (FastAPI):**
   ```
   uvicorn backend.main:app --reload
   ```

5. **Execute o frontend (Streamlit):**
   ```
   streamlit run app.py
   ```

## 📁 Estrutura do projeto

- `app.py` — Aplicativo principal Streamlit
- `backend/` — API FastAPI (CRUD, relatórios, integração com banco)
- `utils/` — Utilitários de frontend (tabs, helpers, PDF, etc)
- `static/fotos/` — Fotos dos alunos
- `template/` — Logo e recursos visuais
- `data/` — Dados temporários ou de backup

## ⚙️ Requisitos

- Python 3.9+
- PostgreSQL
- Variáveis de ambiente configuradas em `.env`

## 💡 Dicas

- O app utiliza máscaras automáticas para CPF e telefone.
- Exclusões de entidades são seguras e pedem confirmação.
- Relatórios podem ser exportados via tabelas.

## 📝 Licença

Este projeto é open-source e pode ser adaptado conforme a necessidade da sua instituição.

---

Desenvolvido com ❤️ para a ViaEducação.
