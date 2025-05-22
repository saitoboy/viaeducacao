from fastapi import APIRouter, HTTPException, Path
from backend.db import get_connection

router = APIRouter()

@router.get("/alunos/")
def get_alunos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT aluno_id, nome, email, cpf FROM alunos ORDER BY nome")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nome": r[1], "email": r[2], "cpf": r[3]} for r in results]

@router.put("/alunos/{aluno_id}")
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

@router.delete("/alunos/{aluno_id}")
def delete_aluno(aluno_id: int = Path(...)):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM carteirinhas WHERE aluno_id = %s", (aluno_id,))
        cur.execute("DELETE FROM alunos WHERE aluno_id = %s", (aluno_id,))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
