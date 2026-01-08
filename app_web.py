import streamlit as st
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.units import cm

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Kalluan Cartoon CV Generator", page_icon="📄", layout="wide")

# --- BARRA LATERAL (Configurações) ---
with st.sidebar:
    st.title("🎨 Design do Currículo")
    st.write("Personalize a aparência do documento.")
    
    tema_estilo = st.radio("Escolha o Estilo:", ["Moderno", "Clássico Executivo"])
    
    cor_tema = st.color_picker("Cor Principal:", "#003366")
    
    st.info("ℹ️ Este sistema gera um PDF profissional baseado em Python/ReportLab rodando em nuvem.")

# --- ÁREA PRINCIPAL (Formulário) ---
st.title("📄 Gerador de Currículo SaaS")
st.markdown("**Desenvolvido por Kalluan Cartoon**")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Dados Pessoais")
    nome = st.text_input("Nome Completo")
    titulo = st.text_input("Cargo / Título")
    contato = st.text_input("Contato")
    links = st.text_input("Links", "GitHub")

with col2:
    st.subheader("2. Resumo Profissional")
    resumo = st.text_area("Resumo", height=150)

st.subheader("3. Experiência e Projetos")
projeto = st.text_area("Projeto Destaque (Nephrodiag)", height=150)

experiencia = st.text_area("Experiência Profissional", height=150)

formacao = st.text_area("Formação & Skills",  height=100)

# --- LÓGICA DE GERAÇÃO (Back-end) ---
def gerar_pdf_na_memoria():
    buffer = io.BytesIO()  # Cria um arquivo na memória RAM
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Define cores baseadas na escolha do usuário
    cor_titulo = colors.HexColor(cor_tema) if tema_estilo == "Moderno" else colors.black
    
    # Estilos
    style_nome = ParagraphStyle('Nome', parent=styles['Heading1'], fontSize=20, textColor=cor_titulo, alignment=1, spaceAfter=8)
    style_cargo = ParagraphStyle('Cargo', parent=styles['Normal'], fontSize=12, textColor=colors.grey, alignment=1, spaceAfter=8)
    style_contato = ParagraphStyle('Contato', parent=styles['Normal'], fontSize=9, alignment=1)
    
    style_secao = ParagraphStyle('Secao', parent=styles['Heading2'], fontSize=13, textColor=cor_titulo, spaceBefore=15, spaceAfter=6, textTransform='uppercase')
    if tema_estilo == "Clássico Executivo":
        style_secao.textColor = colors.black
        style_secao.fontName = "Times-Bold"
        
    style_texto = ParagraphStyle('Texto', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6, alignment=4)

    # Conteúdo
    story.append(Paragraph(nome, style_nome))
    story.append(Paragraph(titulo, style_cargo))
    story.append(Paragraph(contato, style_contato))
    story.append(Paragraph(links, style_contato))
    story.append(HRFlowable(width="100%", thickness=1, color=cor_titulo, spaceBefore=5, spaceAfter=15))
    
    sections = [
        ("Resumo Profissional", resumo),
        ("Projetos & Inovação", projeto),
        ("Experiência Profissional", experiencia),
        ("Formação & Competências", formacao)
    ]
    
    for title, content in sections:
        story.append(Paragraph(title, style_secao))
        # Converte quebras de linha do input para <br/> do PDF
        content_formatted = content.replace('\n', '<br/>')
        story.append(Paragraph(content_formatted, style_texto))
        
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- BOTÃO DE DOWNLOAD ---
st.markdown("---")
st.write("### 🚀 Finalizar")

if st.button("Gerar Prévia e Preparar Download"):
    try:
        pdf_buffer = gerar_pdf_na_memoria()
        
        st.success("PDF Gerado com Sucesso! Baixe abaixo:")
        
        st.download_button(
            label="⬇️ Baixar Currículo PDF",
            data=pdf_buffer,
            file_name="Curriculo_generator.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Erro ao gerar: {e}")