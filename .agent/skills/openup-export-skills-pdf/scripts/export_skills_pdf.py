#!/usr/bin/env python3
"""
export_skills_pdf.py
--------------------
Genera un PDF con la documentación completa de todas las skills del repositorio.
Usa ReportLab para generación directa y robusta de PDF.

Uso:
    python export_skills_pdf.py [--skills-dir DIR] [--output FILE] [--title TITLE] [--extra-dir DIR]

Dependencias:
    pip install reportlab markdown
"""

import argparse
import os
import sys
import re
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Importaciones con mensajes de error descriptivos
# ---------------------------------------------------------------------------
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, HRFlowable, KeepTogether
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus.tableofcontents import TableOfContents
except ImportError:
    print("ERROR: Falta la librería 'reportlab'. Instálala con: pip install reportlab")
    sys.exit(1)

try:
    import markdown
    import html as htmlmod
    from html.parser import HTMLParser
except ImportError:
    print("ERROR: Falta la librería 'markdown'. Instálala con: pip install markdown")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Paleta de colores
# ---------------------------------------------------------------------------
COLOR_PRIMARY   = HexColor("#0f3460")
COLOR_SECONDARY = HexColor("#16213e")
COLOR_ACCENT    = HexColor("#e94560")
COLOR_LIGHT_BG  = HexColor("#f0f4f8")
COLOR_BORDER    = HexColor("#d0dce8")
COLOR_TEXT      = HexColor("#1a1a2e")
COLOR_MUTED     = HexColor("#666666")
COLOR_CODE_BG   = HexColor("#1a1a2e")
COLOR_CODE_TEXT = HexColor("#e0e0e0")


# ---------------------------------------------------------------------------
# Parseo de frontmatter YAML simple
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple:
    """Extrae el frontmatter YAML y el cuerpo Markdown de un SKILL.md."""
    meta = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_meta = parts[1].strip()
            body = parts[2].strip()
            for line in raw_meta.splitlines():
                line = line.strip()
                if ":" in line and not line.startswith("#"):
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value and not value.startswith("{"):
                        meta[key] = value
    return meta, body


# ---------------------------------------------------------------------------
# Escaneo de skills
# ---------------------------------------------------------------------------

def scan_skills(skills_dir: Path) -> list:
    """Escanea un directorio y retorna lista de skills con sus metadatos."""
    skills = []
    if not skills_dir.exists():
        print(f"AVISO: Directorio no existe: {skills_dir}")
        return skills

    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir():
            continue
        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            print(f"  AVISO: {item.name} sin SKILL.md — omitido")
            continue

        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  AVISO: No se pudo leer {skill_md}: {e}")
            continue

        meta, body = parse_frontmatter(content)
        skills.append({
            "dir": item.name,
            "name": meta.get("name", item.name),
            "description": meta.get("description", "Sin descripción"),
            "license": meta.get("license", ""),
            "compatibility": meta.get("compatibility", ""),
            "version": meta.get("version", ""),
            "author": meta.get("author", ""),
            "body": body,
            "meta": meta,
        })
        print(f"  ✓ {item.name}")

    return skills


# ---------------------------------------------------------------------------
# Conversión de Markdown a texto simple para ReportLab
# ---------------------------------------------------------------------------

class HTMLToReportLab(HTMLParser):
    """Convierte HTML simple a elementos de texto para ReportLab."""
    
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.current_tags = []
        self.in_code = False
        self.in_pre = False
        self.skip_tags = {"style", "script"}
        self.in_skip = False
        self.buffer = ""
    
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.in_skip = True
        self.current_tags.append(tag)
        if tag == "code":
            self.in_code = True
        elif tag == "pre":
            self.in_pre = True
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.in_skip = False
        if self.current_tags and self.current_tags[-1] == tag:
            self.current_tags.pop()
        if tag == "code":
            self.in_code = False
        elif tag == "pre":
            self.in_pre = False
    
    def handle_data(self, data):
        if self.in_skip:
            return
        self.text_parts.append(data)
    
    def get_text(self):
        return "".join(self.text_parts)


def md_to_plain(md_text: str) -> str:
    """Convierte Markdown a texto plano."""
    parser = HTMLToReportLab()
    md_obj = markdown.Markdown(extensions=["tables", "fenced_code"])
    html = md_obj.convert(md_text)
    parser.feed(html)
    return parser.get_text()


def parse_markdown_blocks(md_text: str, styles: dict) -> list:
    """
    Convierte Markdown a lista de flowables de ReportLab.
    Procesamiento línea por línea para mayor control.
    Cada elemento se envuelve en try/except para robustez.
    """
    elements = []
    lines = md_text.splitlines()
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        try:
            # ── Bloque de código ──
            if line.strip().startswith("```"):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                code_text = "\n".join(code_lines)
                if code_text.strip():
                    elements.append(Spacer(1, 4))
                    safe_code = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    elements.append(
                        Paragraph(
                            f'<font name="Courier" size="7" color="#e0e0e0">{safe_code.replace(chr(10), "<br/>")}</font>',
                            styles["code_block"]
                        )
                    )
                    elements.append(Spacer(1, 4))
                i += 1
                continue
            
            # ── H1 ──
            if line.startswith("# ") and not line.startswith("## "):
                text = clean_inline(line[2:].strip())
                if text:
                    elements.append(Spacer(1, 8))
                    elements.append(Paragraph(text, styles["h1"]))
                    elements.append(HRFlowable(color=COLOR_PRIMARY, thickness=1, width="100%"))
                    elements.append(Spacer(1, 4))
            
            # ── H2 ──
            elif line.startswith("## ") and not line.startswith("### "):
                text = clean_inline(line[3:].strip())
                if text:
                    elements.append(Spacer(1, 6))
                    elements.append(Paragraph(text, styles["h2"]))
                    elements.append(Spacer(1, 3))
            
            # ── H3 ──
            elif line.startswith("### ") and not line.startswith("#### "):
                text = clean_inline(line[4:].strip())
                if text:
                    elements.append(Spacer(1, 4))
                    elements.append(Paragraph(text, styles["h3"]))
            
            # ── H4 ──
            elif line.startswith("#### "):
                text = clean_inline(line[5:].strip())
                if text:
                    elements.append(Spacer(1, 3))
                    elements.append(Paragraph(text, styles["h4"]))
            
            # ── Lista ──
            elif line.strip().startswith("- ") or line.strip().startswith("* "):
                text = clean_inline(line.strip()[2:].strip())
                if text:
                    elements.append(Paragraph(f"• {text}", styles["bullet"]))
            
            elif re.match(r"^\d+\.\s", line.strip()):
                text = clean_inline(re.sub(r"^\d+\.\s", "", line.strip()))
                if text:
                    elements.append(Paragraph(f"  {text}", styles["bullet"]))
            
            # ── Tabla ──
            elif "|" in line and line.strip().startswith("|"):
                table_lines = []
                while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                    table_lines.append(lines[i])
                    i += 1
                table_el = build_table(table_lines, styles)
                if table_el:
                    elements.append(Spacer(1, 6))
                    elements.append(table_el)
                    elements.append(Spacer(1, 6))
                continue  # ya incrementamos i
            
            # ── Línea horizontal ──
            elif line.strip() in ("---", "***", "___"):
                elements.append(HRFlowable(color=COLOR_BORDER, thickness=0.5, width="100%"))
            
            # ── Línea en blanco ──
            elif not line.strip():
                elements.append(Spacer(1, 4))
            
            # ── Párrafo normal ──
            else:
                text = clean_inline(line.strip())
                if text:
                    elements.append(Paragraph(text, styles["body_text"]))
        
        except Exception as e:
            # Si una línea falla, la emitimos como texto plano escapado
            safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            try:
                elements.append(Paragraph(safe_line, styles["body_text"]))
            except Exception:
                pass  # ignorar líneas irrecuperables
        
        i += 1
    
    return elements


def clean_inline(text: str) -> str:
    """Convierte formato Markdown inline a tags ReportLab.
    
    Procesa en orden seguro para evitar anidamiento de tags XML inválido:
    1. Extrae backtick code spans como placeholders
    2. Aplica negrita/cursiva
    3. Restaura code spans al final
    """
    if not text:
        return text
    
    # Escapar caracteres XML primero
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 1. Extraer `código` como placeholders para evitar conflictos de anidamiento
    code_spans = []
    def _save_code(m):
        idx = len(code_spans)
        code_content = m.group(1)
        code_spans.append(code_content)
        return f"\x00CODE{idx}\x00"
    
    text = re.sub(r"`(.+?)`", _save_code, text)
    
    # 2. Procesar [link](url) — mostrar solo el texto
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    
    # 3. **negrita**
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # 4. *cursiva*
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    
    # 5. Restaurar code spans como <font> tags (ahora fuera de <b>/<i>)
    for idx, code_content in enumerate(code_spans):
        text = text.replace(
            f"\x00CODE{idx}\x00",
            f'<font name="Courier" size="8" color="#0f3460">{code_content}</font>'
        )
    
    return text


def build_table(lines: list, styles: dict):
    """Construye una tabla ReportLab desde líneas Markdown."""
    rows = []
    for line in lines:
        if re.match(r"^\|[\s:|-]+\|$", line.strip()):
            continue  # separador de encabezado
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells:
            rows.append(cells)
    
    if not rows:
        return None
    
    # Normalizar ancho de columnas
    max_cols = max(len(r) for r in rows)
    norm_rows = [r + [""] * (max_cols - len(r)) for r in rows]
    
    # Convertir celdas a Paragraphs
    para_rows = []
    for ri, row in enumerate(norm_rows):
        para_row = []
        for cell in row:
            style = styles["table_header"] if ri == 0 else styles["table_cell"]
            text = clean_inline(cell) if cell else ""
            para_row.append(Paragraph(text, style))
        para_rows.append(para_row)
    
    table = Table(para_rows, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, COLOR_LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


# ---------------------------------------------------------------------------
# Estilos ReportLab
# ---------------------------------------------------------------------------

def build_styles() -> dict:
    base = getSampleStyleSheet()
    
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            fontSize=36, fontName="Helvetica-Bold",
            textColor=COLOR_PRIMARY, spaceAfter=10,
            alignment=TA_CENTER, leading=44,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            fontSize=14, fontName="Helvetica",
            textColor=COLOR_SECONDARY, spaceAfter=6,
            alignment=TA_CENTER,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            fontSize=10, fontName="Helvetica",
            textColor=COLOR_MUTED, spaceAfter=4,
            alignment=TA_CENTER,
        ),
        "toc_title": ParagraphStyle(
            "TocTitle",
            fontSize=22, fontName="Helvetica-Bold",
            textColor=COLOR_PRIMARY, spaceAfter=16,
            spaceBefore=8,
        ),
        "toc_entry": ParagraphStyle(
            "TocEntry",
            fontSize=9.5, fontName="Helvetica-Bold",
            textColor=COLOR_TEXT, spaceBefore=5, spaceAfter=1,
            leftIndent=0,
        ),
        "toc_desc": ParagraphStyle(
            "TocDesc",
            fontSize=8, fontName="Helvetica",
            textColor=COLOR_MUTED, spaceAfter=4,
            leftIndent=20,
        ),
        "skill_number": ParagraphStyle(
            "SkillNumber",
            fontSize=8, fontName="Helvetica",
            textColor=white, spaceAfter=2,
            leading=10,
        ),
        "skill_name": ParagraphStyle(
            "SkillName",
            fontSize=22, fontName="Helvetica-Bold",
            textColor=white, spaceAfter=4,
            leading=26,
        ),
        "skill_desc": ParagraphStyle(
            "SkillDesc",
            fontSize=10, fontName="Helvetica",
            textColor=HexColor("#ddeeff"), spaceAfter=0,
            leading=14,
        ),
        "meta_label": ParagraphStyle(
            "MetaLabel",
            fontSize=8.5, fontName="Helvetica-Bold",
            textColor=COLOR_PRIMARY,
        ),
        "meta_value": ParagraphStyle(
            "MetaValue",
            fontSize=8.5, fontName="Helvetica",
            textColor=COLOR_TEXT,
        ),
        "h1": ParagraphStyle(
            "H1", fontSize=16, fontName="Helvetica-Bold",
            textColor=COLOR_PRIMARY, spaceBefore=10, spaceAfter=4,
        ),
        "h2": ParagraphStyle(
            "H2", fontSize=13, fontName="Helvetica-Bold",
            textColor=COLOR_SECONDARY, spaceBefore=8, spaceAfter=3,
            borderPad=4, borderColor=COLOR_PRIMARY,
        ),
        "h3": ParagraphStyle(
            "H3", fontSize=11, fontName="Helvetica-Bold",
            textColor=COLOR_PRIMARY, spaceBefore=6, spaceAfter=2,
        ),
        "h4": ParagraphStyle(
            "H4", fontSize=10, fontName="Helvetica-Bold",
            textColor=COLOR_TEXT, spaceBefore=4, spaceAfter=2,
        ),
        "body_text": ParagraphStyle(
            "BodyText", fontSize=9.5, fontName="Helvetica",
            textColor=COLOR_TEXT, spaceBefore=2, spaceAfter=2,
            leading=14, alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "Bullet", fontSize=9.5, fontName="Helvetica",
            textColor=COLOR_TEXT, spaceBefore=1, spaceAfter=1,
            leftIndent=12, leading=13,
        ),
        "code_block": ParagraphStyle(
            "CodeBlock", fontSize=7.5, fontName="Courier",
            textColor=COLOR_CODE_TEXT, spaceBefore=4, spaceAfter=4,
            backColor=COLOR_CODE_BG, leading=11,
            leftIndent=10, rightIndent=10,
            borderPad=8,
        ),
        "table_header": ParagraphStyle(
            "TableHeader", fontSize=8, fontName="Helvetica-Bold",
            textColor=white,
        ),
        "table_cell": ParagraphStyle(
            "TableCell", fontSize=8, fontName="Helvetica",
            textColor=COLOR_TEXT, leading=11,
        ),
    }


# ---------------------------------------------------------------------------
# Callbacks de página para encabezado/pie
# ---------------------------------------------------------------------------

def make_page_template(title: str):
    def on_first_page(canvas, doc):
        pass  # portada sin encabezado/pie
    
    def on_later_pages(canvas, doc):
        canvas.saveState()
        w, h = A4
        # Línea superior
        canvas.setStrokeColor(COLOR_PRIMARY)
        canvas.setLineWidth(1.5)
        canvas.line(1.5*cm, h - 1.2*cm, w - 1.5*cm, h - 1.2*cm)
        # Título en encabezado
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(COLOR_MUTED)
        canvas.drawString(1.5*cm, h - 1.0*cm, title)
        # Número de página
        canvas.drawRightString(w - 1.5*cm, h - 1.0*cm, f"Página {doc.page}")
        # Línea inferior
        canvas.setLineWidth(0.5)
        canvas.line(1.5*cm, 1.2*cm, w - 1.5*cm, 1.2*cm)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(1.5*cm, 0.88*cm, "Agent Skills — Documentación Completa")
        canvas.restoreState()
    
    return on_first_page, on_later_pages


# ---------------------------------------------------------------------------
# Construcción del documento PDF
# ---------------------------------------------------------------------------

def build_pdf(skills: list, output_path: Path, title: str, generated_at: str):
    styles = build_styles()
    on_first, on_later = make_page_template(title)
    
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.0*cm, bottomMargin=2.0*cm,
        title=title,
        author="OpenUP Agent Skills",
        subject="Documentación completa de skills",
        creator="openup-export-skills-pdf"
    )
    
    story = []
    total = len(skills)
    
    # ══════════════════════════════════════════
    # PORTADA
    # ══════════════════════════════════════════
    story.append(Spacer(1, 3*cm))
    
    # Banner de color
    banner_data = [[Paragraph(
        f'<font color="white" size="36"><b>{title}</b></font>',
        styles["cover_title"]
    )]]
    banner = Table(banner_data, colWidths=[doc.width])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_PRIMARY),
        ("TOPPADDING", (0, 0), (-1, -1), 30),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 30),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    story.append(banner)
    story.append(Spacer(1, 0.8*cm))
    
    story.append(Paragraph("Documentación completa del catálogo de skills del proyecto", styles["cover_subtitle"]))
    story.append(Spacer(1, 0.5*cm))
    
    # Badge de total
    badge_data = [[Paragraph(
        f'<font color="white" size="14"><b>{total} skills documentadas</b></font>',
        ParagraphStyle("Badge", alignment=TA_CENTER)
    )]]
    badge = Table(badge_data, colWidths=[8*cm], hAlign="CENTER")
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_ACCENT),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [20, 20, 20, 20]),
    ]))
    story.append(badge)
    story.append(Spacer(1, 2*cm))
    
    story.append(HRFlowable(color=COLOR_PRIMARY, thickness=2, width="100%"))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"Generado el {generated_at}", styles["cover_meta"]))
    story.append(Paragraph("OpenUP Framework · Agent Skills", styles["cover_meta"]))
    
    story.append(PageBreak())
    
    # ══════════════════════════════════════════
    # TABLA DE CONTENIDOS
    # ══════════════════════════════════════════
    story.append(Paragraph("Tabla de Contenidos", styles["toc_title"]))
    story.append(HRFlowable(color=COLOR_PRIMARY, thickness=2, width="100%"))
    story.append(Spacer(1, 0.4*cm))
    
    toc_rows = []
    for i, skill in enumerate(skills, 1):
        desc = skill["description"]
        if len(desc) > 120:
            desc = desc[:120] + "…"
        
        row_data = [[
            Paragraph(f'<b>{i}.</b>', styles["toc_entry"]),
            Paragraph(f'<b>{skill["name"]}</b>', styles["toc_entry"]),
        ]]
        toc_rows.append(row_data[0])
        
        desc_row = [
            Paragraph("", styles["toc_desc"]),
            Paragraph(desc, styles["toc_desc"]),
        ]
        toc_rows.append(desc_row)
    
    if toc_rows:
        toc_table = Table(toc_rows, colWidths=[0.8*cm, doc.width - 0.8*cm])
        toc_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, COLOR_BORDER),
        ]))
        story.append(toc_table)
    
    story.append(PageBreak())
    
    # ══════════════════════════════════════════
    # SECCIONES POR SKILL
    # ══════════════════════════════════════════
    for i, skill in enumerate(skills, 1):
        # Encabezado de la skill (tabla con fondo de color)
        header_data = [[
            Paragraph(f"SKILL {i} DE {total}", styles["skill_number"]),
        ], [
            Paragraph(skill["name"], styles["skill_name"]),
        ], [
            Paragraph(skill["description"], styles["skill_desc"]),
        ]]
        
        header_table = Table(header_data, colWidths=[doc.width])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_PRIMARY),
            ("TOPPADDING", (0, 0), (0, 0), 14),
            ("TOPPADDING", (0, 1), (0, 2), 3),
            ("BOTTOMPADDING", (0, 2), (-1, -1), 14),
            ("LEFTPADDING", (0, 0), (-1, -1), 16),
            ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ]))
        story.append(header_table)
        
        # Metadatos
        meta_rows = []
        if skill.get("license"):
            meta_rows.append(["Licencia", skill["license"]])
        if skill.get("compatibility"):
            meta_rows.append(["Compatibilidad", skill["compatibility"]])
        if skill.get("version"):
            meta_rows.append(["Versión", skill["version"]])
        if skill.get("author"):
            meta_rows.append(["Autor", skill["author"]])
        meta_rows.append(["Directorio", skill["dir"]])
        
        meta_para_rows = [[
            Paragraph(label, styles["meta_label"]),
            Paragraph(val, styles["meta_value"]),
        ] for label, val in meta_rows]
        
        meta_table = Table(meta_para_rows, colWidths=[3.5*cm, doc.width - 3.5*cm])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_LIGHT_BG),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("LINEBELOW", (0, 0), (-1, -2), 0.3, COLOR_BORDER),
            ("BOX", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.4*cm))
        
        # Contenido del SKILL.md
        if skill["body"].strip():
            body_elements = parse_markdown_blocks(skill["body"], styles)
            story.extend(body_elements)
        
        # Separador al final (excepto la última)
        story.append(Spacer(1, 0.5*cm))
        if i < total:
            story.append(HRFlowable(
                color=COLOR_ACCENT, thickness=1.5, width="100%",
                spaceAfter=0.3*cm
            ))
            story.append(PageBreak())
    
    # ── Generar ──
    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)


# ---------------------------------------------------------------------------
# Entrada principal
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Genera un PDF con la documentación de todas las skills del repositorio."
    )
    parser.add_argument("--skills-dir", default=".agents/skills",
                        help="Directorio principal de skills")
    parser.add_argument("--extra-dir", default=None,
                        help="Directorio adicional de skills (opcional)")
    parser.add_argument("--output", default="docs/skills-documentation.pdf",
                        help="Ruta del PDF de salida")
    parser.add_argument("--title", default="Catálogo de Agent Skills",
                        help="Título del documento")
    args = parser.parse_args()

    now = datetime.datetime.now()
    generated_at = now.strftime("%d/%m/%Y a las %H:%M")

    print(f"\n{'='*60}")
    print(f"  {args.title}")
    print(f"  Generado: {generated_at}")
    print(f"{'='*60}\n")

    cwd = Path.cwd()
    skills_dir = cwd / args.skills_dir
    output_path = cwd / args.output

    print(f"📂 Escaneando: {skills_dir}")
    skills = scan_skills(skills_dir)

    if args.extra_dir:
        extra_dir = cwd / args.extra_dir
        print(f"\n📂 Escaneando adicional: {extra_dir}")
        existing_names = {s["name"] for s in skills}
        for s in scan_skills(extra_dir):
            if s["name"] not in existing_names:
                skills.append(s)
                existing_names.add(s["name"])
            else:
                print(f"  → Omitida (duplicada): {s['name']}")

    if not skills:
        print("\nERROR: No se encontraron skills.")
        sys.exit(1)

    print(f"\n✅ Total de skills: {len(skills)}")
    print(f"\n📄 Generando PDF en: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    build_pdf(skills, output_path, args.title, generated_at)

    size_kb = output_path.stat().st_size / 1024
    print(f"\n🎉 ¡PDF generado correctamente!")
    print(f"   Ruta: {output_path}")
    print(f"   Tamaño: {size_kb:.1f} KB")
    print(f"   Skills documentadas: {len(skills)}")


if __name__ == "__main__":
    main()
