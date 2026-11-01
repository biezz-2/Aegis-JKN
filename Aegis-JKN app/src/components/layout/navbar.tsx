"use client"

import { useTranslations } from "next-intl"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { LayoutDashboard, GitBranch, BarChart3, FileText, Settings, Menu, X, Shield, Brain } from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { cn } from "@/lib/utils"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const navigation = [
  { id: "dashboard", href: "/dashboard", icon: LayoutDashboard },
  { id: "graph", href: "/graph", icon: GitBranch },
  { id: "simulation", href: "/simulation", icon: Brain },
  { id: "audit", href: "/audit", icon: FileText },
  { id: "settings", href: "/settings", icon: Settings },
]

export function Navbar() {
  const t = useTranslations("nav")
  const pathname = usePathname()
  const router = useRouter()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const currentLocale = pathname.split('/')[1] || 'id'

  const handleLocaleChange = (newLocale: string) => {
    const pathWithoutLocale = pathname.replace(`/${currentLocale}`, '')
    const newPath = `/${newLocale}${pathWithoutLocale === '/' ? '' : pathWithoutLocale}`
    router.push(newPath)
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-40 h-16 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-full items-center justify-between px-4 md:px-6">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>

          <Link href={`/${currentLocale}/dashboard`} className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-primary" />
            <span className="font-bold text-xl hidden sm:block">Aegis-JKN</span>
          </Link>
        </div>

        <nav className="hidden md:flex md:items-center md:gap-1" aria-label="Main navigation">
          {navigation.map((item) => {
            const isActive = pathname.includes(item.href)
            return (
              <Link
                key={item.id}
                href={`/${currentLocale}${item.href}`}
                className={cn(
                  "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
                aria-current={isActive ? "page" : undefined}
              >
                <item.icon className="h-4 w-4" />
                {t(item.id)}
              </Link>
            )
          })}
        </nav>

        <div className="flex items-center gap-4">
          <Select onValueChange={handleLocaleChange} defaultValue={currentLocale}>
            <SelectTrigger className="w-[70px]">
              <SelectValue placeholder="Lang" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="id">🇮🇩 ID</SelectItem>
              <SelectItem value="en">🇺🇸 EN</SelectItem>
            </SelectContent>
          </Select>
          <ThemeToggle />
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden border-t bg-background">
          <nav className="p-4 space-y-2" aria-label="Mobile navigation">
            {navigation.map((item) => {
              const isActive = pathname.includes(item.href)
              return (
                <Link
                  key={item.id}
                  href={`/${currentLocale}${item.href}`}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2 text-base font-medium",
                    isActive
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  )}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <item.icon className="h-5 w-5" />
                  {t(item.id)}
                </Link>
              )
            })}
          </nav>
        </div>
      )}
    </header>
  )
}