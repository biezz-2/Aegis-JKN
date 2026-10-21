#!/usr/bin/env node
/**
 * Menjalankan ketiga bagian repositori secara bersamaan:
 *   - showcase MHGSL (Next.js)            → port 3000 (dialihkan kalau dipakai)
 *   - dashboard verifikator (SvelteKit)   → port 5275
 *   - landing page statis (node:http)     → port 5276
 *
 * Tanpa dependensi baru. `concurrently`/sejawatnya akan menambah paket yang
 * harus dipasang; yang dibutuhkan cuma spawn tiga proses anak, jadi itu
 * ditulis langsung di sini.
 *
 * Port dev sengaja berbeda dari port produksi PM2 (5175/5176) supaya
 * `npm run dev` tidak bentrok dengan instance yang sedang online. Kalau
 * keduanya memakai port sama, Vite (`strictPort: true`) gagal start.
 *
 * Override lewat env: DEV_SHOWCASE_PORT, DEV_DASHBOARD_PORT, DEV_LANDING_PORT,
 * DEV_PUBLIC_HOST.
 */
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { networkInterfaces } from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer } from 'node:net';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

/** Port bebas pertama mulai dari `start`. Kalau port sudah dipegang proses
 *  lain (mis. 3000 dipakai proxy proyek lain di mesin ini) ambil yang
 *  berikutnya, supaya `npm run dev` tetap jalan tanpa intervensi manual.
 *  Port hasil pemeriksaan ini dikunci lewat `strictPort` supaya tidak ada
 *  balapan antara pemeriksaan dan proses anak benar-benar bind. */
function pickFreePort(start) {
	return new Promise((resolvePort) => {
		const tryPort = (p) => {
			const srv = createServer();
			srv.once('error', () => {
				if (p >= start + 50) resolvePort(start);
				else tryPort(p + 1);
			});
			srv.listen(p, '0.0.0.0', () => srv.close(() => resolvePort(p)));
		};
		tryPort(start);
	});
}

/** IPv4 non-loopback pertama. Dipakai untuk tautan antar-aplikasi supaya
 *  tautannya tetap berlaku saat dibuka dari perangkat lain (ponsel) di
 *  jaringan yang sama, bukan hanya dari localhost. */
function lanIPv4() {
	for (const addrs of Object.values(networkInterfaces())) {
		for (const a of addrs || []) {
			if (a.family === 'IPv4' && !a.internal) return a.address;
		}
	}
	return '127.0.0.1';
}

const HOST = process.env.DEV_PUBLIC_HOST || lanIPv4();

const SHOWCASE_PORT = await pickFreePort(Number(process.env.DEV_SHOWCASE_PORT || 3000));
const DASHBOARD_PORT = await pickFreePort(Number(process.env.DEV_DASHBOARD_PORT || 5275));
const LANDING_PORT = await pickFreePort(Number(process.env.DEV_LANDING_PORT || 5276));

const DASHBOARD_URL = `http://${HOST}:${DASHBOARD_PORT}`;
const LANDING_URL = `http://${HOST}:${LANDING_PORT}`;

const services = [
	{
		name: 'showcase',
		color: '\u001b[36m',
		bin: resolve(ROOT, 'node_modules/next/dist/bin/next'),
		args: ['dev', '--port', String(SHOWCASE_PORT)],
		cwd: ROOT,
		env: {},
		ready: /Local:\s+(http:\/\/\S+)/,
		url: `http://localhost:${SHOWCASE_PORT}`
	},
	{
		name: 'dashboard',
		color: '\u001b[35m',
		bin: resolve(ROOT, 'dashboard/node_modules/vite/bin/vite.js'),
		args: ['dev', '--port', String(DASHBOARD_PORT), '--strictPort', '--host', '0.0.0.0'],
		cwd: resolve(ROOT, 'dashboard'),
		env: { PUBLIC_LANDING_URL: LANDING_URL },
		ready: /Local:\s+(http:\/\/\S+)/,
		url: DASHBOARD_URL
	},
	{
		name: 'landing',
		color: '\u001b[32m',
		bin: resolve(ROOT, 'landing/serve.mjs'),
		args: [],
		cwd: resolve(ROOT, 'landing'),
		env: { PORT: String(LANDING_PORT), HOST: '0.0.0.0', DASHBOARD_URL },
		ready: /landing page berjalan/,
		url: LANDING_URL
	}
];

const missing = services.filter((s) => !existsSync(s.bin));
if (missing.length) {
	console.error('Berkas berikut belum ada — jalankan `npm install` dulu:');
	for (const s of missing) console.error(`  ${s.name}: ${s.bin.replace(ROOT + '/', '')}`);
	process.exit(1);
}

const RESET = '\u001b[0m';
const DIM = '\u001b[2m';
const children = [];
const ready = new Set();
let summaryShown = false;

function prefix(name, color, chunk) {
	return chunk
		.toString()
		.split('\n')
		.filter((line, i, arr) => line.length > 0 || i < arr.length - 1)
		.map((line) => `${color}[${name}]${RESET} ${line}`)
		.join('\n');
}

function showSummary() {
	if (summaryShown) return;
	summaryShown = true;
	const all = [
		...new Set(
			Object.values(networkInterfaces())
				.flat()
				.filter((a) => a && a.family === 'IPv4')
				.map((a) => a.address)
		)
	];
	console.log(`\n${DIM}────────────────────────────────────────────────────────────${RESET}`);
	console.log(`  ${'showcase'.padEnd(10)} http://localhost:${SHOWCASE_PORT}`);
	console.log(`  ${'dashboard'.padEnd(10)} ${DASHBOARD_URL}`);
	console.log(`  ${'landing'.padEnd(10)} ${LANDING_URL}`);
	console.log(`${DIM}────────────────────────────────────────────────────────────${RESET}`);
	console.log(`${DIM}  alamat lain di mesin ini: ${all.join(', ')}`);
	console.log(`  produksi PM2: dashboard :5175, landing :5176${RESET}\n`);
}

for (const svc of services) {
	const child = spawn(process.execPath, [svc.bin, ...svc.args], {
		cwd: svc.cwd,
		env: { ...process.env, ...svc.env },
		stdio: ['ignore', 'pipe', 'pipe']
	});
	children.push(child);

	let pending = '';
	const onData = (chunk) => {
		pending += chunk.toString();
		const lines = pending.split('\n');
		pending = lines.pop() ?? '';
		for (const line of lines) {
			console.log(prefix(svc.name, svc.color, line));
			if (svc.ready.test(line) && !ready.has(svc.name)) {
				ready.add(svc.name);
				if (ready.size === services.length) showSummary();
			}
		}
	};
	child.stdout.on('data', onData);
	child.stderr.on('data', onData);

	child.on('exit', (code, signal) => {
		console.log(prefix(svc.name, svc.color, `selesai (${signal || `kode ${code}`})`));
		shutdown(code ?? 0);
	});
	child.on('error', (err) => {
		console.error(prefix(svc.name, svc.color, `gagal start: ${err.message}`));
		shutdown(1);
	});
}

let shuttingDown = false;
function shutdown(code) {
	if (shuttingDown) return;
	shuttingDown = true;
	for (const c of children) {
		if (!c.killed) c.kill('SIGTERM');
	}
	setTimeout(() => process.exit(code), 300).unref();
}

process.on('SIGINT', () => shutdown(0));
process.on('SIGTERM', () => shutdown(0));

// Ringkasan tetap tampil kalau ada layanan yang tidak pernah mencetak baris
// "ready" (mis. karena format log Next.js berubah).
setTimeout(showSummary, 15000).unref();
