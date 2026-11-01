import { Navbar } from "@/components/layout/navbar"
import { Sidebar } from "@/components/layout/sidebar"

export function AppLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="relative flex min-h-screen">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 bg-primary text-primary-foreground p-2 rounded shadow-lg"
      >
        Skip to main content
      </a>
      <Navbar />
      <Sidebar />
      <main id="main-content" className="flex-1 pl-0 pt-16 md:pl-64 transition-all duration-200">
        <div className="p-4 md:p-8">
          {children}
        </div>
      </main>
    </div>
  )
}