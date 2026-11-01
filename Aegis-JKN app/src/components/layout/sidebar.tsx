"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  GitBranch,
  BarChart3,
  FileText,
  Settings,
  Shield,
  Brain,
  ChevronLeft,
  ChevronRight,
  Users,
  AlertTriangle,
  Activity,
  Network,
} from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const mainNavigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Fraud Graph", href: "/graph", icon: GitBranch },
  { name: "Simulation", href: "/simulation", icon: Brain },
  { name: "Audit Trail", href: "/audit", icon: FileText },
  { name: "Settings", href: "/settings", icon: Settings },
]

const secondaryNavigation = [
  { name: "Providers", href: "/dashboard/providers", icon: Users },
  { name: "Alerts", href: "/dashboard/alerts", icon: AlertTriangle },
  { name: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { name: "Network Map", href: "/graph/network", icon: Network },
  { name: "Real-time", href: "/dashboard/realtime", icon: Activity },
]

export function Sidebar() {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={cn(
        "fixed left-0 top-16 z-30 h-[calc(100vh-4rem)] border-r bg-card transition-all duration-200",
        collapsed ? "w-16" : "w-64"
      )}
      aria-label="Sidebar navigation"
    >
      <div className="flex h-full flex-col">
        <nav className="flex-1 space-y-1 p-3" aria-label="Main navigation">
          {mainNavigation.map((item) => {
            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href))
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  collapsed ? "justify-center" : "",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
                aria-current={isActive ? "page" : undefined}
                title={collapsed ? item.name : undefined}
              >
                <item.icon className="h-5 w-5 flex-shrink-0" />
                {!collapsed && <span>{item.name}</span>}
              </Link>
            )
          })}
        </nav>

        {!collapsed && (
          <div className="border-t px-3 py-3">
            <h3 className="mb-2 px-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Shortcuts
            </h3>
            <nav className="space-y-1" aria-label="Shortcuts">
              {secondaryNavigation.map((item) => {
                const isActive = pathname === item.href || pathname.startsWith(item.href)
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                      isActive
                        ? "bg-primary/10 text-primary"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    )}
                    aria-current={isActive ? "page" : undefined}
                  >
                    <item.icon className="h-4 w-4" />
                    <span>{item.name}</span>
                  </Link>
                )
              })}
            </nav>
          </div>
        )}

        <div className="p-3">
          <Button
            variant="ghost"
            size="icon"
            className={cn("w-full justify-center", collapsed && "mx-auto")}
            onClick={() => setCollapsed(!collapsed)}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
          </Button>
        </div>
      </div>
    </aside>
  )
}