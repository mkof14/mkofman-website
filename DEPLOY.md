# Deploy checklist — mkofman.com (Vercel)

## 1. Vercel

1. Import the project at [vercel.com/new](https://vercel.com/new) (GitHub or upload)
2. **Framework Preset:** Other (static site)
3. **Root Directory:** `.` (project root)
4. **Build / Install:** configured in `vercel.json` (build script, config, Media Kit PDF)
5. **Output Directory:** `.` (static HTML at root)
6. Deploy

`vercel.json` configures cache headers, www → apex redirect, and the build pipeline.

## 2. Custom domain

1. Vercel → Project → Settings → Domains
2. Add `mkofman.com` and `www.mkofman.com`
3. At your registrar, set DNS as Vercel instructs (usually `A` / `CNAME` to Vercel)

## 3. Environment variables (Vercel → Settings → Environment Variables)

| Variable | Example | Purpose |
|----------|---------|---------|
| `FORMSPREE_ENDPOINT` | `https://formspree.io/f/xyzabcde` | Contact form delivery |
| `ANALYTICS_PROVIDER` | `plausible` or `ga4` | Enable analytics |
| `PLAUSIBLE_DOMAIN` | `mkofman.com` | Plausible site id |
| `GA4_ID` | `G-XXXXXXXXXX` | Google Analytics 4 |

Copy `.env.example` to `.env` for the same values locally. `scripts/generate_config.py` writes `js/site-config.js` at build time.

### Formspree setup

1. Create a form at [formspree.io](https://formspree.io)
2. Set `FORMSPREE_ENDPOINT` to the form URL (e.g. `https://formspree.io/f/xyzabcde`)
3. Redeploy — forms use Formspree; if unset, mailto fallback remains

## 4. After content changes

```bash
python3 scripts/build_site.py
python3 scripts/generate_config.py
.venv/bin/python scripts/generate_media_kit_pdf.py   # first time: python3 -m venv .venv && .venv/bin/pip install fpdf2 pillow
```

Then commit and push — Vercel redeploys automatically.

## 5. Google Search Console

Submit `https://mkofman.com/sitemap.xml`

## 6. Media Kit PDF

Generated at `downloads/michael-kofman-media-kit.pdf` during build. Linked from the Media Kit page.
