const SITE_CONFIG = {
  url: 'https://mkofman.com',
  email: 'mkofman@mkofman.com',
  /**
   * Formspree endpoint — set FORMSPREE_ENDPOINT in Vercel or .env locally.
   * Example: https://formspree.io/f/xyzabcde
   * Leave empty to use mailto: fallback.
   */
  formspreeEndpoint: '',
  /**
   * Calendly scheduling URL — set CALENDLY_URL in Vercel or .env.
   * Example: https://calendly.com/your-name/intro
   */
  calendlyUrl: '',
  ogImage: '/images/portrait-hero-og.jpg',
  /**
   * Analytics — set ANALYTICS_PROVIDER=plausible|ga4 in Vercel or .env.
   */
  analytics: {
    provider: '',
    plausibleDomain: 'mkofman.com',
    ga4Id: '',
  },
};
