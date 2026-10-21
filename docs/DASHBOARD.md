# Dashboard Verifikator Aegis-JKN

Dashboard Aegis-JKN adalah SPA internal untuk menelaah **dataset klaim sintetis**. Ia membantu verifikator memprioritaskan pembacaan bukti; ia tidak terhubung ke SATUSEHAT, V-Claim, database, atau layanan inferensi.

> AI memberikan rekomendasi, bukan keputusan. Keputusan akhir ada pada verifikator.

## Dokumentasi

- [Arsitektur](../dashboard/docs/ARCHITECTURE.md)
- [Tech stack](../dashboard/docs/TECH_STACK.md)
- [Panduan penggunaan dan pengembangan](../dashboard/docs/README.md)
- [Deployment internal](../dashboard/docs/DEPLOYMENT.md)
- [Kontrak dataset](DATA_SCHEMA.md)
- [Makalah Aegis-JKN](makalah/Makalah_Aegis-JKN.md)

## Batasan data

Sumber kanonik tetap `docs/datasets/klaim-aegis-jkn-dataset.json`. Salinan aplikasi di `dashboard/src/data/` harus byte-identik. Sumber tidak memiliki tarif INA-CBG pembanding, graph edge produksi, atau nilai SHAP fitur numerik; UI tidak boleh membuat nilai tersebut.

Graf sindikat hanya muncul untuk label sindikat yang telah ada pada dataset dan diberi penanda sebagai representasi kelompok sintetis. Audit keputusan disimpan pada `localStorage` browser untuk demonstrasi; itu bukan rekam audit produksi.

## Rute

| Rute | Halaman |
|---|---|
| `/` | Landing page publik (Aegis JKN Flow). Ketiga tombol—"Mulai Trial Gratis", "Lihat Demo", dan "Mulai Integrasi Sekarang"—mengarah ke `/demo`. |
| `/demo` | **Dashboard Verifikator Aegis-JKN** — antrean klaim, EMR, bukti AI, graf sindikat, tindakan HITL, dan audit lokal. |

## Menjalankan

```bash
cd dashboard
npm install
npm run typecheck
npm test
npm run build
npm run dev
```

Aplikasi adalah SvelteKit (adapter-node). Server dev dikonfigurasi pada port **5175** dengan `strictPort`. Perangkat tepercaya dapat mengakses `http://<IP-LAN-host>:5175` atau `http://<IP-Tailscale-host>:5175`. Pastikan firewall mengizinkan TCP pada port tersebut; binding `0.0.0.0` tidak menyediakan autentikasi.

Untuk produksi lokal gunakan PM2 dari akar repositori:

```bash
cd dashboard && npm run build
cd .. && pm2 start ecosystem.config.cjs   # PORT=5175
pm2 logs aegis-dashboard
```

Gunakan tiga aksi manusia—**Setujui Klaim**, **Minta Konfirmasi RS**, dan **Tolak**—dengan catatan wajib. Aksi hanya menambah log lokal dan tidak mengubah dataset, risiko, atau rekomendasi sumber.
