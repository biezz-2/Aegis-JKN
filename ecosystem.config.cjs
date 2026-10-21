module.exports = {
  apps: [
    {
      name: "aegis-dashboard",
      script: "build/index.js",
      cwd: "/home/biezz/Documents/Project/coding/Aegis-JKN/dashboard",
      interpreter: "node",
      autorestart: true,
      watch: false,
      max_memory_restart: "500M",
      env: {
        NODE_ENV: "production",
        PORT: "5175",
        HOST: "0.0.0.0",
        PUBLIC_LANDING_URL: "http://100.87.184.112:5176"
      }
    },
    {
      // Landing page statis. Port terpisah dari dashboard (5175) supaya
      // keduanya bisa hidup berdampingan tanpa proxy rewrite.
      name: "aegis-landing",
      script: "serve.mjs",
      cwd: "/home/biezz/Documents/Project/coding/Aegis-JKN/landing",
      interpreter: "node",
      autorestart: true,
      watch: false,
      max_memory_restart: "200M",
      env: {
        NODE_ENV: "production",
        PORT: "5176",
        HOST: "0.0.0.0",
        DASHBOARD_URL: "http://100.87.184.112:5175"
      }
    }
  ]
};
