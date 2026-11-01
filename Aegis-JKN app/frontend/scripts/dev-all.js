#!/usr/bin/env node

/**
 * Aegis-JKN Unified Development Server Runner.
 * Concurrently starts:
 *   1. FastAPI Backend (Python Uvicorn) on http://127.0.0.1:8000
 *   2. SvelteKit Frontend (Vite) on http://localhost:5173
 * Handles cross-platform path resolution, color-coded logging, and clean SIGINT termination.
 */

import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Directory paths
const frontendDir = path.resolve(__dirname, "..");
const appDir = path.resolve(frontendDir, "..");
const backendDir = path.resolve(appDir, "src", "backend");

// Locate Python virtual environment executable
const venvPythonWin = path.join(backendDir, "venv", "Scripts", "python.exe");
const venvPythonUnix = path.join(backendDir, "venv", "bin", "python");

let pythonExec = "python";
if (process.platform === "win32" && fs.existsSync(venvPythonWin)) {
  pythonExec = venvPythonWin;
} else if (fs.existsSync(venvPythonUnix)) {
  pythonExec = venvPythonUnix;
}

console.log("\x1b[1m\x1b[36m%s\x1b[0m", "==================================================");
console.log("\x1b[1m\x1b[36m%s\x1b[0m", "  AEGIS-JKN UNIFIED DEVELOPMENT RUNNER");
console.log("\x1b[1m\x1b[36m%s\x1b[0m", "==================================================");
console.log(`\x1b[34m[INFO]\x1b[0m Frontend Dir : ${frontendDir}`);
console.log(`\x1b[34m[INFO]\x1b[0m Backend Dir  : ${backendDir}`);
console.log(`\x1b[34m[INFO]\x1b[0m Python Exec  : ${pythonExec}\n`);

// 1. Spawn FastAPI Backend (Uvicorn)
console.log("\x1b[36m[STARTING]\x1b[0m Meluncurkan FastAPI Backend (Uvicorn) pada port 8000...");
const backendProcess = spawn(
  pythonExec,
  ["-m", "uvicorn", "app.main:create_app", "--factory", "--host", "127.0.0.1", "--port", "8000"],
  {
    cwd: backendDir,
    env: { ...process.env, PYTHONPATH: appDir },
    shell: false,
  }
);

backendProcess.stdout.on("data", (data) => {
  const lines = data.toString().trim().split("\n");
  for (const line of lines) {
    if (line.trim()) {
      console.log(`\x1b[36m[BACKEND]\x1b[0m ${line}`);
    }
  }
});

backendProcess.stderr.on("data", (data) => {
  const lines = data.toString().trim().split("\n");
  for (const line of lines) {
    if (line.trim()) {
      console.log(`\x1b[33m[BACKEND LOG]\x1b[0m ${line}`);
    }
  }
});

backendProcess.on("error", (err) => {
  console.error("\x1b[31m[BACKEND ERROR]\x1b[0m", err);
});

// 2. Spawn Vite Frontend
console.log("\x1b[32m[STARTING]\x1b[0m Meluncurkan SvelteKit Frontend (Vite) pada port 5173...\n");
const npxCmd = process.platform === "win32" ? "npx.cmd" : "npx";
const frontendProcess = spawn(npxCmd, ["vite", "dev", "--port", "5173"], {
  cwd: frontendDir,
  env: process.env,
  shell: process.platform === "win32",
});

frontendProcess.stdout.on("data", (data) => {
  const lines = data.toString().trim().split("\n");
  for (const line of lines) {
    if (line.trim()) {
      console.log(`\x1b[32m[FRONTEND]\x1b[0m ${line}`);
    }
  }
});

frontendProcess.stderr.on("data", (data) => {
  const lines = data.toString().trim().split("\n");
  for (const line of lines) {
    if (line.trim()) {
      console.log(`\x1b[35m[FRONTEND LOG]\x1b[0m ${line}`);
    }
  }
});

frontendProcess.on("error", (err) => {
  console.error("\x1b[31m[FRONTEND ERROR]\x1b[0m", err);
});

// Clean shutdown handler
function cleanExit() {
  console.log("\n\x1b[33m[SHUTDOWN]\x1b[0m Menghentikan frontend dan backend server...");
  try {
    backendProcess.kill();
  } catch (e) {}
  try {
    frontendProcess.kill();
  } catch (e) {}
  process.exit(0);
}

process.on("SIGINT", cleanExit);
process.on("SIGTERM", cleanExit);
process.on("exit", () => {
  try {
    backendProcess.kill();
    frontendProcess.kill();
  } catch (e) {}
});
