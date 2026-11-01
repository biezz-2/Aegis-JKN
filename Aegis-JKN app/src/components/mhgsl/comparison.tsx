"use client"

import { useEffect, useState } from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  LineChart,
  Line,
  Dot,
} from "recharts"
import { Card, CardContent } from "@/components/ui/card"

interface MetricData {
  model: string
  auprc: number
  precision: number
  recall: number
  f1Score: number
}

interface SummaryData {
  headline: {
    accuracy: number
    overchargeTotal: number
    totalClaims: number
    detectedFraud: number
  }
  models: MetricData[]
  lastUpdated: string
}

const COLORS = {
  "Aegis-JKN": "#2a78d6",
  XGBoost: "#eb6834",
  GCN: "#1baf7a",
}

const METRIC_LABELS: Record<string, string> = {
  auprc: "AUPRC",
  precision: "Precision",
  recall: "Recall",
  f1Score: "F1-Score",
}

const METRIC_KEYS: Array<keyof MetricData> = ["auprc", "precision", "recall", "f1Score"]

export function ComparisonDashboard() {
  const [data, setData] = useState<SummaryData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const res = await fetch("/api/metrics/summary")
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }
        const json = await res.json()
        setData(json)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch metrics")
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
    const interval = setInterval(fetchMetrics, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="space-y-6" role="status" aria-label="Loading metrics">
        {[...Array(4)].map((_, i) => (
          <SkeletonTile key={i} />
        ))}
        <SkeletonChart height={300} />
        <SkeletonChart height={280} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600 dark:text-red-400" role="alert">
        <p>Failed to load metrics: {error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    )
  }

  if (!data) {
    return null
  }

  const chartData = data.models.map((m) => ({
    model: m.model,
    AUPRC: m.auprc,
    Precision: m.precision,
    Recall: m.recall,
    "F1-Score": m.f1Score,
  }))

  return (
    <div className="space-y-6" data-viz-root="comparison">
      <style>{`
        [data-viz-root="comparison"] {
          --surface-1: #fcfcfb;
          --text-primary: #0b0b0b;
          --text-secondary: #52514e;
          --series-1: #2a78d6;
          --series-2: #eb6834;
          --series-3: #1baf7a;
          --gridline: #e1e0d9;
          --baseline: #c3c2b7;
        }
        @media (prefers-color-scheme: dark) {
          :root:where(:not([data-theme="light"])) [data-viz-root="comparison"] {
            --surface-1: #1a1a19;
            --text-primary: #ffffff;
            --text-secondary: #c3c2b7;
            --series-1: #3987e5;
            --series-2: #d95926;
            --series-3: #199e70;
            --gridline: #2c2c2a;
            --baseline: #383835;
          }
        }
        :root[data-theme="dark"] [data-viz-root="comparison"] {
          --surface-1: #1a1a19;
          --text-primary: #ffffff;
          --text-secondary: #c3c2b7;
          --series-1: #3987e5;
          --series-2: #d95926;
          --series-3: #199e70;
          --gridline: #2c2c2a;
          --baseline: #383835;
        }
      `}</style>

      <section aria-labelledby="headline-title" className="space-y-4">
        <h2 id="headline-title" className="text-2xl font-semibold text-gray-900 dark:text-white">
          Headline Metrics
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatTile
            label="Accuracy"
            value={data.headline.accuracy}
            format="percent"
            trend={{ value: 2.3, direction: "up" }}
            ariaLabel={`Model accuracy ${(data.headline.accuracy * 100).toFixed(1)}%`}
          />
          <StatTile
            label="Overcharge Total"
            value={data.headline.overchargeTotal}
            format="currency"
            trend={{ value: -12.5, direction: "down" }}
            ariaLabel={`Total overcharge detected ${data.headline.overchargeTotal.toLocaleString("id-ID")} IDR`}
          />
          <StatTile
            label="Total Claims"
            value={data.headline.totalClaims}
            format="number"
            ariaLabel={`Total claims processed ${data.headline.totalClaims.toLocaleString("id-ID")}`}
          />
          <StatTile
            label="Detected Fraud"
            value={data.headline.detectedFraud}
            format="number"
            trend={{ value: 8.7, direction: "up" }}
            ariaLabel={`Fraud cases detected ${data.headline.detectedFraud.toLocaleString("id-ID")}`}
          />
        </div>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Last updated: {new Date(data.lastUpdated).toLocaleString("id-ID")}
        </p>
      </section>

      <section aria-labelledby="model-comparison-title" className="space-y-4">
        <h2 id="model-comparison-title" className="text-2xl font-semibold text-gray-900 dark:text-white">
          Model Comparison: Aegis-JKN vs Baselines
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="h-full">
            <CardContent className="h-full p-4">
              <h3 className="text-lg font-medium mb-4 text-gray-900 dark:text-white">
                Grouped Bar Comparison
              </h3>
              <div className="h-[300px] w-full" style={{ background: "var(--surface-1)" }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={chartData}
                    margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                  >
                    <CartesianGrid
                      stroke="var(--gridline)"
                      vertical={false}
                      strokeDasharray="3 3"
                    />
                    <XAxis
                      dataKey="model"
                      tick={{ fill: "var(--text-secondary)", fontSize: 12 }}
                      axisLine={{ stroke: "var(--baseline)" }}
                      tickLine={false}
                    />
                    <YAxis
                      tick={{ fill: "var(--text-secondary)", fontSize: 12 }}
                      axisLine={false}
                      tickLine={false}
                      domain={[0, "auto"]}
                      tickFormatter={(v) => (v * 100).toFixed(0) + "%"}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "var(--surface-1)",
                        border: "1px solid var(--baseline)",
                        borderRadius: 8,
                        color: "var(--text-primary)",
                      }}
                      labelStyle={{ color: "var(--text-secondary)" }}
                      formatter={(value: any) => [(Number(value ?? 0) * 100).toFixed(2) + "%", ""]}
                    />
                    <Legend
                      wrapperStyle={{ paddingTop: 20 }}
                      iconSize={12}
                      formatter={(value) => <span style={{ color: "var(--text-primary)" }}>{value}</span>}
                    />
                    {METRIC_KEYS.map((key, index) => (
                      <Bar
                        key={key}
                        dataKey={key.charAt(0).toUpperCase() + key.slice(1)}
                        name={METRIC_LABELS[key]}
                        fill={Object.values(COLORS)[index] as string}
                        radius={[4, 4, 0, 0]}
                        maxBarSize={40}
                      >
                        {chartData.map((_, i) => (
                          <Cell
                            key={`cell-${key}-${i}`}
                            fill={Object.values(COLORS)[i] as string}
                          />
                        ))}
                      </Bar>
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card className="h-full">
            <CardContent className="h-full p-4">
              <h3 className="text-lg font-medium mb-4 text-gray-900 dark:text-white">
                Radar / Multi-Metric View
              </h3>
              <div className="h-[300px] w-full" style={{ background: "var(--surface-1)" }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={chartData}
                    margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                  >
                    <CartesianGrid
                      stroke="var(--gridline)"
                      vertical={false}
                      strokeDasharray="3 3"
                    />
                    <XAxis
                      dataKey="model"
                      tick={{ fill: "var(--text-secondary)", fontSize: 12 }}
                      axisLine={{ stroke: "var(--baseline)" }}
                      tickLine={false}
                    />
                    <YAxis
                      tick={{ fill: "var(--text-secondary)", fontSize: 12 }}
                      axisLine={false}
                      tickLine={false}
                      domain={[0, "auto"]}
                      tickFormatter={(v) => (v * 100).toFixed(0) + "%"}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "var(--surface-1)",
                        border: "1px solid var(--baseline)",
                        borderRadius: 8,
                        color: "var(--text-primary)",
                      }}
                      labelStyle={{ color: "var(--text-secondary)" }}
                      formatter={(value: any) => [(Number(value ?? 0) * 100).toFixed(2) + "%", ""]}
                    />
                    <Legend
                      wrapperStyle={{ paddingTop: 20 }}
                      iconSize={12}
                      formatter={(value) => <span style={{ color: "var(--text-primary)" }}>{value}</span>}
                    />
                    {METRIC_KEYS.map((key, index) => (
                      <Line
                        key={key}
                        type="monotone"
                        dataKey={key.charAt(0).toUpperCase() + key.slice(1)}
                        name={METRIC_LABELS[key]}
                        stroke={Object.values(COLORS)[index] as string}
                        strokeWidth={2}
                        dot={{ r: 6, strokeWidth: 2 }}
                        activeDot={{ r: 8, strokeWidth: 2 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <section aria-labelledby="detail-table-title" className="space-y-4">
        <h2 id="detail-table-title" className="text-2xl font-semibold text-gray-900 dark:text-white">
          Detailed Metrics Table
        </h2>
        <div className="overflow-x-auto" style={{ background: "var(--surface-1)" }}>
          <table className="w-full text-left" role="table">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="p-3 font-medium text-gray-900 dark:text-white">Model</th>
                {METRIC_KEYS.map((key) => (
                  <th key={key} className="p-3 font-medium text-gray-900 dark:text-white">
                    {METRIC_LABELS[key]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.models.map((model, rowIndex) => (
                <tr
                  key={model.model}
                  className={`border-b border-gray-100 dark:border-gray-800 ${
                    rowIndex === 0 ? "bg-blue-50 dark:bg-blue-900/20" : ""
                  }`}
                >
                  <td className="p-3 font-medium text-gray-900 dark:text-white">
                    {model.model}
                    {rowIndex === 0 && (
                      <span className="ml-2 px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">
                        Primary
                      </span>
                    )}
                  </td>
                  {METRIC_KEYS.map((key) => {
                    const val = Number(model[key] ?? 0);
                    return (
                      <td key={key} className="p-3 text-gray-700 dark:text-gray-300 font-mono tabular-nums">
                        {(val * 100).toFixed(2)}%
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

interface StatTileProps {
  label: string
  value: number
  format: "percent" | "currency" | "number"
  trend?: { value: number; direction: "up" | "down" }
  ariaLabel: string
}

function StatTile({ label, value, format, trend, ariaLabel }: StatTileProps) {
  const formattedValue = useFormattedValue(value, format)

  return (
    <Card
      className="p-4 transition-shadow hover:shadow-md"
      style={{
        background: "var(--surface-1)",
        border: "1px solid var(--baseline)",
      }}
      aria-label={ariaLabel}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">{label}</p>
          <p className="mt-1 text-3xl font-bold text-gray-900 dark:text-white tabular-nums">
            {formattedValue}
          </p>
          {trend && (
            <div
              className={`mt-2 flex items-center gap-1 text-sm ${
                trend.direction === "up" ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
              }`}
            >
              <span aria-hidden="true">
                {trend.direction === "up" ? "▲" : "▼"}
              </span>
              <span>{Math.abs(trend.value).toFixed(1)}%</span>
              <span className="text-gray-500 dark:text-gray-400">vs last period</span>
            </div>
          )}
        </div>
        <div
          className="w-12 h-12 rounded-lg flex items-center justify-center"
          style={{
            background: "var(--series-1)",
            opacity: 0.15,
          }}
          aria-hidden="true"
        >
          <svg
            className="w-6 h-6"
            style={{ fill: "var(--series-1)" }}
            viewBox="0 0 24 24"
          >
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" />
          </svg>
        </div>
      </div>
    </Card>
  )
}

function useFormattedValue(value: number, format: "percent" | "currency" | "number"): string {
  switch (format) {
    case "percent":
      return `${(value * 100).toFixed(1)}%`
    case "currency":
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value)
    case "number":
      return new Intl.NumberFormat("id-ID").format(value)
    default:
      return String(value)
  }
}

function SkeletonTile() {
  return (
    <Card className="p-4 animate-pulse" style={{ background: "var(--surface-1)" }}>
      <div className="h-4 w-3/4 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
      <div className="h-8 w-1/2 bg-gray-200 dark:bg-gray-700 rounded" />
      <div className="mt-2 h-4 w-1/3 bg-gray-200 dark:bg-gray-700 rounded" />
    </Card>
  )
}

function SkeletonChart({ height }: { height: number }) {
  return (
    <Card className="animate-pulse" style={{ background: "var(--surface-1)" }}>
      <CardContent className="h-full p-4">
        <div className="h-6 w-1/3 bg-gray-200 dark:bg-gray-700 rounded mb-4" />
        <div className="h-full bg-gray-200 dark:bg-gray-700 rounded" style={{ height }} />
      </CardContent>
    </Card>
  )
}