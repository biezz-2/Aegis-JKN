import { AppLayout } from "@/components/layout/app-layout"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default async function ClaimGraphPage({ params }: { params: Promise<{ locale: string; claimId: string }> }) {
  const { claimId } = await params

  return (
    <AppLayout>
      <div className="space-y-6">
        <header className="flex flex-col gap-2">
          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">Claim Graph</h1>
            <Badge variant="outline">Data demo: tidak ada</Badge>
          </div>
          <p className="text-muted-foreground">
            Multi-channel graph segmentation view for claim{" "}
            <span className="font-mono font-semibold text-foreground">{claimId}</span>.
          </p>
        </header>

        <div className="grid gap-6 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-xl">Graph analysis</CardTitle>
              <CardDescription>
                No analysis result has been computed for this claim yet.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex min-h-[280px] flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center">
                <p className="font-medium">Graph visualization will appear here</p>
                <p className="mt-2 max-w-md text-sm text-muted-foreground">
                  This page is a placeholder. It does not call an API and it does not render
                  synthetic fraud scores, so there is nothing to misread as a real result.
                  Topology, feature, and semantic channel attributions will be shown once a
                  scoring endpoint is available.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Claim details</CardTitle>
              <CardDescription>Read directly from the request URL.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="rounded-md border p-3">
                <div className="text-xs uppercase tracking-wide text-muted-foreground">Claim ID</div>
                <div className="mt-1 font-mono text-base">{claimId}</div>
              </div>
              <div className="rounded-md border p-3">
                <div className="text-xs uppercase tracking-wide text-muted-foreground">Analysis status</div>
                <div className="mt-1">Not computed</div>
              </div>
              <div className="rounded-md border p-3">
                <div className="text-xs uppercase tracking-wide text-muted-foreground">Data source</div>
                <div className="mt-1">URL parameter only</div>
              </div>
              <p className="text-xs text-muted-foreground">
                No demo or synthetic data is displayed on this page.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}