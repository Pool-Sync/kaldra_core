# FRONTEND_STRUCTURE_CHECKLIST.md

## 1. Purpose

This document provides a **structured checklist** to validate that the `4iam_frontend/` project is correctly configured and ready for:

- Local development
- Design System evolution
- Integration with the KALDRA API
- Deployment to Vercel

---

## 2. High-Level Structure

The frontend is a **Next.js 14 (App Router)** application with the following expected structure:

```text
4iam_frontend/
├── app/
│   ├── (alpha)/
│   ├── (geo)/
│   ├── (product)/
│   ├── (safeguard)/
│   ├── (kaldra)/
│   └── (docs)/
├── components/
├── design_system/
│   ├── tokens/
│   └── branding/
├── lib/
│   ├── api/
│   ├── news/
│   ├── seo/
│   └── operations/
├── public/
├── styles/
└── docs/   # Frontend-related documentation
```

> The exact folder names may differ slightly, but the **conceptual structure** should match this layout.

---

## 3. Repository-Level Checklist

* [ ] `4iam_frontend/` exists at the repo root.
* [ ] `package.json` is present and includes:

  * [ ] `next`, `react`, `react-dom`, `typescript`, `tailwindcss`
* [ ] `tsconfig.json` exists and is valid.
* [ ] `next.config.js` exists and uses the **App Router**.
* [ ] `tailwind.config.js` and `postcss.config.js` exist.
* [ ] `styles/globals.css` is configured and imported in the root layout.

---

## 4. App Router Checklist (`app/`)

* [ ] `app/layout.tsx` defines the global layout and imports Tailwind globals.
* [ ] `app/page.tsx` exists as the main landing page.
* [ ] Sections exist for each KALDRA pillar:

  * [ ] `/alpha`
  * [ ] `/geo`
  * [ ] `/product`
  * [ ] `/safeguard`
  * [ ] `/kaldra`
  * [ ] `/docs` or similar documentation area.
* [ ] Each page uses shared layout components (header, navigation, footer).

---

## 5. Design System Checklist (`design_system/`)

* [ ] `design_system/README_DESIGN_SYSTEM.md` exists.
* [ ] Token files exist in `design_system/tokens/`:

  * [ ] `colors.json`
  * [ ] `typography.json`
  * [ ] `spacing.json`
  * [ ] `radii.json`
  * [ ] `elevations.json`
  * [ ] `effects.json`
* [ ] Branding docs exist in `design_system/branding/`:

  * [ ] `LOGO_GUIDE.md`
  * [ ] `COLOR_GUIDE.md`
  * [ ] `TYPOGRAPHY_GUIDE.md`
  * [ ] `LAYOUT_GUIDE.md`
  * [ ] `COMPONENT_GUIDE.md`
* [ ] Core UI components created as stubs (cards, buttons, navigation, layout components).

---

## 6. API & Data Layer Checklist (`lib/`)

* [ ] `app/lib/api/types.ts` defines shared types:

  * [ ] `Signal`, `Insight`, `ExplorerFeedItem`, `ServiceKey`, `TWRegime`, `SignalPriority`, `InsightType`, etc.
* [ ] `app/lib/api/config.ts` defines:

  * [ ] `API_ENDPOINTS`
  * [ ] `API_CONFIG` with `useMocks` or similar flag.
* [ ] `app/lib/api/mock_data.ts` exists and provides mock signals for:

  * [ ] Alpha
  * [ ] GEO
  * [ ] Product
  * [ ] Safeguard
* [ ] Hooks (optional but recommended):

  * [ ] `app/hooks/useExplorer.ts`
  * [ ] Other domain-specific hooks as needed.

---

## 7. Environment & Deployment Checklist

* [ ] `docs/ENV_REFERENCE_FRONTEND.md` exists and is up to date.
* [ ] `docs/DEPLOY_FRONTEND_VERCEL.md` describes the Vercel deployment process.
* [ ] `docs/PRODUCTION_NOTES.md` describes how production behavior differs from development.
* [ ] `.env.example` exists with at least:

  * [ ] `NEXT_PUBLIC_KALDRA_API_MODE`
  * [ ] `NEXT_PUBLIC_KALDRA_API_URL`

---

## Future Implementations

* Add separate checklists for:

  * Accessibility (a11y).
  * Performance (Lighthouse budgets, Core Web Vitals).
* Include a "Design Review" section tied to Figma or design artifacts.

---

## Enhancements (Short/Medium Term)

* Add a CI job to automatically verify structure (e.g. required files and folders).
* Create a CLI script (`scripts/check_frontend_structure.py` or similar) to run locally.
* Extend this checklist with links to visual specs for each major page.

---

## Research Track (Long Term)

* Investigate automated visual regression testing to ensure changes don’t break layout.
* Explore design token synchronization between code and design tools.
* Consider multi-brand / multi-theme support using the same Design System.

---

## Known Limitations

* This checklist does not validate **implementation details**, only structure and presence.
* Some folders or filenames may evolve, requiring manual updates to this document.
* Does not yet encode dependencies between UI components and backend capabilities.

---

## Testing

* Manual:

  * Periodically walk this checklist after major refactors.
* Automated (future):

  * Add a CI step that checks for required file paths and fails if any are missing.

---

## Next Steps

* Ensure this document is created at `docs/FRONTEND_STRUCTURE_CHECKLIST.md`.
* Cross-link it from:

  * `docs/DEPLOY_FRONTEND_VERCEL.md`
  * `docs/PRODUCTION_NOTES.md`
* Use this checklist before each **major release** or **design system upgrade**.
