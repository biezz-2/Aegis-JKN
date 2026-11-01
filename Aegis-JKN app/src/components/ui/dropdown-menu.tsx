"use client"

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"

import { cn } from "@/lib/utils"

/**
 * Lightweight dropdown menu primitive.
 *
 * The Radix dropdown-menu package is intentionally NOT used: it is not a
 * dependency of this project. This implementation keeps the same public API
 * subset the app relies on (DropdownMenu / DropdownMenuTrigger /
 * DropdownMenuContent / DropdownMenuItem / DropdownMenuSeparator) using plain
 * React state, a context for the open state, and a pointerdown listener for
 * click-outside dismissal.
 */

type DropdownMenuContextValue = {
  open: boolean
  setOpen: React.Dispatch<React.SetStateAction<boolean>>
  close: () => void
}

const DropdownMenuContext = React.createContext<DropdownMenuContextValue | null>(null)

function useDropdownMenu() {
  const context = React.useContext(DropdownMenuContext)
  if (!context) {
    throw new Error("DropdownMenu components must be rendered inside <DropdownMenu>.")
  }
  return context
}

type DropdownMenuProps = React.HTMLAttributes<HTMLDivElement>

function DropdownMenu({ className, children, ...props }: DropdownMenuProps) {
  const [open, setOpen] = React.useState(false)
  const rootRef = React.useRef<HTMLDivElement | null>(null)

  React.useEffect(() => {
    if (!open) return

    const handlePointerDown = (event: PointerEvent) => {
      const root = rootRef.current
      if (!root) return
      if (event.target instanceof Node && root.contains(event.target)) return
      setOpen(false)
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false)
      }
    }

    document.addEventListener("pointerdown", handlePointerDown)
    document.addEventListener("keydown", handleKeyDown)

    return () => {
      document.removeEventListener("pointerdown", handlePointerDown)
      document.removeEventListener("keydown", handleKeyDown)
    }
  }, [open])

  const contextValue = React.useMemo<DropdownMenuContextValue>(
    () => ({
      open,
      setOpen,
      close: () => setOpen(false),
    }),
    [open]
  )

  return (
    <DropdownMenuContext.Provider value={contextValue}>
      <div
        ref={rootRef}
        className={cn("relative inline-block text-left", className)}
        {...props}
      >
        {children}
      </div>
    </DropdownMenuContext.Provider>
  )
}
DropdownMenu.displayName = "DropdownMenu"

interface DropdownMenuTriggerProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean
}

const DropdownMenuTrigger = React.forwardRef<
  HTMLButtonElement,
  DropdownMenuTriggerProps
>(({ asChild = false, className, onClick, type, children, ...props }, ref) => {
  const { open, setOpen } = useDropdownMenu()
  const Comp = asChild ? Slot : "button"

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onClick?.(event)
    setOpen((previous) => !previous)
  }

  return (
    <Comp
      ref={ref}
      type={asChild ? undefined : type ?? "button"}
      aria-haspopup="menu"
      aria-expanded={open}
      data-state={open ? "open" : "closed"}
      className={cn(!asChild && "cursor-pointer", className)}
      onClick={handleClick}
      {...props}
    >
      {children}
    </Comp>
  )
})
DropdownMenuTrigger.displayName = "DropdownMenuTrigger"

type DropdownMenuContentProps = React.HTMLAttributes<HTMLDivElement> & {
  align?: "start" | "center" | "end"
  sideOffset?: number
}

const contentAlignment: Record<
  NonNullable<DropdownMenuContentProps["align"]>,
  string
> = {
  start: "left-0",
  center: "left-1/2 -translate-x-1/2",
  end: "right-0",
}

const DropdownMenuContent = React.forwardRef<
  HTMLDivElement,
  DropdownMenuContentProps
>(
  (
    { className, align = "center", sideOffset = 4, style, children, ...props },
    ref
  ) => {
    const { open } = useDropdownMenu()

    if (!open) return null

    return (
      <div
        ref={ref}
        role="menu"
        aria-orientation="vertical"
        data-state="open"
        style={{ marginTop: sideOffset, ...style }}
        className={cn(
          "absolute top-full z-50 min-w-[8rem] overflow-hidden rounded-md border border-border bg-popover p-1 text-popover-foreground shadow-md",
          contentAlignment[align],
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)
DropdownMenuContent.displayName = "DropdownMenuContent"

interface DropdownMenuItemProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  inset?: boolean
}

const DropdownMenuItem = React.forwardRef<
  HTMLButtonElement,
  DropdownMenuItemProps
>(({ className, inset = false, onClick, type, children, ...props }, ref) => {
  const { close } = useDropdownMenu()

  return (
    <button
      ref={ref}
      type={type ?? "button"}
      role="menuitem"
      className={cn(
        "relative flex w-full cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-left text-sm outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground disabled:pointer-events-none disabled:opacity-50",
        inset && "pl-8",
        className
      )}
      onClick={(event) => {
        onClick?.(event)
        close()
      }}
      {...props}
    >
      {children}
    </button>
  )
})
DropdownMenuItem.displayName = "DropdownMenuItem"

const DropdownMenuSeparator = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    role="separator"
    aria-orientation="horizontal"
    className={cn("-mx-1 my-1 h-px bg-border", className)}
    {...props}
  />
))
DropdownMenuSeparator.displayName = "DropdownMenuSeparator"

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
}
