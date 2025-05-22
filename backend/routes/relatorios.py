from fastapi import APIRouter
from backend.db import get_connection

router = APIRouter()

@router.get("/relatorio/distritos/")
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

@router.get("/relatorio/transportadores/")
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

@router.get("/relatorio/dias/")
def relatorio_dias():
    conn = get_connection()
    cur = conn.cursor()
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

@router.get("/relatorio/dias_distritos/")
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
