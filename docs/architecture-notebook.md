# Architecture Notebook — DevSkills Hub

**System Name:** DevSkills Hub (starry-wind)  
**Version:** 1.0  
**Date:** 2026-05-12  
**Architect:** Jesús P.

---

## 1. System Overview

### Purpose

DevSkills Hub es un catálogo web estático para skills de agentes de IA. Permite descubrir, previsualizar y descargar skills organizadas por categorías, con soporte para búsqueda/filtrado client-side y temas claro/oscuro.

### Scope

- **In Scope:**
  - Catálogo interactivo de 47+ skills
  - Búsqueda y filtrado dinámico por nombre/descripción/categoría
  - Modal para previsualización de contenido en markdown
  - Soporte multiidioma (EN/ES) por skill
  - Descarga de ZIPs pre-generados
  - Tema claro/oscuro persistido en localStorage
  - Generación automática de manifest y sitemaps
  - Deploy a GitHub Pages y Vercel

- **Out of Scope:**
  - Gestión de usuarios/autenticación
  - Base de datos dinámica
  - Hosting de contenido versionado (versioning es manual)
  - Sistema de comentarios o ratings
  - Análisis avanzado de uso

### Context & Stakeholders

| Stakeholder | Role | Concerns |
|--|--|--|
| Desarrolladores de skills | Contribuidores | Facilidad para empaquetar skills; descubrimiento rápido |
| Usuarios finales (AI engineers) | Consumidores | UX responsiva; búsqueda eficiente; descargas rápidas |
| Autor (Jesús P.) | Maintainer | Bajo costo operativo; deployment automático; extensibilidad |

---

## 2. Architectural Concerns

### Primary Concerns

1. **Performance & UX at Scale**
   - 47+ skills en grid grid responsivo requiere renderizado eficiente
   - Búsqueda debe ser instantánea (client-side)
   - Dark/light theme switch sin layout shift ni flash de tema incorrecto

2. **Maintainability & Extensibility**
   - Agregar nuevas skills debe ser trivial (solo crear `skills/{name}/SKILL.md`)
   - Cambios en estructura require actualizar build script, no código frontend
   - TypeScript strict para detectar errores en tiempo de build

3. **SEO & Discoverability**
   - Sitio SSG indexable por Google
   - Metadata OpenGraph para compartir en redes
   - Sitemap + robots.txt para crawlers

4. **Deployment Automation**
   - GitHub Actions auto-deploy en push a main
   - Soportar dos plataformas (GitHub Pages con subpath `/DevsSkills`, Vercel con `/`)
   - Generar manifests y ZIPs como parte del build

---

## 3. Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Pages / Vercel                   │
│                   (Static HTML/CSS/JS dist)                  │
└────────────────┬────────────────────────────────────────────┘
                 │
      ┌──────────┴──────────┐
      │                     │
  ┌─────────────┐      ┌────────────────┐
  │  index.astro│      │ SkillCard.astro│
  │  (Hero,     │      │ (Modal,        │
  │   Toolbar,  │      │  Download)     │
  │   Grid)     │      └────────────────┘
  └────────┬────┘
           │
      ┌────▼──────────────────────────────┐
      │  Layout.astro (Global Shell)       │
      │  - HTML boilerplate                │
      │  - Font loading                    │
      │  - Theme toggle script (is:inline) │
      │  - OG meta tags                    │
      └────┬──────────────────────────────┘
           │
    ┌──────▼──────────────────┐
    │  Generated Manifest      │
    │  src/data/             │
    │  skills-manifest.json  │
    └──────────────────────────┘
           │
      ┌────▼───────────────────────────┐
      │  Build-Time Script              │
      │  scripts/build-skill-zips.mjs   │
      │  - Scan skills/{name}/          │
      │  - Extract YAML frontmatter     │
      │  - Generate ZIPs                │
      │  - Create manifest JSON         │
      └────────────────────────────────┘
           │
    ┌──────▼──────────────┐
    │  skills/ Directory  │
    │  - openup-*         │
    │  - dotnet-*         │
    │  - python-*         │
    │  - pdf-*            │
    │  - etc.             │
    │  Each has SKILL.md + │
    │  optional SKILL_es.md│
    └─────────────────────┘
```

### Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Astro 6.1 | SSG-first; minimal JS; multi-framework support if needed |
| **UI/CSS** | Vanilla CSS + CSS variables | No build overhead; dark/light theme via `data-theme` |
| **Interactivity** | Vanilla JavaScript | No framework bloat; event listeners for search/filter/modal |
| **Icons** | Inline SVG | No HTTP requests; scoped styles |
| **Build** | Node.js script + Astro | Custom manifest generation; ZIPs via archiver |
| **Deployment** | GitHub Actions | Auto-deploy on push; free; integrated with GitHub Pages |

---

## 4. Key Architectural Decisions

### Decision 1: Static Site Generation (SSG)

**Context:** Skill catalog is relatively stable; no real-time updates needed.

**Decision:** Build as static site with pre-generated manifest; no server-side rendering.

**Rationale:**
- Zero server costs (GitHub Pages free)
- Fast CDN distribution
- SEO-friendly (Astro generates sitemap.xml)
- Predictable build output
- Skill additions trigger rebuild, not database changes

**Consequences:**
- Must run `npm run build:skills` before deploy
- Skill YAML parsing is custom (not full YAML library) to keep build slim
- Adding 1 skill requires push → GitHub Actions → rebuild

### Decision 2: Client-Side Search & Filter

**Context:** 47 skills fit in memory; real-time filtering expected.

**Decision:** Pass entire manifest to frontend; JavaScript filters on-page.

**Rationale:**
- Instant search results (no API latency)
- No backend needed
- Works offline (if cached)
- Reduces complexity

**Consequences:**
- Initial page load includes full manifest JSON
- Search logic duplicated in markup (data-* attributes) and JS
- No server-side sorting/pagination

### Decision 3: Theme Toggle in `is:inline` Script

**Context:** Flash of unstyled theme (FOUC) on page load is jarring.

**Decision:** Embed theme detection/apply in inline `<script is:inline>` before first paint.

**Rationale:**
- Reads localStorage before rendering
- Respects system preference if no localStorage
- No hydration overhead

**Consequences:**
- Inline script must be sync (blocks parsing briefly, but tiny)
- Theme toggle button requires client-side JS listener

### Decision 4: Manifest as Generated JSON (not CMS)

**Context:** No database; skills stored as directories.

**Decision:** `scripts/build-skill-zips.mjs` scans `skills/*/` and outputs `src/data/skills-manifest.json`.

**Rationale:**
- Single source of truth: `SKILL.md` frontmatter
- No schema drift (Zod in Astro would require schema file)
- Simple regex YAML parser (no external dependency)
- Reproducible builds

**Consequences:**
- Manifest must be regenerated on every `npm run dev/build`
- `src/data/skills-manifest.json` is in `.gitignore` (generated)
- `astro check` requires manifest to exist first

### Decision 5: Conditional Site & Base Path

**Context:** Deploy to both GitHub Pages (subpath `/DevsSkills`) and Vercel (root `/`).

**Decision:** Environment variable `VERCEL=1` switches site URL and base path; import.meta.env.BASE_URL prefixes all asset URLs.

**Rationale:**
- Single codebase handles both platforms
- All URLs computed at build time
- No runtime URL manipulation

**Consequences:**
- Must use `import.meta.env.BASE_URL` everywhere (enforce via code review)
- Local dev serves at `/DevsSkills` by default
- CI/CD must set `VERCEL=1` before building on Vercel

---

## 5. Architectural Constraints

### Technical Constraints

| Constraint | Impact | Mitigation |
|-----------|--------|-----------|
| No database | Skills are files in Git | Manifest generated at build time |
| Static output | No user-generated content | Rate limiting, analytics, etc. not possible |
| FOUC risk | Theme loads late | Use inline script before body |
| Client-side filtering | Limited to 47 skills | Acceptable; scale to ~500 before needing server |
| Custom YAML parsing | Not bulletproof | Enforce strict YAML format in `SKILL.md` |
| Git subpath `/DevsSkills` | URLs include base path | Import `BASE_URL` everywhere |

### Business Constraints

| Constraint | Reason |
|-----------|--------|
| Free deployment | No budget for hosting |
| No authentication | Public catalog; optional auth for contributor merges |
| Maintenance by 1 person | Simple architecture; minimal dependencies |
| Skills added manually | Curation over automation |

---

## 6. Quality Attributes

### Performance

**Requirement:** LCP < 2.5s, CLS < 0.1 on 4G networks.

**Architectural Support:**
- Astro auto-minifies HTML/CSS/JS
- CSS variables only (no Tailwind bloat)
- No framework hydration
- `loading="lazy"` on card images
- `display=swap` on Google Fonts
- Preconnect to fonts.googleapis.com

**Measurement:** Lighthouse CI on GitHub Actions (planned).

### Security

**Requirement:** No XSS, CSRF, or injection vectors.

**Architectural Support:**
- No user input in database (skills curated)
- Content-Security-Policy headers on Vercel
- Astro sanitizes component props
- No eval/innerHTML (only .textContent)
- TypeScript strict mode catches null/undefined

### Maintainability

**Requirement:** One person can add/update skills in <10 minutes.

**Architectural Support:**
- Skill = directory + `SKILL.md` only
- Manifest auto-generated
- No schema migrations
- Build script fully commented

### SEO

**Requirement:** Index all 47 skills on Google; share preview on social.

**Architectural Support:**
- Sitemap generated by `@astrojs/sitemap`
- robots.txt + canonical URLs
- OG meta tags on Layout
- `lang="es"` on HTML
- Semantic HTML (`<header>`, `<main>`, `<section>`)

### Accessibility (a11y)

**Requirement:** WCAG 2.1 Level AA compliance.

**Architectural Support:**
- `lang="es"` for screen readers
- `aria-label` on icon buttons
- `aria-live="polite"` on dynamic counts
- Color contrast > 4.5:1 (dark theme)
- Keyboard search (/ to focus, ESC to clear)
- Modal uses native `<dialog>` element

---

## 7. Subsystem Decomposition

### System Components

#### A. Frontend (Astro SPA-like)

**Purpose:** Render catalog UI with search, filter, modals.

**Components:**
- `src/layouts/Layout.astro` — Global HTML shell, theme script, meta tags
- `src/pages/index.astro` — Hero, toolbar, grid, search logic
- `src/components/SkillCard.astro` — Card + modal template

**Responsibilities:**
- Render skill grid from manifest
- Attach event listeners (search, filter, theme toggle)
- Manage modal lifecycle
- Language switching within modals

**Dependencies:**
- `src/data/skills-manifest.json` (generated)
- Google Fonts (external)

---

#### B. Build System (Node.js)

**Purpose:** Generate manifest and ZIPs from skill directories.

**Components:**
- `scripts/build-skill-zips.mjs` — Main build script
- `astro.config.mjs` — Astro config + integrations (sitemap, prefetch)
- `tsconfig.json` — TypeScript strict mode

**Responsibilities:**
- Scan `skills/{name}/SKILL.md` files
- Extract YAML frontmatter (name, description, license, etc.)
- Auto-detect category from directory prefix (`openup-*` → "OpenUP")
- Zip each skill directory → `public/downloads/{name}.zip`
- Generate manifest JSON → `src/data/skills-manifest.json`
- Generate sitemap → `dist/sitemap-index.xml` (via @astrojs/sitemap)

**Dependencies:**
- `archiver` (npm) for ZIP creation
- `fs`, `path` (Node.js builtins)
- Regex YAML parser (custom, in script)

---

#### C. Deployment Pipeline (GitHub Actions)

**Purpose:** Auto-build and deploy on push.

**Flow:**
1. Checkout code
2. Setup Node.js 22
3. `npm ci` install deps
4. `npm run build:skills` generate manifest + ZIPs
5. `npx astro check` type-check
6. `npx astro build` generate dist/
7. Upload to GitHub Pages

**Responsibilities:**
- Triggered on push to `main` branch
- Generate production-ready dist/
- Publish to GitHub Pages

---

### Interfaces Between Components

| From | To | Data | Protocol |
|------|----|----|----------|
| index.astro | SkillCard | Skill object | Astro prop |
| index.astro | Layout | title, description | Astro prop |
| Search script | DOM | Filter state | classList / style.display |
| Theme script | localStorage | theme preference | localStorage API |
| Build script | Manifest | Skills metadata | JSON file |
| Astro build | GitHub Pages | Static files | rsync/git push |

---

## 8. Data Model

### Skill Object (Runtime)

```typescript
interface Skill {
  id: string;                    // e.g., "openup-inception"
  name: string;                  // e.g., "Inception Phase"
  description: string;           // One-line summary
  category: string;              // "OpenUP", ".NET Core", "Python", etc.
  license: string;               // e.g., "MIT"
  compatibility: string | null;  // e.g., "1.0"
  fileCount: number;             // Files in ZIP
  rawSize: number;               // Uncompressed bytes
  zipSize: number;               // Compressed bytes
  subdirs: string[];             // Subdirectories in skill
  body: string;                  // Markdown content (English)
  bodyEs?: string | null;        // Markdown content (Spanish, optional)
  downloadUrl: string;           // /DevsSkills/downloads/{id}.zip
  image: string | null;          // /DevsSkills/images/skills/{id}.png
}
```

### SKILL.md Frontmatter (Source)

```yaml
---
name: Inception Phase
description: Initialize project with vision, scope, and feasibility
license: MIT
compatibility: "1.0"
---

# Content here (markdown body)
```

---

## 9. Technology Rationale Summary

| Choice | Reason | Alternative | Why Not |
|--------|--------|-------------|---------|
| Astro | SSG-first, minimal JS | Next.js, Gatsby | Overkill; server needed |
| Vanilla CSS | No build overhead | Tailwind | Simpler; CSS variables enough |
| TypeScript | Catch nulls/undefined | Flow | Better adoption; Astro support |
| Client-side search | Instant feedback | Server API | No backend available |
| GitHub Pages | Free, integrated | Netlify, AWS | GitHub-native workflow |
| GitHub Actions | Free CI/CD | Jenkins, CircleCI | Integrated with GitHub |

---

## 10. Known Limitations & Future Work

### Current Limitations

1. **No version control** — Skills are replaced in-place; no history.
2. **No dynamic sorting** — Only category filter + text search (both client-side).
3. **No analytics** — No view counts, download stats, etc.
4. **YAML parser is custom** — Doesn't handle all YAML edge cases.
5. **Modal content is `<pre><code>`** — No syntax highlighting for code blocks.

### Scalability Limits

- **Skills:** 47 → 500 is fine (client-side filter still instant). Beyond ~500, consider server-side search.
- **Images:** Currently PNG in public/; beyond ~30 MB total, optimize with WebP/AVIF conversion.
- **Downloads:** Served via CDN; no bandwidth limits observed to date.

### Planned Improvements

1. **Syntax highlighting** — Add Shiki or Prism for code blocks in modal.
2. **WebP/AVIF conversion** — Use `astro:assets` <Image> component.
3. **Full-text search** — If skills reach 500+, add Algolia or server-side search.
4. **Skill versioning** — Track multiple versions per skill (requires DB).
5. **Skill ratings/reviews** — Community feedback (requires DB + auth).

---

## 11. Architectural Decision Log

| Date | Decision | Status | Rationale Link |
|------|----------|--------|---|
| 2024-01 | SSG-only (no server) | ✅ Approved | See Decision 1 |
| 2024-02 | Client-side search | ✅ Approved | See Decision 2 |
| 2024-03 | Manifest JSON (not CMS) | ✅ Approved | See Decision 4 |
| 2026-05 | Upgrade to `astro/tsconfigs/strictest` | ✅ Approved | Type safety; detect undefined errors |
| 2026-05 | Add `@astrojs/sitemap` integration | ✅ Approved | SEO; auto-generate sitemap.xml |
| 2026-05 | Add `astro check` to CI | ✅ Approved | Catch type errors before build |

---

## 12. References & Related Documents

- **Vision Document:** (to be created)
- **Risk List:** (to be created)
- **Build Script:** `scripts/build-skill-zips.mjs`
- **Astro Config:** `astro.config.mjs`
- **CLAUDE.md:** Project instructions

---

**Notebook Version:** 1.0  
**Last Updated:** 2026-05-12  
**Next Review:** After major architectural change or new phase initiation
