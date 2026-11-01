import { DICTS, type Lang, type Dict } from "$lib/data/i18n";

class LangStore {
  current = $state<Lang>("id");

  get t(): Dict {
    return DICTS[this.current];
  }

  setLang(l: Lang) {
    this.current = l;
    if (typeof window !== "undefined") {
      localStorage.setItem("aegis-lang", l);
    }
  }

  toggle() {
    this.setLang(this.current === "id" ? "en" : "id");
  }

  init() {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("aegis-lang") as Lang | null;
      if (stored === "id" || stored === "en") {
        this.current = stored;
      }
    }
  }
}

export const lang = new LangStore();
