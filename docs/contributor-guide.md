# Contributor Guide — DevSkills Hub

Cómo agregar, actualizar y documentar skills en el catálogo DevSkills Hub.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Skill Structure](#skill-structure)
3. [SKILL.md Format](#skillmd-format)
4. [Adding Translations](#adding-translations)
5. [Preview Image](#preview-image)
6. [Testing Locally](#testing-locally)
7. [Submitting a PR](#submitting-a-pr)
8. [FAQ](#faq)

---

## Quick Start

**TL;DR:** Agregar una nueva skill toma 5 minutos:

```bash
# 1. Crea el directorio de tu skill
mkdir skills/my-awesome-skill

# 2. Crea SKILL.md con frontmatter y contenido
cat > skills/my-awesome-skill/SKILL.md << 'EOF'
---
name: Mi Skill Increíble
description: Una breve descripción de una línea
license: MIT
compatibility: "1.0"
---

# Contenido aquí

Escribe el contenido completo de tu skill en markdown.
EOF

# 3. Opcional: añade traducción al español
cat > skills/my-awesome-skill/SKILL_es.md << 'EOF'
# Contenido traducido al español

El cuerpo en español (el frontmatter se ignora).
EOF

# 4. Opcional: añade imagen de preview (360×160 PNG)
# cp my-image.png public/images/skills/my-awesome-skill.png

# 5. Test local
npm run dev

# 6. Abre http://localhost:4321
# y busca tu skill en el catálogo
```

Done. El ZIP y la entrada en el manifest se generan automáticamente.

---

## Skill Structure

Cada skill es un directorio en `skills/{skill-name}/` con esta estructura:

```
skills/
└── my-awesome-skill/
    ├── SKILL.md              # ✅ Requerido: Metadatos + Contenido (EN)
    ├── SKILL_es.md           # ❌ Opcional: Contenido (ES)
    ├── other-files.md        # ❌ Opcional: Documentación adicional
    ├── scripts/              # ❌ Opcional: Código ejecutable
    ├── assets/               # ❌ Opcional: Imágenes, datos, etc.
    └── ...más archivos/
```

**Notas:**

- El nombre del directorio debe ser **lowercase con guiones** (ej: `my-awesome-skill`)
- Solo `SKILL.md` es requerido
- Todo el directorio se empaqueta en `public/downloads/{skill-name}.zip`

---

## SKILL.md Format

### Estructura

```yaml
---
name: Nombre legible de la skill
description: Una línea que describe qué es y para qué sirve
license: MIT
compatibility: "1.0"
---

# Encabezado principal

Escribe tu contenido aquí en **markdown**. Puede incluir:
- Listas con viñetas
- Código con bloques ``` ```
- Tablas
- Enlaces
- Todo lo que markdown soporta

## Secciones

Organiza el contenido como quieras.

### Ejemplo de código

```python
print("Hello, world!")
```
```

### YAML Frontmatter (Requerido)

| Campo | Tipo | Ejemplo | Notas |
|-------|------|---------|-------|
| `name` | string | `"Inception Phase"` | Nombre legible (puede tener espacios) |
| `description` | string | `"Initialize project with scope and vision"` | Una sola línea; aparece en la card |
| `license` | string | `"MIT"` | Tipo de licencia (ej: MIT, Apache-2.0, proprietary) |
| `compatibility` | string\|null | `"1.0"` | Versión compatible; puede ser null |

**Validación:**

- `name` y `description` no pueden estar vacíos
- Máx 200 caracteres para `description`
- `license` debe ser válido (no caseSensitive)

### Markdown Body

- **Mínimo:** Una sección con contenido relevante
- **Máximo:** Tan largo como necesites
- **Formato:** Markdown estándar (CommonMark)
- **Rendering:** En modal dentro del catálogo con fuente monoespaciada

**No permitido:**

- HTML (se escapa como texto plano)
- JavaScript (se ignora)
- Iframes (se borran)

---

## Category Detection

El catálogo asigna automáticamente una categoría según el **prefijo del nombre del directorio**:

| Prefijo | Categoría | Icono |
|---------|-----------|-------|
| `openup-*` | OpenUP | 🔄 |
| `dotnet-*` | .NET Core | 🟣 |
| `python-*` | Python | 🐍 |
| `pdf-*` | Utilidades | 🛠️ |
| `skill-*` | Meta | ✨ |
| *(otro)* | Front-end | 📦 |

**Ejemplo:**
- `skills/openup-inception/` → categoría "OpenUP"
- `skills/python-patterns/` → categoría "Python"
- `skills/my-helper-tool/` → categoría "Front-end"

Elige el prefijo que mejor describe tu skill.

---

## Adding Translations

### Español (SKILL_es.md)

Para agregar una versión en español:

1. **Crea `SKILL_es.md`** en el mismo directorio

   ```bash
   cp skills/my-skill/SKILL.md skills/my-skill/SKILL_es.md
   ```

2. **Traduce solo el cuerpo** (ignora el frontmatter)

   ```markdown
   # Traducción al Español

   Aquí va el contenido traducido. El frontmatter se ignora.
   Solo el cuerpo se usa como contenido en español.
   ```

3. **Guarda en UTF-8**

   Asegúrate de que el archivo esté en UTF-8 (sin BOM).

**Resultado:**

- En el modal, aparecerá un botón con bandera 🇪🇸 / 🇬🇧
- Click alterna entre EN y ES
- Si no existe `SKILL_es.md`, no aparece el botón

---

## Preview Image

### Agregando una imagen

1. **Crea o descarga una imagen PNG**
   - Tamaño recomendado: **360×160 píxeles**
   - Formato: PNG (JPEG también funciona)
   - Máx 500 KB

2. **Coloca en `public/images/skills/`**

   ```bash
   cp my-image.png public/images/skills/my-awesome-skill.png
   ```

   El nombre del archivo debe coincidir con el nombre del directorio de la skill.

3. **Test local**

   ```bash
   npm run dev
   ```

   La imagen debe aparecer en la parte superior de la card en el grid.

### Notas de imagen

- La imagen se recorta/escala a 360×160 en la card
- Aparece con filtro oscuro y overlay degradado
- En hover, se amplía ligeramente
- Si no existe imagen, se oculta ese espacio

---

## Testing Locally

### Setup

```bash
# Clonar repo
git clone https://github.com/jesusprodriguezUnir/DevsSkills.git
cd DevsSkills

# Instalar dependencias (Node.js ≥22.12.0 requerido)
npm install
```

### Desarrollo

```bash
# Generar manifests + iniciar servidor dev
npm run dev

# Servidor corre en http://localhost:4321
# Base path es /DevsSkills (como en GitHub Pages)
```

**El servidor automáticamente:**

- Regenera el manifest cuando cambias `SKILL.md`
- Recargas el navegador (Astro integra hot reload)
- Detecta nuevas imágenes en `public/images/skills/`

### Verificar tu skill

1. Abre http://localhost:4321
2. Busca tu skill por nombre (/ para enfocar búsqueda)
3. Haz click en "Ver contenido" → verifica el markdown
4. Verifica filtro por categoría
5. Prueba descargar el ZIP → debe contener todos los archivos del directorio
6. Si tiene `SKILL_es.md`, prueba el toggle de idioma

### Troubleshooting Dev

| Problema | Causa | Solución |
|----------|-------|----------|
| Skill no aparece | SKILL.md invalido o nombre mal | Verifica `npm run build:skills` output |
| Imagen no se ve | Archivo no en `public/images/skills/` o nombre mal | Usa mismo nombre que skill directory |
| Traducción no se toglea | `SKILL_es.md` no existe o está vacío | Crea archivo y añade contenido |
| Error "Cannot find module" | Dependencias no instaladas | Corre `npm install` |

---

## Submitting a PR

### Workflow

1. **Fork & branch**

   ```bash
   git checkout -b feature/add-my-skill
   ```

2. **Agregar skill & archivos**

   ```bash
   mkdir skills/my-awesome-skill
   # ...agrega SKILL.md, SKILL_es.md (opcional), imagen (opcional)...
   git add skills/my-awesome-skill/
   ```

3. **Test local**

   ```bash
   npm run dev
   # Verifica que tu skill aparece en http://localhost:4321
   ```

4. **Commit**

   ```bash
   git add skills/
   git commit -m "feat: add my-awesome-skill

   - Adds Inception phase workflow documentation
   - Includes Spanish translation
   - Includes preview image"
   ```

5. **Push & PR**

   ```bash
   git push origin feature/add-my-skill
   # Abre PR en GitHub
   ```

### PR Checklist

- [ ] Skill directory sigue naming convention (lowercase con guiones)
- [ ] `SKILL.md` tiene metadatos válidos (name, description, license, compatibility)
- [ ] Descripción cabe en una línea (max 200 chars)
- [ ] Contenido es en markdown válido (sin HTML/JS)
- [ ] `SKILL_es.md` incluido si es traducción importante
- [ ] Imagen en `public/images/skills/{skill-name}.png` (360×160, <500KB)
- [ ] Testeado localmente (`npm run dev` y verificado en browser)
- [ ] ZIP se descarga sin errores

### CI/CD

GitHub Actions automáticamente:

1. Checkout del código
2. Instala dependencias
3. Regenera ZIPs + manifest
4. Ejecuta `astro check` (type checking)
5. Construye el sitio
6. Publica a GitHub Pages

Si todo pasa, tu PR se mergeará y el sitio se actualizará automáticamente.

---

## FAQ

### ¿Cuánto tarda en aparecer mi skill en producción?

Después de merge a `main`:
1. GitHub Actions se dispara (2-3 minutos)
2. Genera ZIPs + sitio + deploys
3. Aparece en producción en ~5 minutos

### ¿Puedo actualizar una skill existente?

Sí, simplemente edita el archivo `SKILL.md`:

```bash
# Edita skills/openup-inception/SKILL.md
# Commit y push
# GitHub Actions regenera automáticamente
```

### ¿Qué pasa si mi SKILL.md tiene errores de YAML?

El build falla con error. Verifica:
- Comillas correctas en strings con `:`
- Indentación (no espacios antes del `---`)
- Caracteres especiales escapados

Usa un validador YAML online si necesitas.

### ¿Puedo incluir subcarpetas/scripts en mi skill?

Sí, todo lo dentro de `skills/my-skill/` se empaqueta en el ZIP:

```
skills/my-skill/
├── SKILL.md
├── scripts/
│   ├── deploy.sh
│   └── test.py
├── assets/
│   └── diagram.png
└── docs/
    └── ARCHITECTURE.md
```

El usuario descargará todo esto en el ZIP.

### ¿Cómo cambio la categoría de mi skill?

Renombra el directorio con el prefijo correcto:

```bash
git mv skills/general-my-skill skills/openup-my-skill
```

El catálogo detextará automáticamente `openup-*` → OpenUP.

### ¿Puedo agregar múltiples imágenes?

Actualmente solo se soporta una imagen por skill (preview en la card). Para más imágenes, inclúyelas en el ZIP dentro de `assets/` para que el usuario las descargue.

### ¿Hay límite de tamaño de skill?

No hay límite explícito, pero:
- ZIP de skill muy grandes (>100 MB) pueden tomar tiempo en descargar
- Búsqueda es client-side, así que manifests enormes ralentizarían el browser
- Actualmente 47 skills sin problemas

### ¿Puedo usar variables/templates en SKILL.md?

No, `SKILL.md` es markdown plano. No se interpola. Si necesitas dinamismo, incluye instrucciones en el markdown que el usuario ejecute manualmente.

### ¿Cómo contribuyo una bugfix en el catálogo mismo (no una skill)?

Abre issue en GitHub describiendo el bug. Si es UI/UX:

```bash
git clone https://github.com/jesusprodriguezUnir/DevsSkills.git
# Edita src/pages/index.astro, src/components/SkillCard.astro, etc.
npm run dev
# Test en http://localhost:4321
git commit -m "fix: descripción del fix"
git push origin fix-branch
# Abre PR
```

---

## Resources

- **Project README:** [README.md](../README.md)
- **Architecture Notebook:** [docs/architecture-notebook.md](./architecture-notebook.md)
- **GitHub Repo:** https://github.com/jesusprodriguezUnir/DevsSkills/
- **Live Catalog:** https://devs-skills.vercel.app (Vercel) o https://jesusprodriguezUnir.github.io/DevsSkills/ (GitHub Pages)

### Skill Ecosystems & Inspiration

Check these external registries for more ideas and to share your skills:

- [Skills.sh](https://www.skills.sh/) — AI Agent Skills Registry
- [Awesome Claude](https://awesomeclaude.ai/) — Curated Claude Resources
- [AI Templates](https://aitmpl.com/) — Professional AI Prompt Templates
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — Official Claude patterns
- [Claude.ai Docs](https://claude.ai/docs) — Official Documentation

---

**Happy contributing! 🚀**

Preguntas? Abre un issue en GitHub o contacta al maintainer.
