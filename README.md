# still-content

Static content repository for the [Still](https://github.com/JesperStockenstrand/still) app. Served as JSON via Vercel's CDN — no backend, no database, no cost.

## How it works

The Still app fetches these files on launch and caches them locally. If the device is offline, the app falls back to the last cached version (or bundled defaults on first launch).

The app checks `manifest.json` first. If `version` has not changed since the last fetch, the other files are not re-downloaded.

## Files

| File | Purpose |
|---|---|
| `manifest.json` | Version number and file index. App checks this on every launch. |
| `insights.json` | Short daily insights shown on the Home screen. |
| `articles.json` | Longer psychoeducation articles shown in the Learn tab. |
| `resources.json` | Curated books, podcasts, and therapy directories. |

## Adding or updating content

1. Edit the relevant JSON file directly on GitHub, or clone and push.
2. Bump `version` in `manifest.json` by 1.
3. Update `last_updated` in `manifest.json`.
4. Commit and push to `main` — Vercel deploys automatically.

The app will pick up the new content on next launch.

## Content guidelines

- **Tone:** Warm, plain language, empowering — never preachy or clinical.
- **Insights:** 1–2 sentences. Should stand alone without context.
- **Articles:** 3–5 minute read. Use `\n\n` for paragraph breaks, `**bold**` for emphasis.
- **Resources:** Include a brief, honest description. External URLs only — no affiliate links.

## JSON schemas

### `manifest.json`
```json
{
  "version": 1,
  "last_updated": "YYYY-MM-DD",
  "min_app_version": "1.0.0",
  "files": { "insights": "...", "articles": "...", "resources": "..." }
}
```

### `insights.json`
```json
{
  "insights": [
    {
      "id": "i001",
      "text": "Short insight text.",
      "article_id": "a001"
    }
  ]
}
```
`article_id` is optional — links the insight to a full article in `articles.json`.

### `articles.json`
```json
{
  "articles": [
    {
      "id": "a001",
      "title": "Article title",
      "summary": "One-sentence summary shown in the article list.",
      "tags": ["neuroscience", "dopamine"],
      "read_minutes": 4,
      "body": "Full article text. Use \\n\\n for paragraphs."
    }
  ]
}
```

### `resources.json`
```json
{
  "resources": [
    {
      "id": "r001",
      "title": "Resource title",
      "type": "book | podcast | directory",
      "author": "Author name or null",
      "description": "Brief description shown on the card.",
      "url": "https://..."
    }
  ]
}
```
