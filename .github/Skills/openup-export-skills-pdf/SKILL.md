---
name: openup-export-skills-pdf
description: Genera un documento PDF con la documentación completa de todas las skills del repositorio. Escanea los directorios de skills, extrae metadatos y contenido SKILL.md, y los compila en un PDF estructurado con portada, índice y sección por skill. Usar cuando se necesite documentar, compartir o revisar el catálogo completo de skills del proyecto.
license: Apache-2.0
compatibility: Requires Python 3.8+. Install dependencies with: pip install markdown xhtml2pdf
metadata:
  author: openup-team
  version: "1.0"
---

# openup-export-skills-pdf

Genera un PDF con la documentación completa de todas las skills del repositorio.

## Cuándo usar esta skill

- El usuario pide "documentar las skills", "exportar skills a PDF" o "generar catálogo de skills"
- Se necesita un documento imprimible o compartible del catálogo de skills
- Se quiere revisar visualmente el estado de todas las skills

## Dependencias

Instala antes de ejecutar:

```bash
pip install markdown xhtml2pdf
```

## Ejecución

### Uso básico

```bash
python .agents/skills/openup-export-skills-pdf/scripts/export_skills_pdf.py
```

Genera `docs/skills-documentation.pdf` escaneando `.agents/skills/`.

### Opciones

```bash
python scripts/export_skills_pdf.py \
  --skills-dir <ruta_al_directorio_de_skills> \
  --output <ruta_de_salida.pdf> \
  --title "Catálogo de Skills" \
  --extra-dir <directorio_adicional>
```

| Argumento | Por defecto | Descripción |
|-----------|-------------|-------------|
| `--skills-dir` | `.agents/skills` | Directorio principal de skills |
| `--output` | `docs/skills-documentation.pdf` | Ruta del PDF generado |
| `--title` | `Catálogo de Agent Skills` | Título del documento |
| `--extra-dir` | *(ninguno)* | Directorio adicional de skills a incluir |

### Ejemplo con ambos directorios de skills

```bash
python .agents/skills/openup-export-skills-pdf/scripts/export_skills_pdf.py \
  --skills-dir .agents/skills \
  --extra-dir .github/skills \
  --output docs/skills-documentation.pdf
```

## Contenido del PDF generado

1. **Portada** — Título, fecha de generación y número total de skills
2. **Tabla de contenidos** — Listado con nombre y descripción breve de cada skill
3. **Secciones por skill** — Para cada skill:
   - Nombre y descripción
   - Metadatos del frontmatter (compatibility, license, version, etc.)
   - Cuerpo completo del SKILL.md renderizado
4. **Pie de página** — Número de página y nombre del documento

## Gestión de errores

| Error | Acción |
|-------|--------|
| `ModuleNotFoundError: markdown` | Ejecutar `pip install markdown xhtml2pdf` |
| `ModuleNotFoundError: xhtml2pdf` | Ejecutar `pip install xhtml2pdf` |
| Skill sin `SKILL.md` | Se omite el directorio con aviso en consola |
| Frontmatter YAML inválido | Se incluye la skill con metadatos vacíos y aviso |
| Directorio no existe | Error claro con la ruta incorrecta |

## Verificación del resultado

Después de ejecutar, confirma:
- El archivo PDF existe en la ruta de salida
- Tiene portada con fecha actual
- El índice lista todas las skills encontradas
- Cada sección muestra el nombre, descripción y contenido completo

## Script de referencia

Ver `scripts/export_skills_pdf.py` para la implementación completa.
