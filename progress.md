# Project Summary: EpiMinds + Ball Site

## Goal
Run two separate websites locally, fixing 404s, SyntaxErrors, and ChunkLoadErrors.

## Folder Structure
- `e:\epwinds\` = EpiMinds site (Port 8080)
- `e:\epwinds\ball-site\` = Ball Site (Port 8081)

## Fixes Applied
1. **SyntaxError in inline JS** - Ran `fix_scripts.py` to decode HTML entities (`=&gt;` -> `=>`) inside `<script>` tags.
2. **404 for `.script.js` chunks** - Proxy servers serve local files first, then forward to remote if missing.
3. **404 for fonts/GLBs** - Proxied to `files.peachworlds.com` / `files.staging.peachworlds.com`.
4. **ChunkLoadError** - Fixed after chunks loaded via proxy.
5. **Ball Site serving wrong CSS** - Fixed proxy.py to use absolute `BASE_DIR` instead of current working directory.

## Proxy Servers
- **EpiMinds**: `python e:\epwinds\proxy.py` (serves `e:\epwinds\`, forwards to `https://epiminds.com`)
- **Ball Site**: `python e:\epwinds\ball-site\proxy.py` (serves `e:\epwinds\ball-site\`, forwards to `https://gentle-bjppjzad.peachworlds.com`)

## Local URLs
- EpiMinds: `http://127.0.0.1:8080`
- Ball Site: `http://127.0.0.1:8081`

## Next Steps
Both sites run. User wants to edit content (text, sections). Any change to local HTML/CSS/JS files shows immediately on refresh.
