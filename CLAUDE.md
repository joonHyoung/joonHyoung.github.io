# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal blog (Korean locale, "Redsnow's Anything Blog") built on the **Minimal Mistakes** Jekyll theme and deployed to **GitHub Pages** at https://joonhyoung.github.io. The repository is a full copy of the theme gem, so the theme's own gemspec, `docs/`, and `test/` directories live at the root alongside the actual site content. `docs/` and `test/` are excluded from the build (`exclude:` in `_config.yml`) — they are theme source/examples, not this site.

## Commands

```bash
# Install Ruby dependencies
bundle install

# Local dev server with live reload (http://localhost:4000)
bundle exec jekyll serve

# One-off production build into _site/
bundle exec jekyll build

# Rebuild the minified JS bundle after editing anything under assets/js/
# (concatenates + uglifies plugins into assets/js/main.min.js, then adds the license banner)
npm run build:js

# Watch JS and rebuild on change
npm run watch:js
```

There is no lint step and no site-level test suite — the `test/` directory belongs to the upstream theme, not this blog.

## Authoring content

- **Posts** go in `_posts/` named `YYYY-MM-DD-title.md`. Front matter uses `title`, `categories`, `tag`, `toc`, `last_modified_at`, `comments`, `mathjax`. Post-wide defaults (`layout: single`, author profile, read time, comments, share, related) are applied via `defaults:` in `_config.yml` — do not repeat them per post.
- **Standalone pages** go in `_pages/` with an explicit `permalink`. The category/tag/year archives (`category-archive.md`, `tag-archive.md`, `year-archive.md`) are Liquid-generated (`type: liquid`) and their permalinks (`/categories/`, `/tags/`, `/year-archive/`) must match the archive paths configured in `_config.yml`.
- Permalinks for posts are `/:categories/:title/`; pagination shows 5 posts per page.
- Top navigation is driven by `_data/navigation.yml`; UI string translations by `_data/ui-text.yml`.

## Key configuration facts

- Theme is set two ways in `_config.yml`: `theme: minimal-mistakes-jekyll` (the local gem, used by `bundle exec jekyll serve`) and `remote_theme: mmistakes/minimal-mistakes` (for GitHub Pages remote-theme builds). Keep them in sync; do not reintroduce any other `theme:` key.
- The home page is `index.html` (`layout: home`, `author_profile: true`). Previously duplicated as `index.md`/`index.markdown` — keep a single index file.
- Comments: Disqus (`joonhyoung-github-io`). Search: lunr with full-content indexing. Analytics: Google gtag (`G-R6WK8J8QD8`).
- Site skin is `air` (`minimal_mistakes_skin`); customize styling under `_sass/`.
- Various verification/ownership files (`google*.html`, `naver*.html`, `ads.txt`, `robots.txt`, `sitemap.xml`, `feed.xml`) are served as-is and should not be renamed.

## Architecture

Layout inheritance and includes come from the Minimal Mistakes theme (`_layouts/`, `_includes/`). Site-specific overrides are layered on top: `_config.yml` for site settings and build defaults, `_data/` for navigation and translations, `_sass/` for style overrides, and `assets/` for compiled CSS/JS/images. When a layout or include needs changing, override the theme file locally rather than editing the gem — the root-level `_layouts/` and `_includes/` already shadow the theme's copies.
