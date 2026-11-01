class ThemeStore {
  current = $state<"light" | "dark">("light");

  init() {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("aegis-theme") as "light" | "dark" | null;
      if (stored) {
        this.current = stored;
      } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        this.current = "dark";
      }
      this.apply();
    }
  }

  setTheme(t: "light" | "dark") {
    this.current = t;
    if (typeof window !== "undefined") {
      localStorage.setItem("aegis-theme", t);
      this.apply();
    }
  }

  toggle() {
    this.setTheme(this.current === "dark" ? "light" : "dark");
  }

  apply() {
    if (typeof document !== "undefined") {
      if (this.current === "dark") {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    }
  }
}

export const theme = new ThemeStore();
