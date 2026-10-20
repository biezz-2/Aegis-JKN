import { NextResponse } from "next/server";

export async function GET() {
  try {
    return NextResponse.json({ message: "Hello, world!" });
  } catch {
    // Fail securely without exposing stack traces or internal implementation details
    return NextResponse.json(
      { error: "An unexpected error occurred." },
      { status: 500 }
    );
  }
}
