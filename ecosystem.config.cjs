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
        HOST: "0.0.0.0"
      }
    }
  ]
};
