# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MySkills** (package name: `starry-wind`) is a static web catalog for AI agent skills, built with Astro. It packages skill directories into downloadable ZIPs, generates a manifest, and renders a searchable/filterable dark-theme UI deployed to GitHub Pages at `https://jesusprodriguezUnir.github.io/DevsSkills/`.

## Commands

```bash
# Development
npm run dev          # Build skills + start Astro dev server at localhost:4321

# Build
npm run build        # Build skills ZIPs + manifest, then build production site to ./dist/
npm run build:skills # Only generate skill ZIPs and manifest (src/data/skills-manifest.json)

# Preview
npm run preview      # Preview the production build locally
```

Requires Node.js >=22.12.0.

## Architecture

### Data Flow

1. `scripts/build-skill-zips.mjs` scans `skills/*/` directories
2. Each skill must have a `SKILL.md` with YAML frontmatter (`name`, `description`, optional `license`, `compatibility`)
3. The script creates `public/downloads/{skill-name}.zip` and `src/data/skills-manifest.json`
4. Astro reads the manifest at build time — **there is no runtime database**
5. Static site deploys via `.github/workflows/deploy.yml` on push to `main`

### Category Detection (in build script)

Skills are auto-categorized by directory name prefix:
- `openup-*` → "OpenUP"
- `dotnet-*` → ".NET Core"
- `pdf-*` → "Utilidades"
- `skill-*` → "Meta"
- anything else → "General"

### Key Source Files

- `src/pages/index.astro` — Main page: reads manifest, renders hero stats, search, category filters, and skill grid. Client-side JS handles search (`/` = focus, `ESC` = clear) and filter via `data-*` attributes.
- `src/components/SkillCard.astro` — Card + modal (native `<dialog>`). Modal opens on "Ver contenido", download triggers on "Descargar .zip".
- `src/layouts/Layout.astro` — Global HTML shell, CSS custom properties (dark glassmorphism theme), animated background orbs.
- `scripts/build-skill-zips.mjs` — Build-time skill packager. Uses a simple regex YAML parser (not a full YAML library) for frontmatter.

### Adding a New Skill

Create `skills/{skill-name}/SKILL.md` with frontmatter:
```yaml
---
name: Human Readable Name
description: One-line description
license: MIT          # optional
compatibility: "1.0"  # optional
---
```
Then run `npm run build:skills`. The ZIP and manifest entry are generated automatically. Skill directory name must be lowercase-with-hyphens (1–64 chars, no leading/trailing/consecutive hyphens) and must match the manifest `id`.

### Generated Files (not committed)

- `public/downloads/*.zip` — Skill ZIPs
- `src/data/skills-manifest.json` — Skill metadata consumed by Astro
- `dist/` — Production build output
- `.astro/` — Astro generated types

## Agent Guidelines (from agent.md)

1. **Think Before Coding** — No assumptions; surface trade-offs; require a plan for architectural changes.
2. **Simplicity First** — Minimum code to achieve the goal. No premature abstractions. YAGNI.
3. **Surgical Changes** — Only modify what is strictly necessary. Do not refactor adjacent code.
4. **Goal-Driven Execution** — Define success criteria before implementation; verify every change.

Tech stack is intentionally minimal: Astro + vanilla CSS (CSS variables, Flex/Grid). No database by default; scale only when explicitly requested.
