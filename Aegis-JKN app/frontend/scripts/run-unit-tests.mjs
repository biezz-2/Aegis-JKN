#!/usr/bin/env node
import { createServer } from "vite";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, "..");

async function runUnitTests() {
  console.log("==================================================");
  console.log("  AEGIS-JKN FRONTEND - UNIT TEST RUNNER");
  console.log("==================================================");

  const server = await createServer({
    root,
    resolve: {
      alias: {
        $lib: path.resolve(root, "src/lib"),
      },
    },
    server: { middlewareMode: true, hmr: false, ws: false },
    optimizeDeps: { noDiscovery: true },
    logLevel: "silent",
    appType: "custom",
  });

  try {
    const testFiles = [
      path.resolve(root, "src/lib/claims.test.ts"),
      path.resolve(root, "src/lib/stores/dashboard.test.ts"),
    ];

    for (const testFile of testFiles) {
      console.log(`\nRunning: ${path.relative(root, testFile)}`);
      console.log("-".repeat(50));
      await server.ssrLoadModule(testFile);
    }
  } catch (err) {
    console.error("Test execution failed:", err);
    process.exitCode = 1;
  } finally {
    await server.close();
  }
}

runUnitTests().catch((err) => {
  console.error("Unhandled test runner error:", err);
  process.exit(1);
});
