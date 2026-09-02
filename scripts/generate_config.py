#!/usr/bin/env python3
"""Generate js/site-config.js from environment variables (Vercel) or .env (local)."""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "js" / "site-config.js"
ENV_FILE = ROOT / ".env"


def load_dotenv() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip("'\"")
        os.environ.setdefault(key, value)


def esc_js(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def main() -> None:
    load_dotenv()

    formspree = os.environ.get("FORMSPREE_ENDPOINT", "").strip()
    provider = os.environ.get("ANALYTICS_PROVIDER", "").strip().lower()
    plausible = os.environ.get("PLAUSIBLE_DOMAIN", "mkofman.com").strip()
    ga4 = os.environ.get("GA4_ID", "").strip()
    calendly = os.environ.get("CALENDLY_URL", "").strip()

    if provider and provider not in ("plausible", "ga4"):
        raise SystemExit(f"Invalid ANALYTICS_PROVIDER: {provider!r} (use plausible or ga4)")

    content = f"""const SITE_CONFIG = {{
  url: 'https://mkofman.com',
  email: 'mkofman@mkofman.com',
  /**
   * Formspree endpoint — set FORMSPREE_ENDPOINT in Vercel or .env locally.
   * Example: https://formspree.io/f/xyzabcde
   * Leave empty to use mailto: fallback.
   */
  formspreeEndpoint: '{esc_js(formspree)}',
  /**
   * Calendly scheduling URL — set CALENDLY_URL in Vercel or .env.
   * Example: https://calendly.com/your-name/intro
   */
  calendlyUrl: '{esc_js(calendly)}',
  ogImage: '/images/portrait-hero-og.jpg',
  /**
   * Analytics — set ANALYTICS_PROVIDER=plausible|ga4 in Vercel or .env.
   */
  analytics: {{
    provider: '{esc_js(provider)}',
    plausibleDomain: '{esc_js(plausible)}',
    ga4Id: '{esc_js(ga4)}',
  }},
}};
"""

    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
