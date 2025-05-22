from fastapi import APIRouter, HTTPException
from backend.db import get_connection

router = APIRouter()

@router.get("/carteirinha/dados/{carteirinha_id}")
def get_dados_carteirinha(carteirinha_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                a.nome, a.rg, a.telefone,
                i.nome as instituicao,
                d.nome as distrito,
                c.data_validade,
                c.dias_utilizacao
            FROM carteirinhas c
            JOIN alunos a ON a.aluno_id = c.aluno_id
            JOIN instituicoes i ON i.instituicao_id = c.instituicao_id
            JOIN distritos d ON d.distrito_id = c.distrito_id
            WHERE c.carteirinha_id = %s
        """, (carteirinha_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Carteirinha não encontrada")
        dados = {
            "nome": row[0],
            "rg": row[1],
            "telefone": row[2],
            "instituicao": row[3],
            "distrito": row[4],
            "data_validade": row[5],
            "dias": row[6]
        }
        return dados
    finally:
        cur.close()
        conn.close()

@router.get("/carteirinha/por_aluno/{aluno_id}")
def get_carteirinha_id_por_aluno(aluno_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT carteirinha_id FROM carteirinhas WHERE aluno_id = %s ORDER BY carteirinha_id DESC LIMIT 1", (aluno_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Carteirinha não encontrada para este aluno")
        return {"carteirinha_id": row[0]}
    finally:
        cur.close()
        conn.close()

@router.put("/carteirinha/{carteirinha_id}")
def update_carteirinha(carteirinha_id: int, dados: dict):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Buscar ids das tabelas relacionadas
        cur.execute("SELECT distrito_id FROM distritos WHERE nome=%s", (dados.get("distrito"),))
        distrito_id = cur.fetchone()[0]
        cur.execute("SELECT transportador_id FROM transportadores WHERE nome=%s", (dados.get("transportador"),))
        transportador_id = cur.fetchone()[0]
        cur.execute("SELECT instituicao_id FROM instituicoes WHERE nome=%s", (dados.get("instituicao"),))
        instituicao_id = cur.fetchone()[0]
        cur.execute("SELECT curso_id FROM cursos WHERE nome=%s", (dados.get("curso"),))
        curso_id = cur.fetchone()[0]
        cur.execute("""
            UPDATE carteirinhas SET
                distrito_id=%s,
                transportador_id=%s,
                instituicao_id=%s,
                curso_id=%s,
                periodo=%s,
                dias_utilizacao=%s,
                data_validade=%s,
                observacao=%s
            WHERE carteirinha_id=%s
        """, (
            distrito_id,
            transportador_id,
            instituicao_id,
            curso_id,
            dados.get("periodo"),
            ','.join(dados.get("dias", [])),
            dados.get("data_validade"),
            dados.get("observacao"),
            carteirinha_id
        ))
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
