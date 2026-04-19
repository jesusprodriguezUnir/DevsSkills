---
name: openup-export-skills-pdf
description: Genera un documento PDF con la documentación completa de todas las habilidades del repositorio. Escanea los directorios de skills, extrae metadatos y contenido SKILL.md, y los compila en un PDF estructurado con portada, índice y sección por skills. Usar cuando se necesite documentar, compartir o revisar el catálogo completo de habilidades del proyecto.
license: Apache-2.0
compatibility: Requires Python 3.8+. Install dependencies with: pip install markdown xhtml2pdf
metadata:
  author: openup-team
  version: "1.0"
---

# openup-exportar-habilidades-pdf

Genera un PDF con la documentación completa de todas las skills del repositorio.

## Cuándo usar esta habilidad

- El usuario pide "documentar las skills", "exportar skills a PDF" o "generar catálogo de skills"
- Se necesita un documento imprimible o compartible del catálogo de habilidades.
- Se quiere revisar visualmente el estado de todas las habilidades.

## Dependencias

Instale antes de ejecutar:

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
| `--skills-dir` | `.agentes/habilidades` | Directorio principal de habilidades |
| `--salida` | `docs/documentación-de-habilidades.pdf` | Ruta del PDF generado |
| `--título` | `Catálogo de Habilidades de Agente` | Título del documento |
| `--extra-dir` | *(ninguno)* | Directorio adicional de habilidades a incluir |

### Ejemplo con ambos directorios de skills

```bash
python .agents/skills/openup-export-skills-pdf/scripts/export_skills_pdf.py \
  --skills-dir .agents/skills \
  --extra-dir .github/skills \
  --output docs/skills-documentation.pdf
```

## Contenido del PDF generado

1. **Portada** — Título, fecha de generación y número total de habilidades
2. **Tabla de contenidos** — Listado con nombre y descripción breve de cada habilidad
3. **Secciones por habilidad** — Para cada habilidad:
   - Nombre y descripción
   - Metadatos del frontmatter (compatibilidad, licencia, versión, etc.)
   - Cuerpo completo del SKILL.md renderizado
4. **Pie de página** — Número de página y nombre del documento

## Gestión de errores

| Error | Acción |
|-------|--------|
| `ModuleNotFoundError: rebaja` | Ejecutar `pip install markdown xhtml2pdf` |
| `MóduloNotFoundError: xhtml2pdf` | Ejecutar `pip install xhtml2pdf` |
| Pecado de habilidad `SKILL.md` | Se omite el directorio con aviso en consola |
| Frontmatter YAML inválido | Se incluye la habilidad con metadatos vacíos y aviso |
| Directorio no existe | Error claro con la ruta incorrecta |

## Verificación del resultado

Después de ejecutar, confirme:
- El archivo PDF existe en la ruta de salida
- Tiene portada con fecha actual
- El índice lista de todas las habilidades encontradas.
- Cada sección muestra el nombre, descripción y contenido completo.

## Guión de referencia

Ver `scripts/export_skills_pdf.py` para la implementación completa.
