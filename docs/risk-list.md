# Risk List — DevSkills Hub

**Project:** MySkills (starry-wind)  
**Version:** 1.0  
**Date:** 2026-05-12  
**Owner:** Jesús P.  
**Last Updated:** 2026-05-12  
**Review Frequency:** Quarterly or when new risks emerge

---

## Overview

This document identifies, assesses, and tracks risks that could impact the success of DevSkills Hub. Risks are categorized by probability and impact, with mitigation strategies assigned to owners.

---

## Risk Summary

| Risk ID | Description | P | I | Priority | Owner | Status |
|---------|-------------|---|---|----------|-------|--------|
| R-001 | Single maintainer dependency | M | H | 🔴 High | Jesús P. | Active |
| R-002 | Build script failure (no tests) | L | H | 🟡 Medium | Jesús P. | Active |
| R-003 | Custom YAML parser brittleness | L | M | 🟡 Medium | Jesús P. | Active |
| R-004 | Client-side search degrades >500 skills | M | M | 🟡 Medium | Jesús P. | Active |
| R-005 | Dual deployment complexity (GitHub Pages + Vercel) | M | M | 🟡 Medium | Jesús P. | Active |
| R-006 | Dependency breaking changes (Astro, TypeScript) | M | M | 🟡 Medium | Jesús P. | Active |
| R-007 | External platform downtime (GitHub/Vercel) | L | H | 🟡 Medium | N/A | Active |
| R-008 | Security: Malicious skill code | L | H | 🟡 Medium | Jesús P. | Active |
| R-009 | Performance degradation at scale (images/assets) | M | M | 🟡 Medium | Jesús P. | Active |
| R-010 | Accessibility/SEO regression | L | M | 🟢 Low | Jesús P. | Active |

**Legend:** P = Probability (H/M/L), I = Impact (H/M/L), 🔴 High, 🟡 Medium, 🟢 Low

---

## Detailed Risk Assessment

### R-001: Single Maintainer Dependency

**Description:**  
The project is maintained by a single person (Jesús P.). If the maintainer becomes unavailable (illness, time constraints, job change), skill updates, bug fixes, and deployments will stall.

**Probability:** Medium  
**Impact:** High  
**Risk Level:** 🔴 HIGH

**Current State:**
- Only one person with write access
- No documented runbook for onboarding new maintainers
- Build, deployment, and decision-making are centralized

**Consequences if Realized:**
- No skill updates or fixes for weeks/months
- Broken builds cannot be resolved
- Project perceived as abandoned

**Mitigation Strategy:**
1. Document all processes in `CLAUDE.md`, `docs/contributor-guide.md`, and inline code comments
2. Create a `RUNBOOK.md` with step-by-step setup and deployment instructions
3. Add a `MAINTAINERS.md` file listing maintainers and contact info
4. Automate CI/CD fully (GitHub Actions already in place)
5. Consider adding 1–2 co-maintainers (on a schedule)
6. Publish API/manifest format documentation for third-party integrations

**Owner:** Jesús P.  
**Target Completion:** 2026-06-30  
**Status:** In Progress (CLAUDE.md and contributor-guide.md exist; RUNBOOK.md pending)

---

### R-002: Build Script Failure (No Automated Tests)

**Description:**  
The `scripts/build-skill-zips.mjs` script has no unit or integration tests. If the script breaks (e.g., due to malformed SKILL.md, missing dependencies, Node version mismatch), the entire build pipeline fails, blocking deployments.

**Probability:** Low (script is stable)  
**Impact:** High (deploy blocked, manifest generation fails)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- Build script runs only in CI/CD or locally during `npm run dev/build`
- No test suite
- Manifest JSON is not committed; must be regenerated
- Script relies on custom YAML parsing (regex-based)

**Consequences if Realized:**
- GitHub Actions workflow fails silently or with unclear error
- No new skills can be deployed
- Developers cannot build locally without debugging the script
- Production site serves stale manifest

**Mitigation Strategy:**
1. Add test suite for `build-skill-zips.mjs` (test cases for YAML parsing, ZIP generation, manifest structure)
2. Test edge cases: malformed SKILL.md, missing files, special characters in skill name
3. Add pre-build validation: schema check for SKILL.md frontmatter
4. Add GitHub Actions step to verify manifest integrity (JSON schema validation)
5. Document expected script output in `RUNBOOK.md`
6. Add error handling and helpful error messages in script

**Owner:** Jesús P.  
**Target Completion:** 2026-07-15  
**Status:** Not Started

---

### R-003: Custom YAML Parser Brittleness

**Description:**  
The build script uses a regex-based YAML parser (not a full YAML library) to extract frontmatter. This parser may fail on:
- Multi-line field values
- Special characters (quotes, colons, hyphens)
- Non-ASCII characters
- YAML anchors or aliases

**Probability:** Low (simple YAML format enforced)  
**Impact:** Medium (skill won't build, but won't affect others)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- Parser is hardcoded in `build-skill-zips.mjs`
- Architecture Notebook notes: "Enforce strict YAML format in `SKILL.md`"
- No validation schema for SKILL.md

**Consequences if Realized:**
- New skills fail to build; contributor must debug regex
- Mixed quality: some skills parse, others don't
- Contributors may not understand YAML format constraints

**Mitigation Strategy:**
1. Document strict YAML format in `contributor-guide.md` with examples
2. Add pre-commit hook or build-time validation to check SKILL.md format (even before archiving)
3. Consider switching to a lightweight YAML library (e.g., `yaml` npm package) if regex becomes too fragile
4. Add test cases for YAML parsing (special chars, edge cases)
5. Provide a SKILL.md template in `skills/` directory for new contributors to copy

**Owner:** Jesús P.  
**Target Completion:** 2026-07-01  
**Status:** In Progress (contributor-guide.md exists; validation pending)

---

### R-004: Client-Side Search Degrades Beyond 500 Skills

**Description:**  
The current architecture passes the entire manifest JSON to the browser and filters client-side. This works well for 47 skills but will degrade as the catalog grows:
- Manifest JSON payload increases (already ~100 KB for 47 skills; could reach 1+ MB at 1000 skills)
- Search latency increases (JS filter loop over 1000 items is noticeable)
- Memory footprint grows
- Mobile users may experience lag

**Probability:** Medium (project may grow; depends on adoption)  
**Impact:** Medium (UX degradation, not data loss)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- 47 skills are easily handled client-side
- Manifest is embedded in index.astro
- Search/filter logic is vanilla JS (efficient but linear)
- Architecture Notebook notes scalability limit: "Beyond ~500, consider server-side search"

**Consequences if Realized:**
- Users on slow networks/mobile see delayed search results
- Page load time increases
- Perceived slowness leads to lower engagement

**Mitigation Strategy:**
1. Monitor manifest size and search performance (add Lighthouse CI to track)
2. At 250 skills, evaluate: optimize JS search (index-based, trie, or Algolia)
3. At 500+ skills, consider:
   - Server-side search API (simple Node.js backend)
   - Third-party search service (Algolia, Meilisearch)
   - Pagination (load skills in batches)
4. Implement pagination early (show first 20 skills, "Load More" button)
5. Lazy-load manifest JSON; show only categories on first load

**Owner:** Jesús P.  
**Target Completion:** When skills > 250 (TBD)  
**Status:** Not Started (monitoring needed)

---

### R-005: Dual Deployment Complexity (GitHub Pages + Vercel)

**Description:**  
The project is deployed to both GitHub Pages (subpath `/DevsSkills`) and Vercel (root `/`). Maintaining two deployment targets introduces complexity:
- Configuration must support both base paths
- Environment variables (`VERCEL=1`) must be set correctly
- Testing must cover both deployment scenarios
- Debugging is harder (which deployment is serving the issue?)

**Probability:** Medium (ongoing deployment/config changes)  
**Impact:** Medium (broken deploy on one platform, confused users)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- `astro.config.mjs` sets `base: '/DevsSkills'` by default
- `VERCEL=1` switches to Vercel mode (root `/`)
- `.github/workflows/deploy.yml` deploys to GitHub Pages only
- Vercel deployment requires manual setup (not in CI)

**Consequences if Realized:**
- Asset URLs broken on one platform (e.g., downloads return 404 on Vercel)
- Assets load from wrong base path (images, JS, CSS fail)
- Redirect loops or mixed content errors
- Contributors may not test both platforms

**Mitigation Strategy:**
1. Simplify: Choose **one** primary deployment target (recommend Vercel for simplicity)
2. If dual deployment is required:
   - Add both GitHub Actions and Vercel integration to CI/CD
   - Create deployment test matrix (test both base paths before deploy)
   - Document base path logic in `RUNBOOK.md`
   - Add environment variable documentation in `.env.example`
3. Add pre-deploy validation: verify `import.meta.env.BASE_URL` is used consistently
4. Add Lighthouse CI for both deployments to catch regressions

**Owner:** Jesús P.  
**Target Completion:** 2026-06-15  
**Status:** In Progress (GitHub Pages working; Vercel needs testing)

---

### R-006: Dependency Breaking Changes (Astro, TypeScript)

**Description:**  
The project depends on external packages with frequent updates:
- **Astro 6.1** — released frequently; major versions introduce breaking changes
- **TypeScript 5.9** — updated quarterly; strictness rules change
- **archiver 7.0** — ZIP library; rare breaking changes but possible
- Node.js >=22.12 — could drop support for older Node versions

**Probability:** Medium (industry standard for package updates)  
**Impact:** Medium (build breaks, requires fixes; not critical)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- No lock file (no `package-lock.json` committed)
- `package.json` uses caret ranges (^6.1.7, ^5.9.3) → allows minor/patch updates
- CI/CD installs latest compatible versions
- `astro check` catches type errors

**Consequences if Realized:**
- Build breaks unexpectedly on CI/CD
- Type errors appear after minor updates
- Contributors cannot reproduce builds locally (different versions)
- Features or APIs may be removed/renamed

**Mitigation Strategy:**
1. Commit `package-lock.json` to Git (ensure reproducible installs)
2. Pin major versions in `package.json` (`^6.1` → `6.1` for Astro, `5.9` for TypeScript)
3. Set up Dependabot to alert on updates (GitHub native, free)
4. Test updates in a branch before merging (automated via GitHub Actions)
5. Subscribe to Astro release notes and migration guides
6. Add `astro check` to pre-commit hook to catch type errors early
7. Document Node.js version in `.nvmrc` and `RUNBOOK.md`

**Owner:** Jesús P.  
**Target Completion:** 2026-06-01  
**Status:** In Progress (astro check in CI; lock file pending)

---

### R-007: External Platform Downtime (GitHub / Vercel)

**Description:**  
The project depends on external platforms:
- **GitHub** — hosts source code, runs CI/CD, serves GitHub Pages
- **Vercel** — optional alternative deployment
- **npm registry** — provides dependencies (archiver, Astro)

If any of these services experience outages, deployments stall and the site becomes unreachable.

**Probability:** Low (these are enterprise services with high uptime SLAs)  
**Impact:** High (site unreachable, deploy blocked)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- Single point of failure: GitHub Pages for primary deployment
- No fallback deployment (mirror to static host)
- No offline documentation or local backup

**Consequences if Realized:**
- Site inaccessible until platform recovers (likely <1 hour)
- Skill developers cannot deploy new content
- Users cannot download skills
- Team cannot develop/deploy code

**Mitigation Strategy:**
1. Monitor platform status pages (GitHub Status, Vercel Status)
2. Add Vercel as secondary deployment target (fallback if GitHub Pages is down)
3. Export manifest and skill ZIPs regularly for offline backup
4. Document platform dependencies and expected recovery time in `RUNBOOK.md`
5. Consider static host mirror (e.g., AWS S3) for disaster recovery (lower priority)
6. Set up status page (e.g., Uptime Robot) to alert on outages

**Owner:** Jesús P.  
**Target Completion:** 2026-08-01 (Vercel as fallback)  
**Status:** Not Started

---

### R-008: Security: Malicious Skill Code

**Description:**  
Skills are packaged and distributed as ZIPs to users. If a skill contains malicious code, it could:
- Execute arbitrary code when extracted
- Contain password stealers or other malware
- Violate user trust and harm the project's reputation

**Probability:** Low (curated catalog; manual review before merge)  
**Impact:** High (legal liability, reputation damage, user trust loss)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- Skills are curated manually (submitted via PRs)
- No automated security scanning
- No code review checklist for malicious content
- No virus scanning of ZIPs

**Consequences if Realized:**
- Users download and execute malicious code
- Project blamed for hosting malware
- Legal consequences (liability, DMCA takedowns)
- Loss of user trust and contributors

**Mitigation Strategy:**
1. Document security policy in `SECURITY.md` (reporting vulnerabilities)
2. Add code review checklist for skill PRs (scrutinize scripts, executables, API calls)
3. Run security scanning tools:
   - `npm audit` on all JavaScript skills
   - `bandit` or similar for Python skills
   - `dotnet-audit` for .NET skills
4. Scan ZIP files for known malware (optional; use ClamAV or VirusTotal API)
5. Require signed commits (GitHub > Branch Protection Rules)
6. Limit maintainer access (require 2+ reviewers for merges)
7. Add SECURITY.md with responsible disclosure policy
8. Monitor skill downloads for unusual patterns

**Owner:** Jesús P.  
**Target Completion:** 2026-06-30  
**Status:** Not Started (requires SECURITY.md and PR review template)

---

### R-009: Performance Degradation at Scale (Images / Assets)

**Description:**  
Each skill can have a preview image (`public/images/skills/{name}.png`). As the catalog grows:
- Total image payload increases (current: ~10 skill images, ~50 KB each = ~500 KB; at 200 skills with images, could be ~10 MB)
- Page load time increases (especially on slow networks or mobile)
- CDN caching may not be optimal
- Web Vitals (LCP, CLS) may degrade below thresholds

**Probability:** Medium (depends on adoption and image sizes)  
**Impact:** Medium (SEO penalty, user experience)  
**Risk Level:** 🟡 MEDIUM

**Current State:**
- ~47 skills, ~10 with preview images
- Images are PNG format (not optimized)
- `loading="lazy"` is set on card images (helps)
- `display=swap` on Google Fonts (helps)
- No image compression or WebP/AVIF conversion

**Consequences if Realized:**
- LCP > 2.5s on 4G (fails Lighthouse)
- CLS > 0.1 (images shift layout before loading)
- Users abandon site on slow networks
- SEO ranking drops (Google ranks on Core Web Vitals)

**Mitigation Strategy:**
1. Compress existing images (ImageOptim, TinyPNG, or similar)
2. Convert to WebP/AVIF format (use `astro:assets` <Image> component)
3. Set explicit image dimensions to prevent layout shift
4. Serve images via CDN (GitHub Pages + Vercel both cache)
5. Monitor Core Web Vitals via Lighthouse CI (add to GitHub Actions)
6. Use `srcset` for responsive images (mobile: smaller, desktop: larger)
7. Lazy-load images below the fold
8. Consider image proxy/optimization service (e.g., Cloudinary) for dynamic resizing

**Owner:** Jesús P.  
**Target Completion:** 2026-07-30  
**Status:** Not Started (Lighthouse CI setup pending)

---

### R-010: Accessibility / SEO Regression

**Description:**  
The site has several accessibility and SEO features (aria-labels, semantic HTML, sitemap, robots.txt). Updates or refactoring could inadvertently break these:
- Removing `aria-live` attributes
- Changing heading hierarchy (`<h2>` → `<h3>`)
- Disabling theme toggle (keyboard users)
- Removing canonical URLs or meta tags

**Probability:** Low (small codebase; easy to review)  
**Impact:** Medium (SEO drop, accessibility complaints)  
**Risk Level:** 🟢 LOW

**Current State:**
- Semantic HTML is used (Layout.astro, SkillCard.astro)
- `aria-label` on buttons, `aria-live` on dynamic content
- Keyboard shortcuts: `/` to search, `ESC` to clear
- `lang="es"` on HTML
- OG meta tags and canonical URLs
- Sitemap generated automatically

**Consequences if Realized:**
- Screen reader users unable to navigate
- Keyboard-only users stuck (no search shortcut)
- Google penalizes site for poor accessibility
- Skills not indexed properly

**Mitigation Strategy:**
1. Add accessibility testing to PR review checklist
2. Run automated a11y audit (e.g., axe, Lighthouse) in CI/CD
3. Test with screen readers (NVDA, JAWS) before major releases
4. Test keyboard navigation (Tab, Enter, Escape)
5. Test with browser DevTools accessibility tree
6. Maintain canonical URLs in `astro.config.mjs`
7. Test sitemap generation after each build
8. Document a11y guidelines in `contributor-guide.md`

**Owner:** Jesús P.  
**Target Completion:** 2026-07-01  
**Status:** In Progress (basic a11y in place; automated testing needed)

---

## Risk Management Process

### How Risks Are Tracked

1. **Identification:** Risks emerge during development, code review, or planning
2. **Assessment:** Probability and impact are evaluated using matrix below
3. **Mitigation:** Strategies are defined with owners and target dates
4. **Monitoring:** Status is reviewed quarterly or when new information arises
5. **Closure:** Risk is closed when mitigation is complete and validated

### Risk Matrix

| Probability \ Impact | Low | Medium | High |
|------------|---|---|---|
| **High** | 🟡 M | 🔴 H | 🔴 H |
| **Medium** | 🟢 L | 🟡 M | 🔴 H |
| **Low** | 🟢 L | 🟡 M | 🟡 M |

### Review Schedule

- **Quarterly Review:** 2026-08-12, 2026-11-12, 2027-02-12, 2027-05-12
- **After Major Changes:** New architectural decisions, technology upgrades
- **Ad Hoc:** When new risks are identified

### Escalation

- **Low Priority (🟢):** Track in this document; review quarterly
- **Medium Priority (🟡):** Review bi-weekly; assign owner; target completion date
- **High Priority (🔴):** Review weekly; escalate to decision-maker (Jesús P.); may block releases

---

## Risk Status Summary

| Status | Count | Notes |
|--------|-------|-------|
| 🟢 Not Started | 5 | Build tests, YAML validation, security scanning, performance monitoring, a11y automation |
| 🟡 In Progress | 4 | Documentation, CI/CD improvements, dual deployment, dependency management |
| ✅ Resolved | 1 | Basic a11y in place; astro check in CI |
| ⏸️ On Hold | 0 | — |

---

## References

- **Architecture Notebook:** `docs/architecture-notebook.md` (lists known limitations and scalability)
- **CLAUDE.md:** Project instructions and tech stack
- **Contributor Guide:** `docs/contributor-guide.md`

---

**Document Version:** 1.0  
**Owner:** Jesús P.  
**Last Updated:** 2026-05-12  
**Next Review:** 2026-08-12
