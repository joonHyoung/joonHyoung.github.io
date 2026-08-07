# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal blog (Korean locale, "Redsnow's Anything Blog") built on the **Minimal Mistakes** Jekyll theme and deployed to **GitHub Pages** at https://joonhyoung.github.io.

This repository used to be a full copy of the Minimal Mistakes theme gem. The upstream scaffolding (`docs/`, `test/`, `CHANGELOG.md`, both `.gemspec` files, `Rakefile`, theme screenshots, `staticman.yml`) was removed — it was ~28 MB of the repo and none of it reached the build. What remains from the theme are the vendored `_layouts/`, `_includes/`, `_sass/` and `assets/` copies that the site actually renders from. Unused theme layouts and includes were pruned at the same time; recover any of it from git history if a feature (e.g. a dedicated search page, image galleries) is added later.

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

There is no lint step and no test suite.

The root `Gemfile` mirrors the CI `.github/Gemfile` (both use the `github-pages` metagem), so a local build matches production — verified by diffing the two builds' file lists. It previously contained only `gemspec`, which failed outright because two `.gemspec` files sat at the root; local development was impossible until that was fixed.

## Authoring content

- **Posts** go in `_posts/` named `YYYY-MM-DD-title.md`. Front matter uses `title`, `categories`, `tag`, `toc`, `last_modified_at`, `comments`, `mathjax`. Post-wide defaults (`layout: single`, author profile, read time, comments, share, related) are applied via `defaults:` in `_config.yml` — do not repeat them per post.
- **Standalone pages** go in `_pages/` with an explicit `permalink`. The category/tag/year archives (`category-archive.md`, `tag-archive.md`, `year-archive.md`) are Liquid-generated (`type: liquid`) and their permalinks (`/categories/`, `/tags/`, `/year-archive/`) must match the archive paths configured in `_config.yml`.
- Permalinks for posts are `/:categories/:title/`.
- **The home list has no server-side pagination.** `jekyll-paginate` is deliberately disabled (`paginate`/`paginate_path` are commented out in `_config.yml`) and `_layouts/home.html` renders *every* post, doing filter + sort + paging in client-side JS. This is required for correctness: the category filter can only hide rows that exist in the DOM, so with server-side paging a category whose posts fall on page 2 produced an empty page 1. Page size lives in the `per_page` variable in `_layouts/home.html`. Re-enabling `paginate` would regenerate `/page2/` and duplicate the home list.
- Top navigation is driven by `_data/navigation.yml`; UI string translations by `_data/ui-text.yml`.

## Key configuration facts

- **Deployment: GitHub Actions** (`.github/workflows/pages.yml`) — builds with Bundler using the CI-only `.github/Gemfile` (the `github-pages` metagem) and deploys via `actions/deploy-pages`. This requires **Settings → Pages → Build and deployment → Source = "GitHub Actions"**; if that setting is ever reset to "Deploy from a branch", the workflow's deploy step will fail. The CI Gemfile is separate from the root `Gemfile` (which is what local `bundle exec jekyll serve` uses). Confirm build status at https://github.com/joonHyoung/joonHyoung.github.io/actions.
  - **A push to `main` does not always trigger the workflow.** The daily "오늘의 AI 뉴스" automation committed `5534e68` to `main` on 2026-08-07 and no run started, leaving the site a day stale. GitHub suppresses `push` events for commits pushed with the default `GITHUB_TOKEN` (recursion guard). A `schedule:` trigger (`0 21 * * *` UTC = 06:00 KST, just after the automation's usual ~05:00 KST commit) was added as a safety net so a missed trigger self-heals within a day. `workflow_dispatch` is also enabled for manual runs. If a post is on `main` but not live, check whether a run exists for that SHA before debugging the build itself.
- **No external theme. Everything is vendored.** `remote_theme` was removed and `theme:` is set to an explicit empty value. All layouts, includes and sass live in this repo.
  - `theme:` must stay present-but-empty. **Deleting the key is not the same as leaving it blank** — the `github-pages` metagem fills in a default theme (`jekyll-theme-primer`) for a missing key, which publishes an unused 76 KB `assets/css/style.css`.
  - `remote_theme: mmistakes/minimal-mistakes` used to be set. The only thing it actually supplied was `_sass/minimal-mistakes/vendor/**` (breakpoint, susy, magnific-popup), which `_sass/minimal-mistakes.scss` imports; those files are now committed here. Every referenced layout and include was already local. Removing it was verified by diffing builds: all HTML byte-identical and the same `main.css` hash. It also stopped the remote theme from publishing 597 KB of its own `assets/js` sources (`plugins/`, `vendor/`, `_main.js`, `main.min.js.map`), and cut build time from ~4s to ~1s since nothing is fetched over the network.
  - Historical note: the legacy `--safe` Pages build only accepted whitelisted themes, which is why a `theme: jekyll-theme-hacker` line used to be load-bearing. The Actions workflow removed that constraint.
- The home page is `index.html` (`layout: home`, `author_profile: true`). Previously duplicated as `index.md`/`index.markdown` — keep a single index file.
- Comments: Disqus (`joonhyoung-github-io`). Search: lunr with full-content indexing. Analytics: Google gtag (`G-R6WK8J8QD8`).
- Site skin is `air` (`minimal_mistakes_skin`); customize styling under `_sass/`.
- Various verification/ownership files (`google*.html`, `naver*.html`, `ads.txt`, `robots.txt`, `sitemap.xml`, `feed.xml`) are served as-is and should not be renamed.

## Architecture

Layout inheritance and includes come from the Minimal Mistakes theme (`_layouts/`, `_includes/`). Site-specific overrides are layered on top: `_config.yml` for site settings and build defaults, `_data/` for navigation and translations, `_sass/` for style overrides, and `assets/` for compiled CSS/JS/images. When a layout or include needs changing, override the theme file locally rather than editing the gem — the root-level `_layouts/` and `_includes/` already shadow the theme's copies.
