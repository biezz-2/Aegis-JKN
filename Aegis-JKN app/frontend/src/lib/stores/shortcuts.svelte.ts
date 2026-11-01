import type { DetailTab } from "$lib/types";

class ShortcutsStore {
  helpOpen = $state(false);

  toggleHelp() {
    this.helpOpen = !this.helpOpen;
  }

  openHelp() {
    this.helpOpen = true;
  }

  closeHelp() {
    this.helpOpen = false;
  }
}

export const shortcutsModal = new ShortcutsStore();
