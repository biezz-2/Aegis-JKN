<script lang="ts">
  let {
    name,
    size = 18,
    class: className = "",
    strokeWidth = 2
  }: {
    name: string;
    size?: number;
    class?: string;
    strokeWidth?: number;
  } = $props();
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width={strokeWidth}
  stroke-linecap="round"
  stroke-linejoin="round"
  class={className}
>
  {#if name === "ShieldAlert" || name === "shield-alert"}
    <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" />
    <path d="M12 8v4" /><path d="M12 16h.01" />
  {:else if name === "ShieldCheck" || name === "shield-check"}
    <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" />
    <path d="m9 12 2 2 4-4" />
  {:else if name === "CheckCircle2" || name === "check-circle"}
    <circle cx="12" cy="12" r="10" /><path d="m9 12 2 2 4-4" />
  {:else if name === "AlertTriangle" || name === "alert-triangle"}
    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
  {:else if name === "Activity" || name === "activity"}
    <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
  {:else if name === "Layers" || name === "layers"}
    <path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z" /><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65" /><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65" />
  {:else if name === "Search" || name === "search"}
    <circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" />
  {:else if name === "Info" || name === "info"}
    <circle cx="12" cy="12" r="10" /><path d="M12 16v-4" /><path d="M12 8h.01" />
  {:else if name === "Filter" || name === "filter"}
    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
  {:else if name === "ChevronRight" || name === "chevron-right"}
    <path d="m9 18 6-6-6-6" />
  {:else if name === "ArrowLeft" || name === "arrow-left"}
    <path d="m12 19-7-7 7-7" /><path d="M19 12H5" />
  {:else if name === "ArrowRight" || name === "arrow-right"}
    <path d="M5 12h14" /><path d="m12 5 7 7-7 7" />
  {:else if name === "Sun" || name === "sun"}
    <circle cx="12" cy="12" r="4" /><path d="M12 2v2" /><path d="M12 20v2" /><path d="m4.93 4.93 1.41 1.41" /><path d="m17.66 17.66 1.41 1.41" /><path d="M2 12h2" /><path d="M20 12h2" /><path d="m6.34 17.66-1.41 1.41" /><path d="m19.07 4.93-1.41 1.41" />
  {:else if name === "Moon" || name === "moon"}
    <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
  {:else if name === "Download" || name === "download"}
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
  {:else if name === "Printer" || name === "printer"}
    <polyline points="6 9 6 2 18 2 18 9" /><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" /><rect width="12" height="8" x="6" y="14" />
  {:else if name === "Check" || name === "check"}
    <polyline points="20 6 9 17 4 12" />
  {:else if name === "X" || name === "x"}
    <path d="M18 6 6 18" /><path d="m6 6 12 12" />
  {:else if name === "Bot" || name === "bot"}
    <path d="M12 8V4H8" /><rect width="16" height="12" x="4" y="8" rx="2" /><path d="M2 14h2" /><path d="M20 14h2" /><path d="M15 13v2" /><path d="M9 13v2" />
  {:else if name === "Sparkles" || name === "sparkles"}
    <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
  {:else if name === "BarChart3" || name === "bar-chart-3"}
    <path d="M3 3v18h18" /><path d="M18 17V9" /><path d="M13 17V5" /><path d="M8 17v-3" />
  {:else if name === "User" || name === "user"}
    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
  {:else if name === "Stethoscope" || name === "stethoscope"}
    <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3" /><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4" /><circle cx="20" cy="10" r="2" />
  {:else if name === "Hospital" || name === "hospital"}
    <path d="M12 6v4" /><path d="M14 14h-4" /><path d="M14 18h-4" /><path d="M14 8h-4" /><path d="M18 12h.01" /><path d="M18 16h.01" /><path d="M18 20h.01" /><path d="M6 12h.01" /><path d="M6 16h.01" /><path d="M6 20h.01" /><rect width="16" height="20" x="4" y="2" rx="2" />
  {:else if name === "Syringe" || name === "syringe"}
    <path d="m18 2 4 4" /><path d="m17 7 3-3" /><path d="M19 9 8.7 19.3c-.4.4-1 .4-1.4 0l-2.6-2.6c-.4-.4-.4-1 0-1.4L15 5" /><path d="m9 11 4 4" /><path d="m5 19-3 3" /><path d="m14 4 6 6" />
  {:else if name === "ClipboardList" || name === "clipboard-list"}
    <rect width="8" height="4" x="8" y="2" rx="1" /><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" /><path d="M12 11h4" /><path d="M12 16h4" /><path d="M8 11h.01" /><path d="M8 16h.01" />
  {:else if name === "Keyboard" || name === "keyboard"}
    <rect width="20" height="16" x="2" y="4" rx="2" /><path d="M6 8h.001" /><path d="M10 8h.001" /><path d="M14 8h.001" /><path d="M18 8h.001" /><path d="M8 12h.001" /><path d="M12 12h.001" /><path d="M16 12h.001" /><path d="M7 16h10" />
  {:else if name === "Play" || name === "play"}
    <polygon points="6 3 20 12 6 21 6 3" />
  {:else if name === "Pause" || name === "pause"}
    <rect x="6" y="4" width="4" height="16" /><rect x="14" y="4" width="4" height="16" />
  {:else if name === "RotateCcw" || name === "rotate-ccw"}
    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" /><path d="M3 3v5h5" />
  {:else if name === "ExternalLink" || name === "external-link"}
    <path d="M15 3h6v6" /><path d="M10 14 21 3" /><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
  {:else if name === "GitBranch" || name === "git-branch"}
    <line x1="6" x2="6" y1="3" y2="15" /><circle cx="18" cy="6" r="3" /><circle cx="6" cy="18" r="3" /><path d="M18 9a9 9 0 0 1-9 9" />
  {:else if name === "Database" || name === "database"}
    <ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" /><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" />
  {:else if name === "FileText" || name === "file-text"}
    <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /><path d="M10 9H8" /><path d="M16 13H8" /><path d="M16 17H8" />
  {:else if name === "Menu" || name === "menu"}
    <line x1="4" x2="20" y1="12" y2="12" /><line x1="4" x2="20" y1="6" y2="6" /><line x1="4" x2="20" y1="18" y2="18" />
  {:else if name === "Volume2" || name === "volume-2"}
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" /><path d="M15.54 8.46a5 5 0 0 1 0 7.07" /><path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
  {:else if name === "VolumeX" || name === "volume-x"}
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" /><line x1="22" x2="16" y1="9" y2="15" /><line x1="16" x2="22" y1="9" y2="15" />
  {:else}
    <circle cx="12" cy="12" r="10" />
  {/if}
</svg>
