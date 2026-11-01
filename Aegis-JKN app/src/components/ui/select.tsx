"use client"

import * as React from "react"
import { cn } from "@/lib/utils"

interface SelectContextValue {
  value?: string
  onValueChange?: (value: string) => void
  open: boolean
  setOpen: (open: boolean) => void
  register: (value: string, label: React.ReactNode) => void
  labels: Map<string, React.ReactNode>
}

const SelectContext = React.createContext<SelectContextValue | null>(null)

function useSelectContext(component: string) {
  const ctx = React.useContext(SelectContext)
  if (!ctx) throw new Error(`${component} must be used within <Select>`)
  return ctx
}

interface SelectProps {
  value?: string
  defaultValue?: string
  onValueChange?: (value: string) => void
  children: React.ReactNode
  disabled?: boolean
}

const Select = ({ value, defaultValue, onValueChange, children, disabled }: SelectProps) => {
  const [internalValue, setInternalValue] = React.useState(defaultValue)
  const [open, setOpen] = React.useState(false)
  const labelsRef = React.useRef(new Map<string, React.ReactNode>())

  const isControlled = value !== undefined
  const currentValue = isControlled ? value : internalValue

  const register = React.useCallback((itemValue: string, label: React.ReactNode) => {
    labelsRef.current.set(itemValue, label)
  }, [])

  const handleValueChange = React.useCallback(
    (next: string) => {
      if (!isControlled) setInternalValue(next)
      onValueChange?.(next)
      setOpen(false)
    },
    [isControlled, onValueChange]
  )

  const contextValue = React.useMemo(
    () => ({
      value: currentValue,
      onValueChange: handleValueChange,
      open,
      setOpen,
      register,
      labels: labelsRef.current,
    }),
    [currentValue, handleValueChange, open, register]
  )

  return (
    <SelectContext.Provider value={contextValue}>
      <div className="relative" data-disabled={disabled ? "" : undefined}>
        {children}
      </div>
    </SelectContext.Provider>
  )
}

interface SelectTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  id?: string
}

const SelectTrigger = React.forwardRef<HTMLButtonElement, SelectTriggerProps>(
  ({ className, children, onClick, ...props }, ref) => {
    const { open, setOpen } = useSelectContext("SelectTrigger")
    return (
      <button
        type="button"
        ref={ref}
        role="combobox"
        aria-expanded={open}
        className={cn(
          "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        onClick={(event) => {
          onClick?.(event)
          if (!event.defaultPrevented) setOpen(!open)
        }}
        {...props}
      >
        {children}
        <span className="ml-2 shrink-0 opacity-50" aria-hidden="true">
          ▾
        </span>
      </button>
    )
  }
)
SelectTrigger.displayName = "SelectTrigger"

interface SelectValueProps {
  placeholder?: string
  className?: string
}

const SelectValue = ({ placeholder, className }: SelectValueProps) => {
  const { value, labels } = useSelectContext("SelectValue")
  const label = value !== undefined ? labels.get(value) : undefined
  return (
    <span className={cn("truncate", className)}>
      {value !== undefined ? (label ?? value) : (placeholder ?? "")}
    </span>
  )
}

interface SelectContentProps {
  children: React.ReactNode
  className?: string
  position?: string
}

const SelectContent = ({ children, className }: SelectContentProps) => {
  const { open } = useSelectContext("SelectContent")
  if (!open) return null
  return (
    <div
      className={cn(
        "absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border bg-popover p-1 text-popover-foreground shadow-md",
        className
      )}
    >
      {children}
    </div>
  )
}

interface SelectItemProps {
  value: string
  children: React.ReactNode
  className?: string
  disabled?: boolean
}

const SelectItem = ({ value, children, className, disabled }: SelectItemProps) => {
  const { onValueChange, value: selected } = useSelectContext("SelectItem")
  const { register } = useSelectContext("SelectItem")

  React.useEffect(() => {
    register(value, children)
  }, [register, value, children])

  return (
    <div
      role="option"
      aria-selected={selected === value}
      aria-disabled={disabled || undefined}
      className={cn(
        "relative flex w-full cursor-pointer select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none hover:bg-accent hover:text-accent-foreground data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50",
        selected === value && "bg-accent text-accent-foreground",
        className
      )}
      onClick={() => {
        if (!disabled) onValueChange?.(value)
      }}
    >
      {children}
    </div>
  )
}

const SelectGroup = ({ children }: { children: React.ReactNode }) => (
  <div role="group">{children}</div>
)

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem, SelectGroup }