"use client"

import React, { useState, useEffect, useMemo } from "react"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts"
import { Loader2, Play, RotateCcw, Info } from "lucide-react"

// --- Constants ---
const FRAUD_TYPES = [
  { id: "SYND-01", label: "Syndicate: Provider-Led" },
  { id: "SYND-02", label: "Syndicate: Patient-Led" },
  { id: "SYND-03", label: "Cross-Facility Collusion" },
  { id: "SYND-04", label: "Phantom Billing Ring" },
  { id: "SYND-05", label: "Upcoding Cluster" },
  { id: "SYND-06", label: "Referral Kickback Loop" },
  { id: "SYND-07", label: "Identity Theft Ring" },
  { id: "SYND-08", label: "Chronic Care Fraud" },
  { id: "SYND-09", label: "Drug Pharmacy Ring" },
]

// --- Mock API for Preview (Until real backend is ready) ---
const calculateProjections = (params: SimulationParams) => {
  const data = []
  const steps = 10
  const baseOvercharge = 1000000
  const baseDetection = 0.1

  for (let i = 0; i <= steps; i++) {
    const x = i / steps
    // Mock logic: overcharge increases with prevalence and network size
    const overcharge = baseOvercharge * (1 + x) * (params.prevalence / 5) * (params.networkSize / 100)
    // Mock logic: detection rate increases with noise reduction and prevalence
    const detection = Math.min(0.95, baseDetection + (x * 0.5) * (1 - params.noise / 100))

    data.push({
      step: `T${i}`,
      overcharge: Math.round(overcharge),
      detectionRate: detection,
    })
  }
  return data
}

interface SimulationParams {
  fraudType: string
  prevalence: number
  noise: number
  networkSize: number
}

export default function SimulationPage() {
  const [params, setParams] = useState<SimulationParams>({
    fraudType: "SYND-01",
    prevalence: 5,
    noise: 20,
    networkSize: 100,
  })

  const [status, setStatus] = useState<"idle" | "running" | "completed" | "error">("idle")
  const [results, setResults] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const projections = useMemo(() => calculateProjections(params), [params])

  const runSimulation = async () => {
    setStatus("running")
    setError(null)
    try {
      const res = await fetch("/api/simulation/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
      })

      if (!res.ok) throw new Error("Simulation failed to start")

      const { jobId } = await res.json()

      // Polling
      const poll = setInterval(async () => {
        const statusRes = await fetch(`/api/simulation/status/${jobId}`)
        const statusData = await statusRes.json()

        if (statusData.status === "completed") {
          setResults(statusData.result)
          setStatus("completed")
          clearInterval(poll)
        } else if (statusData.status === "failed") {
          setError("Simulation engine error")
          setStatus("error")
          clearInterval(poll)
        }
      }, 2000)

    } catch (err: any) {
      setError(err.message)
      setStatus("error")
    }
  }

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Fraud Simulation</h1>
          <p className="text-muted-foreground">What-if scenario builder for fraud intelligence testing.</p>
        </div>
        <Badge variant="outline" className="w-fit bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900 dark:text-yellow-200 dark:border-yellow-700">
          SIMULASI DATA SINTETIS
        </Badge>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Parameter Builder */}
        <Card className="lg:col-span-4">
          <CardHeader>
            <CardTitle>Scenario Parameters</CardTitle>
            <CardDescription>Configure the synthetic fraud environment.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="fraudType">Fraud Type</Label>
              <Select
                value={params.fraudType}
                onValueChange={(v) => setParams(p => ({ ...p, fraudType: v }))}
              >
                <SelectTrigger id="fraudType">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  {FRAUD_TYPES.map(t => (
                    <SelectItem key={t.id} value={t.id}>{t.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label htmlFor="prevalence">Prevalence (%)</Label>
                <span className="text-xs font-mono">{params.prevalence}%</span>
              </div>
              <Input
                id="prevalence"
                type="range"
                min="1" max="20" step="0.1"
                value={params.prevalence}
                onChange={(e) => setParams(p => ({ ...p, prevalence: parseFloat(e.target.value) }))}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label htmlFor="noise">Noise Level (%)</Label>
                <span className="text-xs font-mono">{params.noise}%</span>
              </div>
              <Input
                id="noise"
                type="range"
                min="0" max="100"
                value={params.noise}
                onChange={(e) => setParams(p => ({ ...p, noise: parseFloat(e.target.value) }))}
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <Label htmlFor="networkSize">Network Size (Nodes)</Label>
                <span className="text-xs font-mono">{params.networkSize}</span>
              </div>
              <Input
                id="networkSize"
                type="range"
                min="10" max="1000" step="10"
                value={params.networkSize}
                onChange={(e) => setParams(p => ({ ...p, networkSize: parseInt(e.target.value) }))}
              />
            </div>

            <div className="pt-4 space-y-3">
              <Button
                className="w-full"
                onClick={runSimulation}
                disabled={status === "running"}
              >
                {status === "running" ? (
                  <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Running...</>
                ) : (
                  <><Play className="mr-2 h-4 w-4" /> Run Full Simulation</>
                )}
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={() => setParams({ fraudType: "SYND-01", prevalence: 5, noise: 20, networkSize: 100 })}
                disabled={status === "running"}
              >
                <RotateCcw className="mr-2 h-4 w-4" /> Reset
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Real-time Preview */}
        <div className="lg:col-span-8 space-y-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Real-time Projection Preview</CardTitle>
                <CardDescription>Estimated impact based on current parameters.</CardDescription>
              </div>
              <Badge variant="secondary" className="text-blue-600 bg-blue-50 dark:bg-blue-900/30">
                Estimated
              </Badge>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={projections}>
                    <defs>
                      <linearGradient id="colorOvercharge" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#2a78d6" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#2a78d6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.5} />
                    <XAxis dataKey="step" />
                    <YAxis yAxisId="left" tickFormatter={(v) => `Rp${(v/1e6).toFixed(0)}M`} />
                    <YAxis yAxisId="right" orientation="right" tickFormatter={(v) => `${(v*100).toFixed(0)}%`} />
                    <Tooltip
                      formatter={(value: any, name: any) => {
                        const nameStr = String(name ?? "");
                        if (nameStr === "Overcharge") return [`Rp${value?.toLocaleString("id-ID")}`, nameStr];
                        return [`${(Number(value) * 100).toFixed(2)}%`, nameStr];
                      }}
                    />
                    <Legend />
                    <Area
                      yAxisId="left"
                      type="monotone"
                      dataKey="overcharge"
                      name="Overcharge"
                      stroke="#2a78d6"
                      fillOpacity={1}
                      fill="url(#colorOvercharge)"
                      strokeWidth={3}
                    />
                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="detectionRate"
                      name="Detection Rate"
                      stroke="#eb6834"
                      strokeWidth={3}
                      dot={{ r: 4 }}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Simulation Results */}
          {status !== "idle" && (
            <div className="space-y-6">
              {status === "error" && (
                <Alert variant="destructive">
                  <Info className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {status === "completed" && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Confusion Matrix</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 gap-0 border border-border text-center">
                        <div className="p-4 border-b border-r border-border bg-muted/30">
                          <span className="text-xs block text-muted-foreground">True Negative</span>
                          <span className="text-2xl font-bold">{(results?.tn || 0).toLocaleString()}</span>
                        </div>
                        <div className="p-4 border-b border-border bg-red-50 dark:bg-red-900/20">
                          <span className="text-xs block text-muted-foreground">False Positive</span>
                          <span className="text-2xl font-bold">{(results?.fp || 0).toLocaleString()}</span>
                        </div>
                        <div className="p-4 border-r border-border bg-red-50 dark:bg-red-900/20">
                          <span className="text-xs block text-muted-foreground">False Negative</span>
                          <span className="text-2xl font-bold">{(results?.fn || 0).toLocaleString()}</span>
                        </div>
                        <div className="p-4 bg-green-50 dark:bg-green-900/20">
                          <span className="text-xs block text-muted-foreground">True Positive</span>
                          <span className="text-2xl font-bold">{(results?.tp || 0).toLocaleString()}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Claim Flow (Sankey Concept)</CardTitle>
                    </CardHeader>
                    <CardContent className="flex items-center justify-center h-[200px] bg-muted/10 rounded-lg border-2 border-dashed">
                      <div className="text-center space-y-2">
                        <p className="text-sm text-muted-foreground">Sankey Diagram Visualization</p>
                        <p className="text-xs text-muted-foreground italic">
                          (Flow: Total Claims → Detected → Verified Fraud)
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
