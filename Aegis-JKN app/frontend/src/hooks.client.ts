import { reticle, registerStore, registerCapabilities } from "@reticlehq/browser";
import { appStore, TESTIDS, Sig } from "./reticle-dev";

if (import.meta.env.DEV) {
  try {
    registerStore("app", appStore);
    registerCapabilities({
      testids: TESTIDS,
      signals: Object.values(Sig),
      stores: ["app"]
    });
    reticle.connect({
      url: "ws://localhost:4400/reticle",
      token: "f7518685676f155447341e4012ea0320be862115893b5c90",
      projectId: "aegis-jkn-frontend"
    });
  } catch {
    // Ignore connection errors if daemon is offline
  }
}
