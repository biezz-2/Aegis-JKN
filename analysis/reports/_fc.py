# -*- coding: utf-8 -*-
import io
P='10-competition.md'
t=io.open(P,encoding='utf-8').read()
old="**Konsekuensi #3 — ubah demo agar terlihat Know-how.** Alur demo wajib menampilkan: \"SmartClaim sudah jalan; Aegis melihat apa yang SmartClaim tidak bisa: klaim 003 dari puskesmas yang sama, dokter yang sama, 1 bulan lalu, Rp52,3 juta, dx gastritis, proc PCI.\" Itu momen yang membedakan."
new=(
"**Konsekuensi #3 — ubah demo agar terlihat Know-how.** Alur demo wajib menampilkan: \"SmartClaim sudah jalan; Aegis melihat apa yang SmartClaim tidak bisa: klaim 003 dari puskesmas yang sama, dokter yang sama, 1 bulan lalu, Rp52,3 juta, dx gastritis, proc PCI.\" Itu momen yang membedakan.\n\n"
"**Bukti independen dari kompetitor di kategori yang sama.** Repo `github.com/NalarAI/nalar-core` (HTTP 200, diakses 22 Okt 2026) secara eksplisit **menolak mencantumkan angka rupiah** di tabel hasilnya, dengan alasan: \"Angka rupiah sengaja tidak ditaruh di tabel ini. Ia bergeser empat puluh persen antar benih acak, jadi angka rupiah tidak boleh dikutip sendirian.\" Ini konfirmasi independen bahwa **nominal rupiah dari data sintetis memang tidak stabil** — sehingga temuan §7.2 (Rp507.370.000 tidak reproducible) bukan sekadar catatan pedantik, melainkan cacat metodologis nyata yang akan diakui juri teknis. Rekomendasi: adopsi kebijakan yang sama — tulis nominal sebagai \"estimasi pada 300 klaim simulasi\", sertakan seed, dan nyatakan rentang antar-seed."
)
assert old in t
t=t.replace(old,new)
io.open(P,'w',encoding='utf-8',newline='\n').write(t)
print('ok')
