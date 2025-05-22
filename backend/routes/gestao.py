from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db import get_connection

router = APIRouter()

class NomeIn(BaseModel):
    nome: str

@router.get("/distritos/")
def get_distritos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM distritos ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@router.post("/distritos/")
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

@router.delete("/distritos/{nome}")
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

# Transportadores
@router.get("/transportadores/")
def get_transportadores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM transportadores ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@router.post("/transportadores/")
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

@router.delete("/transportadores/{nome}")
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

# Instituições
@router.get("/instituicoes/")
def get_instituicoes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM instituicoes ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@router.post("/instituicoes/")
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

@router.delete("/instituicoes/{nome}")
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

# Cursos
@router.get("/cursos/")
def get_cursos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome FROM cursos ORDER BY nome")
    results = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

@router.post("/cursos/")
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

@router.delete("/cursos/{nome}")
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
