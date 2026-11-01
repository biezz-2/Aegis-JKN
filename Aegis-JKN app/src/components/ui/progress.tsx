import * as React from "react"
import { cn } from "@/lib/utils"

export interface ProgressProps {
  value?: number
  className?: string
  indicatorClassName?: string
}

function clampValue(value?: number) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return 0
  }
  return Math.min(100, Math.max(0, value))
}

function Progress({ value, className, indicatorClassName }: ProgressProps) {
  const clamped = clampValue(value)

  return (
    <div
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={value}
      className={cn(
        "h-2 w-full overflow-hidden rounded-full bg-secondary",
        className
      )}
    >
      <div
        className={cn("h-full bg-primary transition-all", indicatorClassName)}
        style={{ width: `${clamped}%` }}
      />
    </div>
  )
}

export { Progress }
