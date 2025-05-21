from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image
import os

def gerar_carteirinha_pdf(dados_aluno, foto_path, output_path):
    """
    Gera um PDF de carteirinha com os dados do aluno.
    
    Args:
        dados_aluno (dict): Dicionário com os dados do aluno (nome, RG, etc.)
        foto_path (str): Caminho para a foto do aluno
        output_path (str): Caminho onde salvar o PDF gerado
    """
    # Verificar se a foto existe
    if not os.path.exists(foto_path):
        raise FileNotFoundError(f"Arquivo de foto não encontrado: {foto_path}")
    
    # Criar o PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # TODO: Personalizar a carteirinha conforme o layout desejado
    
    c.save()
    return output_path
