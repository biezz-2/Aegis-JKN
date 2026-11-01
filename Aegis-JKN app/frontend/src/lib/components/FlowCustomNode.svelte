<script lang="ts">
  import { Position, Handle, type NodeProps } from "@xyflow/svelte";
  import Icon from "./Icon.svelte";

  interface NodeCustomData {
    step?: string;
    title: string;
    subLabel: string;
    detail?: string;
    channel?: "topology" | "feature" | "semantic";
    channelIcon?: string;
    badgeStatus?: "ACTIVE" | "VERIFIED" | "ALERT" | "IDLE";
    borderColor?: string;
    accentColor?: string;
    isHighlighted?: boolean;
    hasTarget?: boolean;
    hasSource?: boolean;
    targetPosition?: Position;
    sourcePosition?: Position;
  }

  let {
    data,
    targetPosition = Position.Left,
    sourcePosition = Position.Right
  }: NodeProps = $props();

  const nodeData = $derived(data as unknown as NodeCustomData);

  const borderClass = $derived.by(() => {
    if (nodeData.channel === "topology") return "border-rose-500/80 shadow-rose-500/10";
    if (nodeData.channel === "feature") return "border-amber-500/80 shadow-amber-500/10";
    if (nodeData.channel === "semantic") return "border-teal-500/80 shadow-teal-500/10";
    if (nodeData.borderColor) return "";
    return "border-border";
  });

  const badgeConfig = $derived.by(() => {
    const status = nodeData.badgeStatus;
    if (status === "ACTIVE") {
      return {
        bg: "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30",
        dot: "bg-emerald-500 animate-pulse",
        text: "ACTIVE"
      };
    }
    if (status === "VERIFIED") {
      return {
        bg: "bg-teal-500/15 text-teal-600 dark:text-teal-400 border-teal-500/30",
        dot: "bg-teal-500",
        text: "VERIFIED"
      };
    }
    if (status === "ALERT") {
      return {
        bg: "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30",
        dot: "bg-rose-500 animate-ping",
        text: "ALERT"
      };
    }
    return {
      bg: "bg-muted text-muted-foreground border-border/40",
      dot: "bg-muted-foreground",
      text: "IDLE"
    };
  });
</script>

{#if nodeData.hasTarget !== false}
  <Handle
    type="target"
    position={nodeData.targetPosition ?? targetPosition}
    class="!w-2.5 !h-2.5 !bg-primary !border-2 !border-background"
  />
{/if}

<div
  class="relative rounded-xl border bg-card text-foreground px-3.5 py-2.5 shadow-sm transition-all duration-200 hover:shadow-md hover:scale-[1.01] {borderClass}"
  style={nodeData.borderColor ? `border-color: ${nodeData.borderColor};` : ""}
>
  <!-- Header: Channel/Step + Badge -->
  <div class="flex items-center justify-between gap-2 mb-1.5">
    <div class="flex items-center gap-1.5 min-w-0">
      {#if nodeData.channelIcon}
        <span
          class="flex items-center justify-center w-5 h-5 rounded-md text-xs shrink-0"
          style={nodeData.accentColor ? `background-color: ${nodeData.accentColor}20; color: ${nodeData.accentColor};` : ""}
        >
          <Icon name={nodeData.channelIcon} size={12} />
        </span>
      {/if}
      {#if nodeData.step}
        <span class="text-[10px] font-mono font-semibold tracking-wider text-muted-foreground uppercase truncate">
          {nodeData.step}
        </span>
      {/if}
    </div>

    {#if nodeData.badgeStatus}
      <span
        class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-mono font-bold tracking-tight border {badgeConfig.bg}"
      >
        <span class="w-1.5 h-1.5 rounded-full {badgeConfig.dot}"></span>
        <span>{badgeConfig.text}</span>
      </span>
    {/if}
  </div>

  <!-- Title -->
  <h4 class="text-xs font-bold text-foreground leading-tight tracking-tight mb-1">
    {nodeData.title}
  </h4>

  <!-- Dynamic Sub-label -->
  <p class="text-[11px] text-muted-foreground leading-relaxed">
    {nodeData.subLabel}
  </p>

  <!-- Metric or Detail Footer if provided -->
  {#if nodeData.detail}
    <div class="mt-2 pt-1.5 border-t border-border/50 flex items-center justify-between gap-1 text-[10px] font-mono tabular-nums">
      <span class="text-muted-foreground/80 truncate">{nodeData.detail}</span>
      {#if nodeData.channel}
        <span
          class="font-semibold uppercase text-[9px] px-1 rounded"
          style={nodeData.accentColor ? `background-color: ${nodeData.accentColor}15; color: ${nodeData.accentColor};` : ""}
        >
          {nodeData.channel}
        </span>
      {/if}
    </div>
  {/if}
</div>

{#if nodeData.hasSource !== false}
  <Handle
    type="source"
    position={nodeData.sourcePosition ?? sourcePosition}
    class="!w-2.5 !h-2.5 !bg-primary !border-2 !border-background"
  />
{/if}
