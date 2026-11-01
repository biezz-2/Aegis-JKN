# Project Rules

## Web Search
- Untuk seluruh pencarian internet, SELALU gunakan tool MCP SearXNG (`mcp__searxng__searxng_web_search`).
- Untuk membaca URL hasil pencarian, gunakan `mcp__searxng__web_url_read`.
- Failover Search: Primary di `http://localhost:8088`, otomatis failover ke remote server `http://192.168.101.19:8089` jika lokal mati.
