from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import os
from datetime import datetime
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import locale
import requests

def gerar_carteirinha_pdf(dados_aluno, foto_path, output_path=None):
    # Tamanho da carteirinha: 100mm x 60mm
    cart_width = 100 * mm  # 10cm
    cart_height = 70 * mm  # 6cm
    largura, altura = A4
    # Definir nome do arquivo de saída se não for passado
    if not output_path:
        nome = dados_aluno.get("nome", "").strip()
        if not nome:
            nome = "carteirinha"
        nome_arquivo = nome.replace(" ", "_").replace("/", "-") + "_Carteirinha"
        output_path = os.path.join("data", f"{nome_arquivo}.pdf")
    c = canvas.Canvas(output_path, pagesize=A4)

    # Centralizar carteirinha na página
    x0 = (largura - cart_width) / 2
    y0 = altura - 220 - cart_height  # margem superior ajustada

    # Cabeçalho com brasão à esquerda
    brasao_path = os.path.join("template", "03_brasao.png")
    brasao_img = None
    brasao_w, brasao_h = 60, 60
    header_top = altura-50
    if os.path.exists(brasao_path):
        brasao_img = ImageReader(brasao_path)
        c.drawImage(brasao_img, 60, header_top-brasao_h+10, width=brasao_w, height=brasao_h, mask='auto')
    # Texto do cabeçalho centralizado na página, com espaçamento igual ao modelo
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura / 2, altura - 60, "PREFEITURA MUNICIPAL DE MURIAÉ")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura / 2, altura - 80, "ESTADO DE MINAS GERAIS")
    c.drawCentredString(largura / 2, altura - 100, "SECRETARIA MUNICIPAL DE EDUCAÇÃO")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura / 2, altura - 150, "Emissão - Carteirinha do Transporte Escolar Noturno")

    # Retângulo da carteirinha
    c.setLineWidth(2)
    c.roundRect(x0, y0, cart_width, cart_height, 8, stroke=1, fill=0)
    # --- FIM DO RETÂNGULO DA CARTEIRINHA ---

    # --- ÁREA DA FOTO (esquerda) ---
    foto_w, foto_h = 30 * mm, 40 * mm
    foto_x = x0 + 8
    foto_y = y0 + cart_height - foto_h - 40
    if os.path.exists(foto_path):
        c.drawImage(foto_path, foto_x, foto_y, width=foto_w, height=foto_h, preserveAspectRatio=True, mask='auto')
    else:
        c.setDash(3,2)
        c.rect(foto_x, foto_y, foto_w, foto_h)
        c.setDash()

    # --- ÁREA DE DADOS DO ALUNO (direita da foto, dentro da caixa vermelha) ---
    # Cálculo para centralizar verticalmente o bloco de dados
    linhas_dados = 5  # NOME, RG/CONTATO, INSTITUIÇÃO, DISTRITO, VALIDADE
    altura_linha = 14
    bloco_dados_h = linhas_dados * altura_linha
    # Centralizar verticalmente na caixa da carteirinha
    centro_caixa = y0 + cart_height/2
    bloco_dados_y0 = centro_caixa + bloco_dados_h/2 - altura_linha + 8  # diminua o valor para descer o bloco
    text_x = foto_x + foto_w + 10  # X inicial dos dados
    text_y = bloco_dados_y0

    # --- CABEÇALHO DENTRO DA CAIXA DA CARTEIRINHA ---
    # Posição do brasão pequeno centralizado acima dos dados
    header_brasao_w, header_brasao_h = 18, 18
    header_brasao_x = text_x + 80  # ajuste para centralizar acima dos dados
    header_brasao_y = bloco_dados_y0 + altura_linha * 2.5  # um pouco acima do topo dos dados
    if os.path.exists(brasao_path):
        c.drawImage(brasao_path, header_brasao_x, header_brasao_y, width=header_brasao_w, height=header_brasao_h, mask='auto')

    # Títulos centralizados acima dos dados
    header_font_size = 6
    header_texts = [
        "SECRETARIA MUNICIPAL DE EDUCAÇÃO",
        "CARTEIRINHA TRANSPORTE ESCOLAR"
    ]
    header_text_y = header_brasao_y - 2  # logo abaixo do brasão
    for i, line in enumerate(header_texts):
        c.setFont("Helvetica-Bold", header_font_size)
        c.drawCentredString(header_brasao_x + header_brasao_w/2, header_text_y - (i+1)*(header_font_size+1), line)
    # --- FIM DO CABEÇALHO DENTRO DA CAIXA ---

    # NOME
    c.setFont("Helvetica-Bold", 8)
    c.drawString(text_x, text_y, "NOME:")
    c.setFont("Helvetica", 8)
    c.drawString(text_x+28, text_y, dados_aluno.get("nome", "").upper())
    text_y -= altura_linha  # sem padding extra

    # RG
    c.setFont("Helvetica-Bold", 8)
    c.drawString(text_x, text_y, "RG:")
    c.setFont("Helvetica", 8)
    c.drawString(text_x+16, text_y, dados_aluno.get("rg", ""))
    text_y -= altura_linha  # sem padding extra

    # CONTATO
    c.setFont("Helvetica-Bold", 8)
    c.drawString(text_x, text_y, "CONTATO:")
    c.setFont("Helvetica", 8)
    c.drawString(text_x+45, text_y, dados_aluno.get("telefone", ""))
    text_y -= altura_linha  # sem padding extra

    # INSTITUIÇÃO DE ENSINO
    c.setFont("Helvetica-Bold", 7)
    c.drawString(text_x, text_y, "INSTITUIÇÃO DE ENSINO:")
    c.setFont("Helvetica", 7)
    c.drawString(text_x+90, text_y, dados_aluno.get("instituicao", ""))
    text_y -= altura_linha  # sem padding extra

    # DISTRITO/LOCALIDADE
    c.setFont("Helvetica-Bold", 7)
    c.drawString(text_x, text_y, "DISTRITO/LOCALIDADE:")
    text_y -= altura_linha  # move para a linha de baixo
    c.setFont("Helvetica", 7)
    c.drawString(text_x, text_y, dados_aluno.get("distrito", ""))
    text_y -= altura_linha  # sem padding extra

    # DATA DE VALIDADE (caixa cinza)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(text_x, text_y, "DATA DE VALIDADE:")
    c.setFont("Helvetica-Bold", 9)
    data_validade = dados_aluno.get("data_validade", "")
    if data_validade:
        try:
            data_validade_fmt = datetime.strptime(data_validade[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
        except Exception:
            data_validade_fmt = data_validade
    else:
        data_validade_fmt = ""
    # Caixa cinza para validade
    c.setFillGray(0.85)
    c.rect(text_x+82, text_y-2, 60, 13, fill=1, stroke=0)
    c.setFillGray(0)
    c.drawString(text_x+85, text_y, data_validade_fmt)
    # --- FIM DA ÁREA DE DADOS DO ALUNO ---

    # --- RODAPÉ DA CARTEIRINHA (linha verde: dias de utilização e validade) ---
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x0+8, y0+23, "DIAS DE UTILIZAÇÃO:")
    c.setFont("Helvetica", 8)
    dias = dados_aluno.get("dias", "")
    if isinstance(dias, list):
        dias_str = ", ".join(dias)
    else:
        dias_str = str(dias)
    # Coloca os dias embaixo do label
    c.drawString(x0+8, y0+10, dias_str)
    # --- FIM DO RODAPÉ ---

    # Texto informativo e observação (ajuste de espaçamento para igualar ao modelo)
    bloco_width = 140 * mm  # largura máxima do bloco de texto
    bloco_x = (largura - bloco_width) / 2
    bloco_y = y0 - 30  # 3cm abaixo da carteirinha

    # Definir locale para data em português
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR')
        except locale.Error:
            pass  # Se não conseguir, segue padrão do sistema

    # Gerar data no formato desejado, sempre com mês capitalizado
    data_hoje = datetime.now().strftime('%d de %B de %Y')
    data_hoje = data_hoje[0:6] + data_hoje[6:].capitalize()  # força inicial maiúscula no mês

    # Definir estilo para o texto justificado
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        'Justify',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        alignment=4,  # Justificado
        leftIndent=0,
        rightIndent=0,
        spaceAfter=0,
        spaceBefore=0,
    )

    texto_info = (
        "A Carteirinha de Transporte Escolar deverá ser plastificada e apresentada ao motorista do Transporte, durante a utilização que deverá respeitar os dias autorizados.\n\n"
        f"Muriaé, {data_hoje}\n\n"
        "Observação:"
    )
    p = Paragraph(texto_info.replace('\n', '<br/>'), style)
    frame = Frame(bloco_x, bloco_y-100, bloco_width, 100, showBoundary=0)  # aumentei altura do frame
    frame.addFromList([p], c)

    # Espaço de 2,5cm (25mm) abaixo do texto informativo
    y_declaracao = bloco_y-100-25*mm
    c.setFont("Helvetica", 10)
    c.drawCentredString(largura/2, y_declaracao, "Declaro ter recebido a Carteirinha do Transporte Escolar.")

    # Espaço de 2,5cm (25mm) abaixo da declaração para assinatura
    y_assinatura = y_declaracao-25*mm
    c.line(largura/2-40*mm, y_assinatura, largura/2+40*mm, y_assinatura)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(largura/2, y_assinatura-15, dados_aluno.get("nome", "").upper())

    # Rodapé
    c.setFont("Helvetica", 8)
    c.drawCentredString(largura/2, 40, "Av. Maestro Sansão, 236 - Centro, Muriaé/MG - 1º Andar - Tel.: (32) 3696-3388")
    c.setFont("Helvetica", 7)
    c.drawRightString(largura-40, 25, f"Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.save()
    return output_path

def gerar_carteirinha_pdf_por_id(carteirinha_id, foto_path, output_path=None):
    # Buscar dados completos da API
    url = f"http://localhost:8000/carteirinha/dados/{carteirinha_id}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Erro ao buscar dados da carteirinha: {resp.text}")
    dados_aluno = resp.json()
    return gerar_carteirinha_pdf(dados_aluno, foto_path, output_path)
