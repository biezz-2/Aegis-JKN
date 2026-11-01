"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { Slot } from "@radix-ui/react-slot"

interface PopoverContextValue {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const PopoverContext = React.createContext<PopoverContextValue | null>(null)

function usePopoverContext() {
  const ctx = React.useContext(PopoverContext)
  if (!ctx) throw new Error("Popover sub-components must be used within <Popover>")
  return ctx
}

interface PopoverProps {
  open?: boolean
  defaultOpen?: boolean
  onOpenChange?: (open: boolean) => void
  children: React.ReactNode
}

const Popover = ({ open, defaultOpen = false, onOpenChange, children }: PopoverProps) => {
  const [internalOpen, setInternalOpen] = React.useState(defaultOpen)
  const isControlled = open !== undefined
  const currentOpen = isControlled ? open : internalOpen

  const handleOpenChange = React.useCallback(
    (next: boolean) => {
      if (!isControlled) setInternalOpen(next)
      onOpenChange?.(next)
    },
    [isControlled, onOpenChange]
  )

  const contextValue = React.useMemo(
    () => ({ open: currentOpen, onOpenChange: handleOpenChange }),
    [currentOpen, handleOpenChange]
  )

  return (
    <PopoverContext.Provider value={contextValue}>
      <div className="relative">{children}</div>
    </PopoverContext.Provider>
  )
}

interface PopoverTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
}

const PopoverTrigger = React.forwardRef<HTMLButtonElement, PopoverTriggerProps>(
  ({ asChild = false, className, children, onClick, ...props }, ref) => {
    const { open, onOpenChange } = usePopoverContext()
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        type="button"
        ref={ref}
        className={cn("cursor-pointer", className)}
        onClick={(e) => {
          onClick?.(e)
          if (!e.defaultPrevented) onOpenChange(!open)
        }}
        {...props}
      >
        {children}
      </Comp>
    )
  }
)
PopoverTrigger.displayName = "PopoverTrigger"

interface PopoverContentProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string
  align?: "start" | "center" | "end"
  side?: "top" | "right" | "bottom" | "left"
  sideOffset?: number
}

const PopoverContent = React.forwardRef<HTMLDivElement, PopoverContentProps>(
  ({ className, children, align = "center", side = "bottom", sideOffset = 4, ...props }, ref) => {
    const { open, onOpenChange } = usePopoverContext()

    if (!open) return null

    return (
      <div
        ref={ref}
        className={cn(
          "z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)
PopoverContent.displayName = "PopoverContent"

export { Popover, PopoverTrigger, PopoverContent }