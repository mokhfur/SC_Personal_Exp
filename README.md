# Shafi Chowdhury — personal showcase

A dark, 3D-animated personal website for Shafi Chowdhury, Founder & Managing Director of
Shafi Consultancy Ltd.

No build step: the pages load Tailwind CSS, Three.js r128 and Lucide icons from public CDNs,
so they can be opened directly in a browser or dropped onto any static host (GitHub Pages,
Netlify, Hostinger).

## Pages
| File | Purpose |
| --- | --- |
| `index.html` | Home — hero with the animated Shafi Consultancy emblem, LinkedIn feed, About, Expertise, Speaking & Events, Insights, Contact |
| `expertise.html` | Six areas of expertise in full, with labels showing Shafi's relationship to each |
| `speaking.html` | All 39 papers, posters and presentations, grouped by theme with filters |
| `insights.html` | Proposed article topics with category filters |

## Assets
| File | Purpose |
| --- | --- |
| `assets/og-shafi-chowdhury.png` | 1200×630 Open Graph / Twitter card image |
| `assets/Shafi_Chowdhury_CV.pdf` | CV, linked from the At a glance panel |
| `assets/publications.py` | Source of truth for the publication list (`PUBS`), used to regenerate `speaking.html` |
| `sitemap.xml`, `robots.txt` | Search engine directives |

## Search engine optimisation

Each page carries a unique `<title>` and meta description, a canonical URL, Open Graph and
Twitter card metadata, and Schema.org JSON-LD:

- `index.html` — `ProfilePage` + `WebSite`, with `Person` and `Organization` nodes
- `expertise.html` — `WebPage` with a `BreadcrumbList` and an `ItemList` of the six areas
- `speaking.html` — `CollectionPage` with a `BreadcrumbList` and an `ItemList` of all 39
  publications, each as a `CreativeWork` (or `Poster`) with authors, year and event
- `insights.html` — `CollectionPage` with a `BreadcrumbList` and an `ItemList` of topics

`Article` markup is deliberately **not** used yet: no articles have been published. When the
first one goes live, add an `Article` or `BlogPosting` node with `headline`, `datePublished`,
`author` (referencing `#shafi`) and `image`.

### Changing the domain

Every absolute URL derives from one base. It currently points at the GitHub Pages address:

```
https://mokhfur.github.io/SC_Personal_Exp/
```

To move to a custom domain, replace that string throughout `index.html`, `expertise.html`,
`speaking.html`, `insights.html`, `sitemap.xml` and `robots.txt`:

```sh
grep -rl 'mokhfur.github.io/SC_Personal_Exp/' . \
  | xargs sed -i 's#https://mokhfur.github.io/SC_Personal_Exp/#https://your-domain.com/#g'
```

Then add a `CNAME` file containing the bare domain and update the `lastmod` dates in
`sitemap.xml`.

## LinkedIn feed

The home page embeds a [SociableKit](https://www.sociablekit.com/) LinkedIn profile post
widget (embed id `25729434`) between the hero and About sections. The widget script is
third-party, so sandboxed previews that restrict external scripts will show a fallback
message instead; it loads normally on the published site.

## Publishing with GitHub Pages

Settings → Pages → Deploy from a branch → `main` / root.

After publishing, submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.

## Content notes

Placeholder marks (dashed purple underlines, and "Still to be added" notes) flag information
Shafi has not yet supplied — currently the contact email and event photographs.
Nothing on the site invents employers, titles, qualifications, publications or client results.

All charts, tables, listings and model outputs use simulated data and do not represent any
real study, sponsor or patient.
