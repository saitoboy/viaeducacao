#uvicorn backend.main:app --reload

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from backend.db import get_connection
from backend.routes.gestao import router as gestao_router
from backend.routes.matriculas import router as matriculas_router
from backend.routes.alunos import router as alunos_router
from backend.routes.relatorios import router as relatorios_router

load_dotenv()

app = FastAPI()

# Permitir requisições do Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gestao_router)
app.include_router(matriculas_router)
app.include_router(alunos_router)
app.include_router(relatorios_router)

class CarteirinhaIn(BaseModel):
    nome: str
    email: str
    cpf: str
    data_nasc: str
    rg: str
    telefone: str
    distrito: str
    transportador: str
    instituicao: str
    curso: str
    periodo: str
    dias: list
    data_validade: str
    observacao: str

class NomeIn(BaseModel):
    nome: str

@app.post("/carteirinha/")
def criar_carteirinha(dados: CarteirinhaIn):
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Exemplo: inserir aluno e carteirinha (ajuste conforme seu modelo real)
        cur.execute("""
            INSERT INTO alunos (nome, email, cpf, data_nascimento, rg, telefone)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING aluno_id
        """, (dados.nome, dados.email, dados.cpf, dados.data_nasc, dados.rg, dados.telefone))
        aluno_id = cur.fetchone()[0]

        # Buscar ids das tabelas relacionadas
        cur.execute("SELECT distrito_id FROM distritos WHERE nome=%s", (dados.distrito,))
        distrito_id = cur.fetchone()[0]
        cur.execute("SELECT transportador_id FROM transportadores WHERE nome=%s", (dados.transportador,))
        transportador_id = cur.fetchone()[0]
        cur.execute("SELECT instituicao_id FROM instituicoes WHERE nome=%s", (dados.instituicao,))
        instituicao_id = cur.fetchone()[0]
        cur.execute("SELECT curso_id FROM cursos WHERE nome=%s", (dados.curso,))
        curso_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO carteirinhas (
                aluno_id, distrito_id, transportador_id, instituicao_id, curso_id, periodo,
                dias_utilizacao, data_validade, observacao
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            aluno_id, distrito_id, transportador_id, instituicao_id, curso_id, dados.periodo,
            ','.join(dados.dias), dados.data_validade, dados.observacao
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/distritos/")
def get_distritos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM distritos ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@app.post("/distritos/")
def add_distrito(distrito: NomeIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO distritos (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (distrito.nome,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/distritos/{nome}")
def delete_distrito(nome: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT distrito_id FROM distritos WHERE nome = %s", (nome,))
        row = cur.fetchone()
        if row:
            distrito_id = row[0]
            cur.execute("DELETE FROM carteirinhas WHERE distrito_id = %s", (distrito_id,))
            cur.execute("DELETE FROM distritos WHERE distrito_id = %s", (distrito_id,))
            conn.commit()
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail="Distrito não encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/transportadores/")
def get_transportadores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM transportadores ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@app.post("/transportadores/")
def add_transportador(transportador: NomeIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO transportadores (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (transportador.nome,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/transportadores/{nome}")
def delete_transportador(nome: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT transportador_id FROM transportadores WHERE nome = %s", (nome,))
        row = cur.fetchone()
        if row:
            transportador_id = row[0]
            cur.execute("DELETE FROM carteirinhas WHERE transportador_id = %s", (transportador_id,))
            cur.execute("DELETE FROM transportadores WHERE transportador_id = %s", (transportador_id,))
            conn.commit()
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail="Transportador não encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/instituicoes/")
def get_instituicoes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM instituicoes ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@app.post("/instituicoes/")
def add_instituicao(instituicao: NomeIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO instituicoes (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (instituicao.nome,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/instituicoes/{nome}")
def delete_instituicao(nome: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT instituicao_id FROM instituicoes WHERE nome = %s", (nome,))
        row = cur.fetchone()
        if row:
            instituicao_id = row[0]
            cur.execute("DELETE FROM carteirinhas WHERE instituicao_id = %s", (instituicao_id,))
            cur.execute("DELETE FROM instituicoes WHERE instituicao_id = %s", (instituicao_id,))
            conn.commit()
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail="Instituição não encontrada")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/cursos/")
def get_cursos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM cursos ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@app.post("/cursos/")
def add_curso(curso: NomeIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO cursos (nome) VALUES (%s) ON CONFLICT (nome) DO NOTHING", (curso.nome,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/cursos/{nome}")
def delete_curso(nome: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT curso_id FROM cursos WHERE nome = %s", (nome,))
        row = cur.fetchone()
        if row:
            curso_id = row[0]
            cur.execute("DELETE FROM carteirinhas WHERE curso_id = %s", (curso_id,))
            cur.execute("DELETE FROM cursos WHERE curso_id = %s", (curso_id,))
            conn.commit()
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail="Curso não encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/alunos/")
def get_alunos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT aluno_id, nome, email, cpf FROM alunos ORDER BY nome")
    results = cur.fetchall()
    cur.close()
    conn.close()
    # Retorna lista de dicionários, incluindo o id
    return [{"id": r[0], "nome": r[1], "email": r[2], "cpf": r[3]} for r in results]

@app.put("/alunos/{aluno_id}")
def update_aluno(aluno_id: int, aluno: dict):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE alunos SET nome=%s, email=%s, cpf=%s, data_nascimento=%s, rg=%s, telefone=%s WHERE aluno_id=%s
        """, (
            aluno.get("nome"),
            aluno.get("email"),
            aluno.get("cpf"),
            aluno.get("data_nascimento"),
            aluno.get("rg"),
            aluno.get("telefone"),
            aluno_id
        ))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/alunos/{aluno_id}")
def delete_aluno(aluno_id: int = Path(...)):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Excluir carteirinhas associadas antes de excluir o aluno
        cur.execute("DELETE FROM carteirinhas WHERE aluno_id = %s", (aluno_id,))
        cur.execute("DELETE FROM alunos WHERE aluno_id = %s", (aluno_id,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/relatorio/distritos/")
def relatorio_distritos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.nome, COUNT(c.carteirinha_id) AS alunos
        FROM distritos d
        LEFT JOIN carteirinhas c ON c.distrito_id = d.distrito_id
        GROUP BY d.nome
        ORDER BY d.nome
    """)
    data = [{"Distrito": row[0], "Alunos": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return data

@app.get("/relatorio/transportadores/")
def relatorio_transportadores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.nome, COUNT(c.carteirinha_id) AS alunos
        FROM transportadores t
        LEFT JOIN carteirinhas c ON c.transportador_id = t.transportador_id
        GROUP BY t.nome
        ORDER BY t.nome
    """)
    data = [{"Transportador": row[0], "Alunos": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return data

@app.get("/relatorio/dias/")
def relatorio_dias():
    conn = get_connection()
    cur = conn.cursor()
    # Considerando que dias_utilizacao é uma string separada por vírgula
    cur.execute("""
        SELECT unnest(string_to_array(dias_utilizacao, ',')) AS dia, COUNT(*) AS alunos
        FROM carteirinhas
        GROUP BY dia
        ORDER BY dia
    """)
    data = [{"Dia": row[0], "Alunos": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return data

@app.get("/relatorio/dias_distritos/")
def relatorio_dias_distritos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.nome as distrito, unnest(string_to_array(c.dias_utilizacao, ',')) as dia
        FROM carteirinhas c
        JOIN distritos d ON d.distrito_id = c.distrito_id
    """)
    data = [{"Distrito": row[0], "Dia": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return data