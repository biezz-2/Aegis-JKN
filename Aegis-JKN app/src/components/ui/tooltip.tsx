"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface TooltipContextValue {
  open: boolean
  setOpen: (open: boolean) => void
}

const TooltipContext = React.createContext<TooltipContextValue | null>(null)

function useTooltipContext(component: string) {
  const ctx = React.useContext(TooltipContext)
  if (!ctx) throw new Error(`${component} must be used within <Tooltip>`)
  return ctx
}

const TooltipProvider = ({ children }: { children: React.ReactNode }) => (
  <>{children}</>
)

interface TooltipProps {
  children: React.ReactNode
  open?: boolean
  defaultOpen?: boolean
  onOpenChange?: (open: boolean) => void
  delayDuration?: number
}

const Tooltip = ({ children, open, defaultOpen = false, onOpenChange }: TooltipProps) => {
  const [internalOpen, setInternalOpen] = React.useState(defaultOpen)
  const isControlled = open !== undefined
  const currentOpen = isControlled ? open : internalOpen

  const setOpen = React.useCallback(
    (next: boolean) => {
      if (!isControlled) setInternalOpen(next)
      onOpenChange?.(next)
    },
    [isControlled, onOpenChange]
  )

  const contextValue = React.useMemo(
    () => ({ open: currentOpen, setOpen }),
    [currentOpen, setOpen]
  )

  return (
    <TooltipContext.Provider value={contextValue}>
      <span className="relative inline-block">{children}</span>
    </TooltipContext.Provider>
  )
}

interface TooltipTriggerProps extends React.HTMLAttributes<HTMLSpanElement> {
  asChild?: boolean
}

const TooltipTrigger = ({ className, children, ...props }: TooltipTriggerProps) => {
  const { open, setOpen } = useTooltipContext("TooltipTrigger")
  return (
    <span
      className={cn("inline-block", className)}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onFocus={() => setOpen(true)}
      onBlur={() => setOpen(false)}
      {...props}
    >
      {children}
    </span>
  )
}

interface TooltipContentProps extends React.HTMLAttributes<HTMLDivElement> {
  side?: "top" | "right" | "bottom" | "left"
  sideOffset?: number
  align?: "start" | "center" | "end"
  alignOffset?: number
}

const TooltipContent = ({
  className,
  children,
  side = "top",
  sideOffset = 4,
  ...props
}: TooltipContentProps) => {
  const { open } = useTooltipContext("TooltipContent")
  if (!open) return null

  return (
    <div
      role="tooltip"
      className={cn(
        "absolute z-50 whitespace-nowrap rounded-md bg-gray-900 px-3 py-1.5 text-sm text-white shadow-lg",
        side === "top" && "bottom-full left-1/2 -translate-x-1/2 mb-2",
        side === "bottom" && "top-full left-1/2 -translate-x-1/2 mt-2",
        side === "left" && "right-full top-1/2 -translate-y-1/2 mr-2",
        side === "right" && "left-full top-1/2 -translate-y-1/2 ml-2",
        className
      )}
      style={{ [side]: `${sideOffset}px` }}
      {...props}
    >
      {children}
    </div>
  )
}

export { TooltipProvider, Tooltip, TooltipTrigger, TooltipContent }