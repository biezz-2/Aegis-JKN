"use client"

import { AppLayout } from "@/components/layout/app-layout"
import { Suspense } from "react"
import { DashboardContent } from "./dashboard-content"

export default function DashboardPage() {
  return (
    <AppLayout>
      <Suspense fallback={<DashboardSkeleton />}>
        <DashboardContent />
      </Suspense>
    </AppLayout>
  )
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-1/4 animate-pulse bg-muted rounded" />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-24 w-full animate-pulse bg-muted rounded-lg" />
        ))}
      </div>
      <div className="h-64 w-full animate-pulse bg-muted rounded-lg" />
    </div>
  )
}