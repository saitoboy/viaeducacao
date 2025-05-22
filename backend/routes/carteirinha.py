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
