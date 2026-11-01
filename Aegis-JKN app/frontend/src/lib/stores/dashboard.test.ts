import test, { describe, it, beforeEach } from "node:test";
import assert from "node:assert/strict";
import {
  dashboard,
  DashboardStore,
  sha256,
  buildAuditPayload,
  verifyAuditChain,
} from "./dashboard.svelte";
import type { Claim, HitlAction, LayoutMode, DetailTab, AuditLogEntry } from "$lib/types";

// ============================================================================
// SUITE 1: PEMILIHAN KLAIM DAN UPDATE KPI KALKULASI
// ============================================================================

describe("Dashboard Store - Pemilihan Klaim dan Update KPI", () => {
  let store: DashboardStore;

  beforeEach(() => {
    store = new DashboardStore();
  });

  describe("Pemilihan Klaim (Claim Selection)", () => {
    it("memiliki default klaim terpilih KLM001", () => {
      assert.strictEqual(store.selectedClaimId, "KLM001");
      assert.ok(store.selectedClaim, "selectedClaim harus terdefinisi");
      assert.strictEqual(store.selectedClaim?.id, "KLM001");
    });

    it("memperbarui selectedClaimId dan selectedClaim saat selectClaim dipanggil", () => {
      store.selectClaim("KLM002");
      assert.strictEqual(store.selectedClaimId, "KLM002");
      assert.strictEqual(store.selectedClaim?.id, "KLM002");

      store.selectClaim("KLM003");
      assert.strictEqual(store.selectedClaimId, "KLM003");
      assert.strictEqual(store.selectedClaim?.id, "KLM003");
    });

    it("menangani ID klaim yang tidak ada dengan fallback ke klaim pertama secara anggun", () => {
      store.selectClaim("KLM-TIDAK-ADA-999");
      assert.strictEqual(store.selectedClaimId, "KLM-TIDAK-ADA-999");
      // Fallback ke claims[0] agar UI tidak crash
      assert.ok(store.selectedClaim);
      assert.strictEqual(store.selectedClaim?.id, store.claims[0].id);
    });

    it("menjaga konsistensi data klaim saat navigasi berulang", () => {
      const targetIds = ["KLM001", "KLM002", "KLM003", "KLM004", "KLM005"];
      for (const id of targetIds) {
        store.selectClaim(id);
        assert.strictEqual(store.selectedClaim?.id, id);
        assert.ok(typeof store.selectedClaim?.costRp === "number");
        assert.ok(typeof store.selectedClaim?.fraudScore === "number");
      }
    });
  });

  describe("Kalkulasi KPI Awal (Initial KPI Calculations)", () => {
    it("menghitung total klaim dengan akurat", () => {
      assert.strictEqual(store.kpi.total, store.claims.length);
      assert.ok(store.kpi.total > 0, "Total klaim harus lebih dari 0");
    });

    it("menghitung agregasi status risiko dan eskalasi secara tepat", () => {
      const expectedEscalate = store.claims.filter(
        (c) => c.status === "escalate" || c.risk === "fraud"
      ).length;
      assert.strictEqual(store.kpi.escalateCount, expectedEscalate);

      const expectedHigh = store.claims.filter((c) => c.risk === "high").length;
      assert.strictEqual(store.kpi.highRiskCount, expectedHigh);

      const expectedReview = store.claims.filter(
        (c) => c.status === "review" && c.risk !== "fraud"
      ).length;
      assert.strictEqual(store.kpi.reviewCount, expectedReview);

      const expectedAutoClear = store.claims.filter(
        (c) => c.status === "auto_clear"
      ).length;
      assert.strictEqual(store.kpi.autoClearCount, expectedAutoClear);

      const expectedContradictions = store.claims.filter(
        (c) => c.hasContradiction
      ).length;
      assert.strictEqual(store.kpi.contradictionCount, expectedContradictions);
    });

    it("menghitung total biaya (totalCostRp) dari seluruh klaim", () => {
      const expectedTotalCost = store.claims.reduce((acc, c) => acc + c.costRp, 0);
      assert.strictEqual(store.kpi.totalCostRp, expectedTotalCost);
      assert.ok(store.kpi.totalCostRp > 0, "Total cost harus lebih dari 0");
    });
  });

  describe("Update KPI Rekalkulasi Saat Keputusan HITL Dicatat", () => {
    it("memperbarui approvedCostRp ketika verifikator menyetujui klaim berstatus review", async () => {
      // Cari klaim review yang belum diverifikasi
      const reviewClaim = store.claims.find(
        (c) => c.status === "review" && !c.verifiedStatus
      );
      assert.ok(reviewClaim, "Harus ada klaim review untuk pengujian");

      const initialApprovedCost = store.kpi.approvedCostRp;
      store.selectClaim(reviewClaim.id);

      await store.recordHitlDecision("APPROVE", "Lolos audit berkas rekam medis lengkap");

      // Cek klaim lokal terupdate
      const updatedClaim = store.claims.find((c) => c.id === reviewClaim.id);
      assert.strictEqual(updatedClaim?.verifiedStatus, "APPROVE");

      // approvedCostRp harus bertambah sebesar biaya klaim tersebut
      const expectedApprovedCost = initialApprovedCost + reviewClaim.costRp;
      assert.strictEqual(store.kpi.approvedCostRp, expectedApprovedCost);
    });

    it("memperbarui preventedCostRp ketika verifikator melakukan eskalasi ke P2PK", async () => {
      // Cari klaim review yang belum diverifikasi
      const targetClaim = store.claims.find(
        (c) => c.status === "review" && !c.verifiedStatus
      );
      assert.ok(targetClaim, "Harus ada klaim review untuk pengujian");

      const initialPreventedCost = store.kpi.preventedCostRp;
      store.selectClaim(targetClaim.id);

      await store.recordHitlDecision(
        "ESCALATE_P2PK",
        "Terindikasi phantom billing - eskalasi ke tim P2PK"
      );

      const updatedClaim = store.claims.find((c) => c.id === targetClaim.id);
      assert.strictEqual(updatedClaim?.verifiedStatus, "ESCALATE_P2PK");

      // preventedCostRp harus bertambah sebesar biaya klaim yang dicegah
      const expectedPreventedCost = initialPreventedCost + targetClaim.costRp;
      assert.strictEqual(store.kpi.preventedCostRp, expectedPreventedCost);
    });

    it("memperbarui KPI dengan benar saat status beralih dari APPROVE ke ESCALATE_P2PK", async () => {
      const claim = store.claims.find(
        (c) => c.status === "review" && !c.verifiedStatus
      );
      assert.ok(claim);

      store.selectClaim(claim.id);

      // Langkah 1: Approve
      await store.recordHitlDecision("APPROVE", "Persetujuan awal");
      const approvedCostAfter1 = store.kpi.approvedCostRp;
      const preventedCostAfter1 = store.kpi.preventedCostRp;

      // Langkah 2: Revisi keputusan jadi Escalate P2PK
      await store.recordHitlDecision(
        "ESCALATE_P2PK",
        "Ditemukan bukti baru pemalsuan berkas laboratorium"
      );

      // approvedCostRp harus berkurang sebesar biaya klaim
      assert.strictEqual(
        store.kpi.approvedCostRp,
        approvedCostAfter1 - claim.costRp
      );
      // preventedCostRp harus bertambah sebesar biaya klaim
      assert.strictEqual(
        store.kpi.preventedCostRp,
        preventedCostAfter1 + claim.costRp
      );
    });
  });
});

// ============================================================================
// SUITE 2: PERGANTIAN MODE LAYOUT (LAYOUT MODE SWITCHING)
// ============================================================================

describe("Dashboard Store - Pergantian Mode Layout", () => {
  let store: DashboardStore;

  beforeEach(() => {
    store = new DashboardStore();
  });

  it("memiliki mode layout default 'dual'", () => {
    assert.strictEqual(store.layoutMode, "dual");
  });

  it("dapat beralih ke mode 'full-queue'", () => {
    store.setLayoutMode("full-queue");
    assert.strictEqual(store.layoutMode, "full-queue");
  });

  it("dapat beralih ke mode 'full-detail'", () => {
    store.setLayoutMode("full-detail");
    assert.strictEqual(store.layoutMode, "full-detail");
  });

  it("dapat kembali ke mode 'dual' dari mode manapun", () => {
    store.setLayoutMode("full-queue");
    store.setLayoutMode("dual");
    assert.strictEqual(store.layoutMode, "dual");

    store.setLayoutMode("full-detail");
    store.setLayoutMode("dual");
    assert.strictEqual(store.layoutMode, "dual");
  });

  it("mendukung siklus transisi seluruh varian LayoutMode yang valid", () => {
    const modes: LayoutMode[] = ["dual", "full-queue", "full-detail", "dual"];
    for (const mode of modes) {
      store.setLayoutMode(mode);
      assert.strictEqual(store.layoutMode, mode);
    }
  });

  describe("Pengaturan Lebar Panel (Panel Width Resizing & Clamping)", () => {
    it("memiliki lebar panel kiri default 38 persen", () => {
      assert.strictEqual(store.leftPanelWidth, 38);
    });

    it("memperbarui lebar panel dalam batas aman [25, 60]", () => {
      store.setPanelWidth(50);
      assert.strictEqual(store.leftPanelWidth, 50);

      store.setPanelWidth(30);
      assert.strictEqual(store.leftPanelWidth, 30);
    });

    it("membatasi batas bawah (clamp minimum) pada 25%", () => {
      store.setPanelWidth(15);
      assert.strictEqual(store.leftPanelWidth, 25);

      store.setPanelWidth(-10);
      assert.strictEqual(store.leftPanelWidth, 25);
    });

    it("membatasi batas atas (clamp maximum) pada 60%", () => {
      store.setPanelWidth(75);
      assert.strictEqual(store.leftPanelWidth, 60);

      store.setPanelWidth(100);
      assert.strictEqual(store.leftPanelWidth, 60);
    });
  });

  describe("Pergantian Tab Detail (Detail Tab Navigation)", () => {
    it("memiliki tab aktif default 'emr'", () => {
      assert.strictEqual(store.activeDetailTab, "emr");
    });

    it("dapat beralih ke seluruh tab detail yang valid (ai, flow, graphiti, audit, emr)", () => {
      const tabs: DetailTab[] = ["ai", "flow", "graphiti", "audit", "emr"];
      for (const tab of tabs) {
        store.setDetailTab(tab);
        assert.strictEqual(store.activeDetailTab, tab);
      }
    });
  });
});

// ============================================================================
// SUITE 3: PEMBENTUKAN PAYLOAD HASH SHA-256 PADA RANTAI AUDIT LOG
// ============================================================================

describe("Kriptografi Audit Log - Pembentukan Payload Hash SHA-256", () => {
  it("menghasilkan hash SHA-256 yang valid sesuai vektor uji standar NIST", async () => {
    // Vektor kosong: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    const hashEmpty = await sha256("");
    assert.strictEqual(
      hashEmpty,
      "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    );

    // Vektor "abc": ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
    const hashAbc = await sha256("abc");
    assert.strictEqual(
      hashAbc,
      "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );

    // Vektor "test": 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
    const hashTest = await sha256("test");
    assert.strictEqual(
      hashTest,
      "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    );
  });

  it("membentuk format payload audit secara deterministik dengan delimiter pipa (|)", () => {
    const payload = buildAuditPayload({
      prevHash: "0000000000000000000000000000000000000000000000000000000000000000",
      timestamp: "2026-10-25T08:00:00.000Z",
      claimId: "KLM001",
      action: "APPROVE",
      verifierId: "VERIF-JKN-0891",
      note: "Catatan verifikasi audit",
      fraudScore: 0.15,
    });

    const expected =
      "0000000000000000000000000000000000000000000000000000000000000000|2026-10-25T08:00:00.000Z|KLM001|APPROVE|VERIF-JKN-0891|Catatan verifikasi audit|0.15";
    assert.strictEqual(payload, expected);

    // Verifikasi jumlah segmen payload tepat 7 field
    const segments = payload.split("|");
    assert.strictEqual(segments.length, 7);
    assert.strictEqual(segments[0], "0000000000000000000000000000000000000000000000000000000000000000");
    assert.strictEqual(segments[1], "2026-10-25T08:00:00.000Z");
    assert.strictEqual(segments[2], "KLM001");
    assert.strictEqual(segments[3], "APPROVE");
    assert.strictEqual(segments[4], "VERIF-JKN-0891");
    assert.strictEqual(segments[5], "Catatan verifikasi audit");
    assert.strictEqual(segments[6], "0.15");
  });

  it("memulai entri pertama (genesis) dengan prevHash 64 karakter nol", async () => {
    const store = new DashboardStore();
    store.selectClaim("KLM001");

    const entry = await store.recordHitlDecision("APPROVE", "Genesis entry audit log");
    assert.ok(entry, "Entri harus berhasil dibuat");

    const GENESIS_PREV_HASH = "0000000000000000000000000000000000000000000000000000000000000000";
    assert.strictEqual(entry.prevHash, GENESIS_PREV_HASH);
    assert.match(entry.hash, /^[0-9a-f]{64}$/, "Hash harus hex SHA-256 64 karakter");
    assert.ok(entry.signature.startsWith("ed25519_sig_"));
    assert.strictEqual(entry.signature, `ed25519_sig_${entry.hash.slice(0, 16)}`);
  });

  it("merangkai hash secara sekuensial (prevHash -> currHash) antar beberapa entri", async () => {
    const store = new DashboardStore();

    // Entri 1
    store.selectClaim("KLM001");
    const entry1 = await store.recordHitlDecision("APPROVE", "Audit 1 lolos");
    assert.ok(entry1);

    // Entri 2
    store.selectClaim("KLM002");
    const entry2 = await store.recordHitlDecision(
      "CLARIFY_RS",
      "Perlu konfirmasi resep obat"
    );
    assert.ok(entry2);

    // Entri 3
    store.selectClaim("KLM003");
    const entry3 = await store.recordHitlDecision(
      "ESCALATE_P2PK",
      "Klaim terindikasi fiktif"
    );
    assert.ok(entry3);

    // Periksa keterkaitan rantai kriptografis
    const GENESIS_PREV_HASH = "0000000000000000000000000000000000000000000000000000000000000000";
    assert.strictEqual(entry1.prevHash, GENESIS_PREV_HASH);
    assert.strictEqual(entry2.prevHash, entry1.hash, "prevHash entry2 harus sama dengan hash entry1");
    assert.strictEqual(entry3.prevHash, entry2.hash, "prevHash entry3 harus sama dengan hash entry2");

    // Semua hash harus unik dan tidak boleh ada tabrakan
    assert.notStrictEqual(entry1.hash, entry2.hash);
    assert.notStrictEqual(entry2.hash, entry3.hash);

    // Rantai utuh harus lolos verifikasi penuh
    const verification = await verifyAuditChain(store.auditLogs);
    assert.strictEqual(verification.valid, true);
  });
});

// ============================================================================
// SUITE 4: PENCEGAHAN MANIPULASI HASH (TAMPER-EVIDENCE & DETECTION)
// ============================================================================

describe("Kriptografi Audit Log - Pencegahan Manipulasi Hash", () => {
  let store: DashboardStore;
  let cleanLogs: AuditLogEntry[];

  beforeEach(async () => {
    store = new DashboardStore();

    // Buat 3 entri asli yang valid
    store.selectClaim("KLM001");
    await store.recordHitlDecision("APPROVE", "Catatan putusan pertama");

    store.selectClaim("KLM002");
    await store.recordHitlDecision("CLARIFY_RS", "Catatan putusan kedua");

    store.selectClaim("KLM003");
    await store.recordHitlDecision("ESCALATE_P2PK", "Catatan putusan ketiga");

    cleanLogs = JSON.parse(JSON.stringify(store.auditLogs));
  });

  it("memverifikasi bahwa buku besar audit log yang asli dan tidak diubah adalah 100% valid", async () => {
    const result = await verifyAuditChain(cleanLogs);
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.brokenIndex, undefined);
  });

  it("mendeteksi manipulasi pada catatan verifikator (tampered note)", async () => {
    const tamperedLogs: AuditLogEntry[] = JSON.parse(JSON.stringify(cleanLogs));
    // Manipulasi catatan pada entri ke-1 tanpa mengubah hash
    tamperedLogs[1].note = "Catatan diubah secara ilegal oleh pihak tidak bertanggung jawab";

    const result = await verifyAuditChain(tamperedLogs);
    assert.strictEqual(result.valid, false, "Manipulasi note harus terdeteksi");
    assert.strictEqual(result.brokenIndex, 1, "Indeks manipulasi harus teridentifikasi tepat");
    assert.match(result.reason || "", /Manipulasi payload terdeteksi/);
  });

  it("mendeteksi manipulasi pada aksi putusan verifikator (tampered action)", async () => {
    const tamperedLogs: AuditLogEntry[] = JSON.parse(JSON.stringify(cleanLogs));
    // Ubah aksi dari ESCALATE_P2PK menjadi APPROVE secara sepihak
    tamperedLogs[2].action = "APPROVE";

    const result = await verifyAuditChain(tamperedLogs);
    assert.strictEqual(result.valid, false, "Manipulasi aksi harus terdeteksi");
    assert.strictEqual(result.brokenIndex, 2);
    assert.match(result.reason || "", /Manipulasi payload terdeteksi/);
  });

  it("mendeteksi manipulasi pada fraud score AI (tampered aiScore)", async () => {
    const tamperedLogs: AuditLogEntry[] = JSON.parse(JSON.stringify(cleanLogs));
    // Turunkan skor fraud dari nilai asli ke nilai rendah palsu (misal 0.05)
    tamperedLogs[2].aiScore = 0.05;

    const result = await verifyAuditChain(tamperedLogs);
    assert.strictEqual(result.valid, false, "Manipulasi skor fraud harus terdeteksi");
    assert.strictEqual(result.brokenIndex, 2);
  });

  it("mendeteksi pemutusan rantai jika penyerang memperbarui hash entri tapi tidak entri berikutnya", async () => {
    const tamperedLogs: AuditLogEntry[] = JSON.parse(JSON.stringify(cleanLogs));
    // Penyerang mengubah note entri 1 dan sengaja menghitung ulang hash entri 1
    tamperedLogs[1].note = "Note dipalsukan";
    const newPayload = buildAuditPayload({
      prevHash: tamperedLogs[1].prevHash,
      timestamp: tamperedLogs[1].timestampIso!,
      claimId: tamperedLogs[1].claimId!,
      action: tamperedLogs[1].action as string,
      verifierId: tamperedLogs[1].verifierId!,
      note: tamperedLogs[1].note!,
      fraudScore: tamperedLogs[1].aiScore!,
    });
    tamperedLogs[1].hash = await sha256(newPayload);

    // Namun entri ke-2 masih memiliki prevHash yang menunjuk ke hash lama entri 1!
    const result = await verifyAuditChain(tamperedLogs);
    assert.strictEqual(result.valid, false);
    // Rantai putus di entri 2 karena prevHash tidak cocok dengan hash entri 1 yang baru
    assert.strictEqual(result.brokenIndex, 2);
    assert.match(result.reason || "", /Rantai hash terputus/);
  });

  it("mendeteksi manipulasi pada genesis block prevHash (non-zero genesis)", async () => {
    const tamperedLogs: AuditLogEntry[] = JSON.parse(JSON.stringify(cleanLogs));
    // Ubah prevHash entri pertama dari 64 nol menjadi nilai lain
    tamperedLogs[0].prevHash = "1111111111111111111111111111111111111111111111111111111111111111";

    const result = await verifyAuditChain(tamperedLogs);
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.brokenIndex, 0);
    assert.match(result.reason || "", /Genesis block prevHash tidak valid/);
  });

  it("mendeteksi manipulasi jika sebuah entri dihapus di tengah-tengah rantai", async () => {
    const tamperedLogs: AuditLogEntry[] = JSON.parse(JSON.stringify(cleanLogs));
    // Hapus entri tengah (indeks 1)
    tamperedLogs.splice(1, 1);

    // Sekarang entri ke-1 (sebelumnya entri 2) memiliki prevHash yang menunjuk ke hash entri yang dihapus,
    // padahal entri sebelumnya adalah entri 0!
    const result = await verifyAuditChain(tamperedLogs);
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.brokenIndex, 1);
    assert.match(result.reason || "", /Rantai hash terputus/);
  });

  it("menguji method store verifyAuditTrail secara langsung", async () => {
    const result = await store.verifyAuditTrail();
    assert.strictEqual(result.valid, true);

    // Ubah salah satu log di store
    store.auditLogs[0].note = "Tindakan manipulasi langsung pada memori store";
    const tamperedResult = await store.verifyAuditTrail();
    assert.strictEqual(tamperedResult.valid, false);
    assert.strictEqual(tamperedResult.brokenIndex, 0);
  });
});
