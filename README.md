# badsignal.app

Landing page + privacy policy for **Bad Signal**, an IPTV player for
Android TV / Google TV. App source: [Saittam82/bad-signal](https://github.com/Saittam82/bad-signal) (private).

Plain static HTML, no build step. `index.html` is the landing page,
`privacy/index.html` serves `badsignal.app/privacy`. Push to `main` → GitHub
Pages deploys automatically.

## Infrastructure (set up Sep 1, 2026)

- **Domain:** `badsignal.app` — Cloudflare Registrar, auto-renew (~$14.20/yr
  at cost). `.app` is HSTS-preloaded: browsers require HTTPS, HTTP never works.
- **Hosting:** GitHub Pages from this repo (`main`, root). Custom domain via
  the `CNAME` file. **Enforce HTTPS is ON** (GitHub-managed Let's Encrypt cert,
  auto-renews).
- **DNS (Cloudflare, all records "DNS only" / grey cloud):**

  | Type | Name | Content |
  |---|---|---|
  | A | `@` | 185.199.108.153 |
  | A | `@` | 185.199.109.153 |
  | A | `@` | 185.199.110.153 |
  | A | `@` | 185.199.111.153 |
  | CNAME | `www` | `saittam82.github.io` |

  Grey cloud matters: proxying (orange) would block GitHub's cert issuance
  and renewal. Plus MX/TXT records managed by Cloudflare Email Routing (locked).
- **Email:** Cloudflare Email Routing, catch-all rule — any address
  `@badsignal.app` (the public one is `hello@`) forwards to the owner's
  personal Gmail. Config lives in the Cloudflare dashboard under
  Email Routing for the zone.

## Gotchas

- Cert issuance only starts once DNS resolves. If HTTPS ever breaks with a
  `*.github.io` cert mismatch, re-trigger issuance by removing and re-adding
  the custom domain in the repo's Pages settings.
- The contact email `hello@badsignal.app` is referenced in `index.html`,
  `privacy/index.html`, and the Play Store listing — keep them in sync.
- Keep the content-responsibility disclaimer (footer + privacy policy): the
  app ships no content, users bring their own playlists. It matters for Play
  review.
