import { NextResponse } from "next/server";

/**
 * Health check showcase.
 *
 * Port dev showcase berada di rentang 3000-3050, yang tumpang tindih dengan
 * rentang alokasi port bridge WhatsApp Hermes (3001-3999). Saat Hermes memindai
 * port itu, ia mengirim `GET /health` ke showcase. Tanpa route ini, setiap probe
 * berakhir 404 dan muncul sebagai error di log dev.
 *
 * Balasan sengaja minimal dan tidak menyamar sebagai bridge Hermes: body ini
 * jujur (showcase hidup), bukan tiruan schema bridge yang memuat `session`.
 */
export async function GET() {
  return NextResponse.json({ status: "ok" });
}
