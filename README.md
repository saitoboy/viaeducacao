# ViaEducação 🚍

Bem-vindo! Este sistema serve para cadastrar e gerenciar carteirinhas de transporte escolar.

Mesmo que você nunca tenha usado Docker ou terminal, siga o passo a passo abaixo que vai dar certo!

## O que é cada coisa?

- **Docker**: é um programa que facilita a instalação do sistema, sem precisar configurar nada complicado. Ele "empacota" tudo que o sistema precisa para rodar.
- **Streamlit**: é o que mostra a tela do sistema no navegador (como se fosse um site).
- **FastAPI**: é o que faz o sistema conversar com o banco de dados.
- **PostgreSQL**: é onde os dados ficam guardados (o banco de dados).

## O que é terminal/PowerShell?

- O terminal é uma “tela preta” onde você digita comandos para o computador executar tarefas.
- No Windows, use o **PowerShell** (procure por "PowerShell" no menu iniciar).

## Como rodar o sistema (passo a passo para iniciantes)

1. **Instale o Docker Desktop**
   - Baixe em: https://www.docker.com/products/docker-desktop/
   - Instale normalmente (como qualquer programa do Windows).
   - Depois de instalar, abra o Docker Desktop e deixe ele aberto.

2. **Baixe o código do sistema**
   - Peça para quem te enviou o sistema te passar a pasta, ou baixe do GitHub.

3. **Abra o terminal (PowerShell)**
   - Clique no menu iniciar, digite “PowerShell” e abra o programa azul que aparecer.

4. **Entre na pasta do sistema**
   - No terminal, digite:
     ```powershell
     cd CAMINHO\DA\PASTA\DO\PROJETO
     ```
     (Exemplo: `cd C:\Users\SeuNome\Downloads\viaeducacao`)

5. **Rode o sistema**
   - No terminal, digite:
     ```powershell
     docker-compose up --build
     ```
   - Aguarde até aparecer a mensagem que o sistema está rodando. Isso pode demorar na primeira vez.

6. **Abra o sistema no navegador**
   - Abra o Chrome, Edge ou Firefox.
   - Digite na barra de endereços: `http://localhost:8501`
   - Pronto! O sistema vai aparecer.

7. **Para parar o sistema**
   - Clique na janela do terminal e pressione as teclas `Ctrl` e `C` ao mesmo tempo.

---

## ✨ Funcionalidades

- Cadastro, busca, edição e exclusão de alunos
- Cadastro e gestão de distritos, transportadores, instituições e cursos
- Geração de carteirinhas de transporte escolar
- Relatórios dinâmicos com gráficos e tabelas (alunos por distrito, transportador, dia etc)
- Exclusão segura com confirmação e exclusão em cascata
- Máscara automática para CPF e telefone
- Interface moderna, responsiva e com emojis para melhor experiência

## 🚀 Como rodar o projeto

### Opção 1: Rodando com Docker (RECOMENDADO)

1. **Instale o Docker Desktop:**
   - Baixe e instale em https://www.docker.com/products/docker-desktop/
   - Abra o Docker Desktop e deixe ele rodando.

2. **Configure o arquivo `.env`:**
   - Já está pronto para Docker, não precisa mudar nada.

3. **Suba tudo com Docker Compose:**
   - No terminal, dentro da pasta do projeto, rode:
     ```powershell
     docker-compose up --build
     ```
   - Isso vai subir o banco, o backend (FastAPI) e o frontend (Streamlit) juntos.

4. **Acesse o sistema:**
   - Frontend (Streamlit): http://localhost:8501
   - Backend (FastAPI): http://localhost:8000

5. **Para parar tudo:**
   - No terminal, pressione `Ctrl+C`.
   - Para remover os containers, rode:
     ```powershell
     docker-compose down
     ```

---

### Opção 2: Rodando manualmente (sem Docker)

1. Instale o Python 3.9+ e o PostgreSQL na sua máquina.
2. Configure o `.env` para usar `localhost` como host do banco.
3. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
4. Rode o backend:
   ```powershell
   uvicorn backend.main:app --reload
   ```
5. Em outro terminal, rode o frontend:
   ```powershell
   streamlit run app.py
   ```

---

> **Dica:**
> Se não souber nada de Docker, use a Opção 1 e só rode o comando do passo 3. O Docker faz tudo sozinho!

> **Atenção para usuários do Git Bash no Windows:**
> - Se você usar o Git Bash para rodar o comando `docker-compose up --build`, pode dar erro de path ou de permissão.
> - Prefira rodar os comandos do Docker no **Prompt de Comando (cmd.exe)** ou **PowerShell** do Windows.
> - Se quiser usar o Git Bash mesmo assim, adicione `winpty` antes do comando:
>   ```bash
>   winpty docker-compose up --build
>   ```
> - Mas o mais seguro é usar o PowerShell ou o terminal padrão do Windows!

## 🌐 Como funciona o acesso na web e no computador das pessoas

- **Na sua máquina (desenvolvimento):**
  - Você acessa o sistema pelo navegador em `http://localhost:8501` (Streamlit) e `http://localhost:8000` (FastAPI).
  - O Docker cria um "mini-servidor" na sua máquina, rodando tudo isolado, sem precisar instalar Python ou PostgreSQL manualmente.
  - Só você (no seu computador) consegue acessar esses endereços.

- **Na VPS (produção/servidor):**
  - O Docker funciona igual, mas agora o sistema está disponível para qualquer pessoa que acessar o IP da VPS.
  - Exemplo: se o IP da sua VPS for `123.123.123.123`, acesse `http://123.123.123.123:8501` no navegador de qualquer computador.
  - O backend (FastAPI) fica em `http://123.123.123.123:8000` (normalmente só usado pelo sistema, não pelo usuário final).
  - O banco de dados PostgreSQL fica protegido dentro do Docker, não exposto para a internet (a não ser que você libere a porta 5432, o que não é recomendado).

- **No computador de outras pessoas (usuários):**
  - Basta passar o link do Streamlit rodando na VPS (ex: `http://123.123.123.123:8501`).
  - Não precisa instalar nada, só abrir o navegador.
  - O Docker só precisa estar instalado na máquina do desenvolvedor ou no servidor, nunca no computador do usuário final.

> **Resumo:**
> - Docker é só para quem vai rodar o sistema (desenvolvedor ou servidor).
> - Usuário final só precisa do link e de um navegador!

## 🗝️ Configuração do arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo (exemplo):

```
API_URL=http://localhost:8000
DATABASE_URL=postgresql://USUARIO:SenhaDoBanco@db:5432/viaeducacao
DB_HOST=db
DB_NAME=viaeducacao
DB_USER=USUARIO
DB_PASS=SenhaDoBanco
```

- **USUARIO** e **SenhaDoBanco**: substitua pelo usuário e senha do seu banco PostgreSQL.
- Se for rodar localmente (sem Docker), troque `db` por `localhost` em `DATABASE_URL` e `DB_HOST`.
- O arquivo `.env` nunca deve ser enviado para o GitHub (adicione ao `.gitignore`).

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

## 🛠️ Como criar/restaurar o banco de dados

- O banco de dados é criado automaticamente pelo Docker Compose na primeira vez que você roda o sistema.
- As tabelas são criadas automaticamente pelo backend FastAPI ao rodar o sistema.
- Se precisar popular o banco com dados iniciais, utilize o script `inicial_app.py` (rode manualmente se desejar).

## 🗃️ Como acessar o banco de dados (administração)

- Você pode usar ferramentas como **DBeaver**, **pgAdmin** ou o próprio terminal para acessar o PostgreSQL.
- Dados de acesso (padrão Docker):
  - Host: `localhost` (ou `db` dentro do Docker)
  - Porta: `5432`
  - Usuário e senha: conforme seu `.env`
  - Banco: `viaeducacao`

## ⚙️ Variáveis de ambiente extras

- Você pode adicionar variáveis extras no `.env` para customizar portas, debug, etc.
- Exemplo: `DEBUG=True` (se seu código suportar)

## 🔄 Como atualizar o sistema

- Para atualizar o código, basta rodar:
  ```powershell
  git pull
  docker-compose up --build
  ```
- O Docker vai reconstruir e rodar a versão nova automaticamente.

## 💾 Como fazer backup dos dados

- Para fazer backup do banco:
  ```powershell
  docker exec -t viaeducacao-db-1 pg_dump -U USUARIO viaeducacao > backup.sql
  ```
- Para backup das fotos, copie a pasta `static/fotos`.

## 📝 Licença

Este projeto é open-source e pode ser adaptado conforme a necessidade da sua instituição.

---

Desenvolvido com ❤️ para a ViaEducação.
