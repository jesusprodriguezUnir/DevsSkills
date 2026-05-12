---
name: astro-improvements
description: Audit an Astro application and propose prioritized improvements across performance & islands, architecture, SEO/accessibility/meta, and DX/TypeScript quality. Produces a report with severity, ranked findings, and before/after refactor recipes. Use when reviewing, refactoring, or onboarding into an Astro codebase.
license: Private
compatibility: Astro 4.x / 5.x · Node.js >=20 · works with SSG, SSR and hybrid output
---

# Astro Improvements

Skill to audit an Astro application, detect anti-patterns across four dimensions, and produce a prioritized report with concrete before/after refactor recipes.

## When to Use

- Before a production release to catch regressions
- When performance budget alerts fire (LCP, CLS, bundle size)
- During onboarding to an unfamiliar Astro codebase
- After migrating from SSG to SSR (or vice versa)
- Suspicion of over-hydration or unnecessary client JavaScript
- Routine accessibility or SEO audit

## Dimensions

| Dimension | Weight | Focus |
|-----------|--------|-------|
| ⚡ **Performance & Islands** | 30% | `client:*` directives, hydration cost, `<Image>`, prefetch, bundle size |
| 🏗️ **Architecture & Structure** | 25% | Layouts, content collections, routing, SSR vs SSG, `astro.config.mjs` |
| 🔍 **SEO, Accessibility & Meta** | 25% | Semantic HTML, ARIA, sitemap, robots, Open Graph, `lang`, headings |
| 🛠️ **DX, TypeScript & Quality** | 20% | `tsconfig`, env types, `Props` interfaces, linting, `astro check` in CI |

## Process

### Step 1: Inventory

Read in this order:
- `astro.config.mjs` — output mode (SSG/SSR/hybrid), integrations, adapters
- `package.json` — Astro version, framework integrations, bundle tools
- `src/` tree — layouts, pages, components, content, middleware
- `public/` — static assets that bypass Astro's asset pipeline

Flag:
```
✅ output mode is explicit and intentional
✅ only needed integrations are listed
⚠️ mixed .astro and framework components (React/Vue) without clear boundary
❌ no astro.config.mjs found → cannot proceed reliably
```

### Step 2: Map findings to dimensions

For each file or pattern found, assign it to one of the four dimensions and note the relevant path (`src/components/Card.astro:12`).

### Step 3: Score severity

| Severity | Criteria |
|----------|----------|
| 🔴 **Critical** | Blocks SEO indexing, breaks a11y for assistive tech, or sends 100+ KB unnecessary JS to every visitor |
| 🟡 **Major** | Degrades Core Web Vitals, creates confusing architecture, or causes DX friction in every feature |
| 🟢 **Minor** | Polish issue — measurable improvement but no immediate impact |

### Step 4: Propose refactors

For every 🔴 Critical and 🟡 Major finding, provide a before/after snippet. For 🟢 Minor findings a one-line fix is enough.

### Step 5: Emit report

Use the [Report Template](#report-template) at the end of this skill.

---

## Catalog of Improvements

### ⚡ Performance & Islands

#### `client:load` used for static content — 🔴 Critical

Every `client:load` sends a full framework bundle to the browser before the page is interactive. Reserve it for components that actually need browser APIs on load.

```astro
<!-- ❌ Before — sends React bundle even though Card is pure HTML -->
<Card client:load title="Hello" />

<!-- ✅ After — no directive: rendered to static HTML at build time -->
<Card title="Hello" />

<!-- ✅ After — interactive only when scrolled into view -->
<Counter client:visible initialCount={0} />
```

**Fix:** Audit every `client:*` directive. Use `client:visible` for below-the-fold interactivity, `client:idle` for low-priority widgets, and no directive for fully static components.

---

#### Raw `<img>` instead of `<Image>` — 🟡 Major

Astro's built-in `<Image>` component generates responsive `srcset`, converts to WebP/AVIF, and adds width/height to prevent layout shift. Raw `<img>` tags skip all of this.

```astro
<!-- ❌ Before -->
<img src="/hero.jpg" alt="Hero" />

<!-- ✅ After -->
---
import { Image } from 'astro:assets';
import heroImg from '../assets/hero.jpg';
---
<Image src={heroImg} alt="Hero" width={1200} height={600} />
```

**Fix:** Replace `<img src="...">` with `<Image>` for all local and remote images. Set `image.remotePatterns` in `astro.config.mjs` for external sources.

---

#### No prefetch strategy — 🟢 Minor

Astro supports automatic link prefetching with a single config line. Without it, navigations feel slower than necessary on multi-page sites.

```js
// ❌ Before — astro.config.mjs, no prefetch config
export default defineConfig({ ... });

// ✅ After — prefetch on hover, opt-out per link with data-astro-prefetch="false"
export default defineConfig({
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' }
});
```

**Fix:** Add `prefetch` config to `astro.config.mjs`. Use `prefetchAll: true` only for small sites with few pages.

---

### 🏗️ Architecture & Structure

#### Front matter logic instead of Content Collections — 🔴 Critical

Embedding data arrays or fetch logic directly in `.astro` page front matter bypasses type safety and makes content unqueryable.

```astro
<!-- ❌ Before — data hardcoded in page front matter -->
---
const posts = [
  { title: 'Post 1', date: '2024-01-01', slug: 'post-1' },
  { title: 'Post 2', date: '2024-02-01', slug: 'post-2' },
];
---

<!-- ✅ After — define a collection with schema -->
```

```ts
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

export const collections = {
  blog: defineCollection({
    schema: z.object({ title: z.string(), date: z.coerce.date() }),
  }),
};
```

```astro
<!-- src/pages/blog/index.astro -->
---
import { getCollection } from 'astro:content';
const posts = await getCollection('blog');
---
```

**Fix:** Move repeated data into `src/content/{collection}/` with a Zod schema in `src/content/config.ts`. Use `getCollection()` to query with full TypeScript inference.

---

#### Duplicate layout wrappers — 🟡 Major

Copy-pasted `<html>`, `<head>`, and `<body>` boilerplate across pages makes global changes (CSP headers, fonts, analytics) error-prone.

```astro
<!-- ❌ Before — same <head> repeated in every page -->
---
// src/pages/index.astro AND src/pages/about.astro
---
<html lang="en">
  <head><title>...</title><link rel="stylesheet" .../></head>
  <body>...</body>
</html>

<!-- ✅ After — one Layout component -->
---
import Layout from '../layouts/Layout.astro';
---
<Layout title="Home">
  <main>...</main>
</Layout>
```

**Fix:** Extract a `src/layouts/Layout.astro` that owns `<html>`, `<head>`, and global styles. Pass `title` and `description` as props.

---

#### Unused integrations in `astro.config.mjs` — 🟢 Minor

Every registered integration runs at build time. Leftover integrations from experiments increase build time and can introduce unexpected transformations.

```js
// ❌ Before — @astrojs/react listed but no .jsx/.tsx files exist
import react from '@astrojs/react';
export default defineConfig({ integrations: [react()] });

// ✅ After — only integrations actually in use
export default defineConfig({ integrations: [sitemap()] });
```

**Fix:** Cross-check `integrations` with `src/` — if no component files use a framework, remove its integration and package.

---

### 🔍 SEO, Accessibility & Meta

#### Missing `lang` attribute on `<html>` — 🔴 Critical

Screen readers and search engines need `lang` to parse content correctly. Its absence is a WCAG 2.1 Level A failure.

```astro
<!-- ❌ Before -->
<html>

<!-- ✅ After -->
<html lang="en">
```

**Fix:** Add `lang` to the root `<html>` in every layout. Accept it as a prop (`lang = 'en'`) for multilingual sites.

---

#### Missing Open Graph and meta description — 🟡 Major

Pages without `og:title`, `og:description`, and `description` meta appear as bare URLs when shared on social platforms and rank lower in search results.

```astro
<!-- ❌ Before — Layout.astro head has only a <title> -->
<head>
  <title>{title}</title>
</head>

<!-- ✅ After -->
<head>
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:type" content="website" />
  <meta property="og:image" content={new URL(ogImage, Astro.url)} />
</head>
```

**Fix:** Add a `<SEO>` component or extend the Layout props to accept `description` and `ogImage`. Make `description` required via TypeScript.

---

#### Skipped heading levels — 🟡 Major

Jumping from `<h1>` to `<h3>` breaks the document outline used by screen readers and degrades SEO heading structure.

```astro
<!-- ❌ Before -->
<h1>Blog</h1>
<h3>Latest Posts</h3>  <!-- h2 is missing -->

<!-- ✅ After -->
<h1>Blog</h1>
<h2>Latest Posts</h2>
<h3>{post.title}</h3>
```

**Fix:** Enforce one `<h1>` per page and sequential levels. Use browser DevTools › Accessibility pane or axe to audit the heading tree.

---

### 🛠️ DX, TypeScript & Quality

#### `strict: false` in `tsconfig.json` — 🔴 Critical

Disabling strict mode masks `null`/`undefined` errors, implicit `any` types, and unchecked function parameters — all common sources of runtime bugs in Astro components.

```jsonc
// ❌ Before
{ "extends": "astro/tsconfigs/base", "compilerOptions": { "strict": false } }

// ✅ After — use the strictest preset Astro ships
{ "extends": "astro/tsconfigs/strictest" }
```

**Fix:** Replace with `astro/tsconfigs/strictest` (or at minimum `astro/tsconfigs/strict`). Fix resulting type errors before enabling — do not suppress with `// @ts-ignore`.

---

#### `import.meta.env` without type declarations — 🟡 Major

Accessing custom env variables without an `env.d.ts` declaration means TypeScript treats them as `any`, silencing typos in variable names.

```ts
// ❌ Before — no env.d.ts, IDE has no autocomplete
const key = import.meta.env.PUBLIC_API_KEY; // type: any

// ✅ After — src/env.d.ts
/// <reference types="astro/client" />
interface ImportMetaEnv {
  readonly PUBLIC_API_KEY: string;
  readonly SECRET_DB_URL: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

**Fix:** Create `src/env.d.ts` with typed declarations for every env variable. Add a check to CI that fails if `.env.example` variables are missing from `env.d.ts`.

---

#### Components without `Props` interface — 🟢 Minor

Untyped component props prevent IDE autocompletion and let callers pass wrong values silently.

```astro
<!-- ❌ Before — no prop types -->
---
const { title, count } = Astro.props;
---

<!-- ✅ After -->
---
interface Props {
  title: string;
  count?: number;
}
const { title, count = 0 } = Astro.props;
---
```

**Fix:** Add an `interface Props` block to every `.astro` component that accepts props. Use `astro check` (see below) to surface violations.

---

## Report Template

````markdown
# Astro Improvements — {project name}

## 📊 Overall Score: {X}/100

| Dimension | Score | Status |
|-----------|-------|--------|
| ⚡ Performance & Islands | {X}/30 | {✅ ⚠️ ❌} |
| 🏗️ Architecture & Structure | {X}/25 | {✅ ⚠️ ❌} |
| 🔍 SEO, Accessibility & Meta | {X}/25 | {✅ ⚠️ ❌} |
| 🛠️ DX, TypeScript & Quality | {X}/20 | {✅ ⚠️ ❌} |

## Verdict

{🟢 SHIP | 🟡 SHIP WITH MINOR FIXES | 🔴 NEEDS WORK BEFORE SHIPPING}

## Findings

| # | Severity | Dimension | Location | Effort |
|---|----------|-----------|----------|--------|
| 1 | 🔴 Critical | Performance | `src/components/Hero.astro:8` | S |
| 2 | 🟡 Major | Architecture | `src/pages/blog/index.astro:3–18` | M |

## Detailed Findings

### Finding 1 — {title}
**File:** `src/...`  
**Why it matters:** ...  
**Before:**
```astro
...
```
**After:**
```astro
...
```

## Top 5 Action Plan

1. [ ] {Most impactful fix — link to finding}
2. [ ] ...
3. [ ] ...
4. [ ] ...
5. [ ] ...

## Checklist

- [ ] No `client:load` on purely static components
- [ ] All `<img>` tags replaced with `<Image>`
- [ ] `astro.config.mjs` integrations match actual usage
- [ ] Every layout has `lang` on `<html>`
- [ ] `og:title`, `og:description`, `description` present on all pages
- [ ] No skipped heading levels
- [ ] `tsconfig.json` extends `astro/tsconfigs/strictest`
- [ ] `src/env.d.ts` types all `import.meta.env` variables
- [ ] All components have a `Props` interface
- [ ] `astro check` runs in CI with zero errors
````

## Heuristics & Quick Wins

- If `client:load` is on a component with no event handlers or browser API calls → remove the directive entirely.
- If `astro.config.mjs` output is `'server'` but every page has no dynamic data → switch to `'static'` and remove the adapter.
- If `@astrojs/sitemap` is absent and the site is SSG → add it; search engines won't automatically discover all pages.
- If a page has two or more `<h1>` tags → refactor so only the page title uses `<h1>`.
- If `astro check` is not in the CI pipeline → add it before the build step; it catches type errors that TypeScript alone misses in `.astro` files.
