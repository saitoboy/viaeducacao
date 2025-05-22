from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from backend.db import get_connection
import psycopg2
import bcrypt
import re
import time

router = APIRouter()

# Controle simples de tentativas de login (em memória)
# Agora por e-mail de usuário
login_attempts = {}
LOCK_TIME = 300  # 5 minutos em segundos

# Função para validar senha forte
# Pelo menos 8 caracteres, 1 maiúscula, 1 minúscula, 1 número, 1 caractere especial
def senha_forte(senha: str) -> bool:
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};:\\|,.<>/?]).{8,}$', senha))

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioTrocaSenha(BaseModel):
    email: str
    senha_atual: str
    nova_senha: str

@router.post("/login/")
def login_usuario(dados: UsuarioLogin, request: Request):
    email = dados.email.lower().strip()
    now = time.time()
    tentativas = login_attempts.get(email, {"count": 0, "last": 0, "locked_until": 0})
    if tentativas.get("locked_until", 0) > now:
        tempo_restante = int((tentativas["locked_until"] - now) // 60) + 1
        raise HTTPException(status_code=429, detail=f"Muitas tentativas. Aguarde {tempo_restante} minutos para tentar novamente.")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT usuario_id, email, senha FROM usuarios WHERE email = %s", (email,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=401, detail="Usuário não encontrado. Verifique o e-mail digitado.")
        if bcrypt.checkpw(dados.senha.encode('utf-8'), row[2].encode('utf-8')):
            login_attempts[email] = {"count": 0, "last": now, "locked_until": 0}  # reset tentativas
            token = f"token_{row[0]}"
            return {"usuario_id": row[0], "email": row[1], "token": token}
        else:
            tentativas["count"] += 1
            tentativas["last"] = now
            if tentativas["count"] >= 3:
                tentativas["locked_until"] = now + LOCK_TIME
            login_attempts[email] = tentativas
            if tentativas["count"] >= 3:
                raise HTTPException(status_code=401, detail="Senha incorreta. Usuário bloqueado por 5 minutos após 3 tentativas.")
            else:
                raise HTTPException(status_code=401, detail=f"Senha incorreta. Você tem mais {3-tentativas['count']} tentativa(s) antes do bloqueio.")
    finally:
        cur.close()
        conn.close()

@router.get("/usuarios/")
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT usuario_id, email FROM usuarios ORDER BY email")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"usuario_id": r[0], "email": r[1]} for r in results]

@router.post("/usuarios/")
def criar_usuario(usuario: UsuarioLogin):
    if not senha_forte(usuario.senha):
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial.")
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Gera hash da senha
        hashed = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
        cur.execute(
            "INSERT INTO usuarios (email, senha) VALUES (%s, %s) RETURNING usuario_id",
            (usuario.email, hashed.decode('utf-8'))
        )
        usuario_id = cur.fetchone()[0]
        conn.commit()
        return {"usuario_id": usuario_id, "email": usuario.email}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@router.post("/usuarios/trocar_senha/")
def trocar_senha(dados: UsuarioTrocaSenha):
    if not senha_forte(dados.nova_senha):
        raise HTTPException(status_code=400, detail="A nova senha deve ter pelo menos 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial.")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT senha FROM usuarios WHERE email = %s", (dados.email,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        senha_hash = row[0]
        if not bcrypt.checkpw(dados.senha_atual.encode('utf-8'), senha_hash.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Senha atual incorreta.")
        novo_hash = bcrypt.hashpw(dados.nova_senha.encode('utf-8'), bcrypt.gensalt())
        cur.execute("UPDATE usuarios SET senha = %s WHERE email = %s", (novo_hash.decode('utf-8'), dados.email))
        conn.commit()
        return {"status": "Senha alterada com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
