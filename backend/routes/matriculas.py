from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db import get_connection

router = APIRouter()

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

@router.post("/carteirinha/")
def criar_carteirinha(dados: CarteirinhaIn):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO alunos (nome, email, cpf, data_nascimento, rg, telefone)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING aluno_id
        """, (dados.nome, dados.email, dados.cpf, dados.data_nasc, dados.rg, dados.telefone))
        aluno_id = cur.fetchone()[0]
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
