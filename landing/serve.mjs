// Server statis tanpa dependensi untuk landing page.
//
// Dipakai karena `pm2 serve` bawaan PM2 tidak ada di dalam `ecosystem.config.cjs`
// sebagai app yang bisa di-restart, dan `landing/` butuh dilayani pada port
// sendiri dari dashboard (5175) supaya keduanya bisa hidup berdampingan.
//
// Batasan yang disengaja: hanya file statis, tanpa SPA fallback, tanpa
// directory listing. Path di luar akar dialihkan ke 404 — landing page tidak
// boleh serving file di luar `landing/`.
import { createServer } from 'node:http';
import { createReadStream } from 'node:fs';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(fileURLToPath(new URL('.', import.meta.url)));
const PORT = Number(process.env.PORT || 5176);
const HOST = process.env.HOST || '0.0.0.0';
/* URL dashboard verifikator. Disuntik ke HTML lewat placeholder
   `{{DASHBOARD_URL}}` supaya IP dan port tidak ditulis mati di markup. */
const DASHBOARD_URL = process.env.DASHBOARD_URL || 'http://127.0.0.1:5175';

const TYPES = {
	'.html': 'text/html; charset=utf-8',
	'.css': 'text/css; charset=utf-8',
	'.js': 'text/javascript; charset=utf-8',
	'.mjs': 'text/javascript; charset=utf-8',
	'.json': 'application/json; charset=utf-8',
	'.svg': 'image/svg+xml',
	'.png': 'image/png',
	'.jpg': 'image/jpeg',
	'.jpeg': 'image/jpeg',
	'.webp': 'image/webp',
	'.ico': 'image/x-icon',
	'.woff': 'font/woff',
	'.woff2': 'font/woff2',
	'.txt': 'text/plain; charset=utf-8'
};

/* Path dinormalisasi lalu diperiksa ulang terhadap ROOT. `normalize` saja
   belum cukup: `..%2f..%2f` bisa keluar dari akar setelah decode. */
function resolveSafe(urlPath) {
	const decoded = decodeURIComponent(urlPath.split('?')[0].split('#')[0]);
	const candidate = resolve(join(ROOT, normalize(decoded)));
	if (candidate !== ROOT && !candidate.startsWith(ROOT + sep)) return null;
	return candidate;
}

async function resolveFile(candidate) {
	try {
		const s = await stat(candidate);
		if (s.isDirectory()) {
			const index = join(candidate, 'index.html');
			const si = await stat(index);
			return si.isFile() ? { path: index, size: si.size } : null;
		}
		return { path: candidate, size: s.size };
	} catch {
		return null;
	}
}

const server = createServer(async (req, res) => {
	if (req.method !== 'GET' && req.method !== 'HEAD') {
		res.writeHead(405, { Allow: 'GET, HEAD' });
		return res.end('Method Not Allowed');
	}

	const candidate = resolveSafe(req.url || '/');
	const file = candidate ? await resolveFile(candidate) : null;

	if (!file) {
		res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
		return res.end('404 Not Found');
	}

	/* Placeholder `{{DASHBOARD_URL}}` di HTML diganti URL dashboard saat
	   request, supaya IP/port tidak perlu ditulis mati di markup. */
	if (file.path.endsWith('.html')) {
		const html = await readFile(file.path, 'utf8');
		const body = html.replaceAll('{{DASHBOARD_URL}}', DASHBOARD_URL);
		res.writeHead(200, {
			'Content-Type': 'text/html; charset=utf-8',
			'Content-Length': Buffer.byteLength(body),
			'Cache-Control': 'no-cache'
		});
		if (req.method === 'HEAD') return res.end();
		return res.end(body);
	}

	const type = TYPES[extname(file.path).toLowerCase()] || 'application/octet-stream';
	res.writeHead(200, {
		'Content-Type': type,
		'Content-Length': file.size,
		'Cache-Control': 'no-cache'
	});

	if (req.method === 'HEAD') return res.end();

	const stream = createReadStream(file.path);
	stream.on('error', () => res.destroy());
	stream.pipe(res);
});

server.listen(PORT, HOST, () => {
	console.log(`Aegis-JKN landing page berjalan di http://${HOST}:${PORT}`);
	console.log(`Tautan dashboard: ${DASHBOARD_URL}`);
});
