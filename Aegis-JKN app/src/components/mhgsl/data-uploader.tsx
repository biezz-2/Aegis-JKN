"use client"

import React, { useState, useCallback, useRef } from "react"
import { Upload, FileText, AlertCircle, CheckCircle2, X, Loader2, Download } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

// --- Types ---
interface ValidationIssue {
  row: number
  column: string
  message: string
  severity: "error" | "warning"
}

interface UploadState {
  fileName: string | null
  fileSize: number | null
  status: "idle" | "validating" | "uploading" | "completed" | "error"
  progress: number
  errors: ValidationIssue[]
  previewData: any[]
}

const REQUIRED_COLUMNS = [
  "claim_id",
  "patient_id",
  "provider_id",
  "diagnosis_code",
  "amount",
  "timestamp",
]

// --- Helper: CSV Parser ---
function parseCSV(text: string): any[] {
  const lines = text.split(/\r?\n/).filter((line) => line.trim() !== "")
  if (lines.length === 0) return []

  const headers = lines[0].split(",").map((h) => h.trim())
  return lines.slice(1).map((line, index) => {
    const values = line.split(",")
    const obj: any = { _row: index + 2 }
    headers.forEach((h, i) => {
      obj[h] = values[i]?.trim()
    })
    return obj
  })
}

// --- Helper: JSON FHIR Parser ---
function parseFHIR(json: any): any[] {
  if (json.resourceType !== "Bundle") {
    throw new Error("Invalid FHIR Bundle: Missing resourceType 'Bundle'")
  }

  const entries = json.entry || []
  return entries.map((entry: any, index: number) => {
    const resource = entry.resource
    return {
      _row: index + 1,
      claim_id: resource.id,
      patient_id: resource.subject?.reference,
      provider_id: resource.provider?.reference,
      amount: resource.total?.value,
      timestamp: resource.created,
      // Map other FHIR fields as needed
    }
  })
}

export function DataUploader() {
  const [state, setState] = useState<UploadState>({
    fileName: null,
    fileSize: null,
    status: "idle",
    progress: 0,
    errors: [],
    previewData: [],
  })

  const fileInputRef = useRef<HTMLInputElement>(null)

  const validateData = (data: any[]) => {
    const issues: ValidationIssue[] = []
    const headers = data.length > 0 ? Object.keys(data[0]).filter(k => k !== '_row') : []

    // 1. Column Check
    const missingCols = REQUIRED_COLUMNS.filter(col => !headers.includes(col))
    if (missingCols.length > 0) {
      issues.push({
        row: 0,
        column: "all",
        message: `Missing required columns: ${missingCols.join(", ")}`,
        severity: "error",
      })
    }

    // 2. Row-level validation
    data.slice(0, 1000).forEach((row) => {
      if (!row.claim_id) {
        issues.push({ row: row._row, column: "claim_id", message: "Required field is empty", severity: "error" })
      }
      if (row.amount && isNaN(Number(row.amount))) {
        issues.push({ row: row._row, column: "amount", message: "Must be a number", severity: "error" })
      }
      // Pseudonymization check (example: must be UUID or specific hash format)
      if (row.patient_id && !/^u_[a-z0-9]{22}$/.test(row.patient_id) && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(row.patient_id)) {
        issues.push({ row: row._row, column: "patient_id", message: "Invalid pseudonymization format", severity: "warning" })
      }
    })

    return issues
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    processFile(file)
  }

  const processFile = async (file: File) => {
    setState((prev) => ({ ...prev, status: "validating", fileName: file.name, fileSize: file.size, errors: [], previewData: [] }))

    try {
      const text = await file.text()
      let data: any[] = []

      if (file.name.endsWith(".csv")) {
        data = parseCSV(text)
      } else if (file.name.endsWith(".json")) {
        data = parseFHIR(JSON.parse(text))
      } else {
        throw new Error("Unsupported file format. Please upload CSV or JSON FHIR Bundle.")
      }

      const validationErrors = validateData(data)
      setState((prev) => ({
        ...prev,
        status: validationErrors.some(e => e.severity === "error") ? "error" : "idle",
        errors: validationErrors,
        previewData: data.slice(0, 50),
      }))
    } catch (err: any) {
      setState((prev) => ({
        ...prev,
        status: "error",
        errors: [{ row: 0, column: "file", message: err.message, severity: "error" }],
      }))
    }
  }

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) processFile(file)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
  }, [])

  const simulateUpload = async () => {
    setState((prev) => ({ ...prev, status: "uploading", progress: 0 }))

    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200))
      setState((prev) => ({ ...prev, progress: i }))
    }

    setState((prev) => ({ ...prev, status: "completed" }))
  }

  const downloadErrorReport = () => {
    const report = state.errors.map(e => `${e.row},${e.column},${e.severity},${e.message}`).join("\\n")
    const blob = new Blob(["Row,Column,Severity,Message\n" + report], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.setAttribute("download", "upload_error_report.csv")
    a.click()
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Data Uploader</CardTitle>
          <CardDescription>
            Upload claim data in CSV or JSON FHIR Bundle format. All data is validated client-side before submission.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => fileInputRef.current?.click()}
            className={cn(
              "border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all",
              state.status === "uploading" ? "border-blue-400 bg-blue-50" : "border-gray-300 hover:border-blue-400 hover:bg-gray-50",
              "dark:border-gray-700 dark:hover:border-blue-500 dark:hover:bg-gray-900"
            )}
          >
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              accept=".csv,.json"
              onChange={handleFileSelect}
            />
            <div className="flex flex-col items-center gap-4">
              <div className="p-4 bg-blue-100 dark:bg-blue-900 rounded-full">
                <Upload className="w-8 h-8 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-lg font-medium">Drag and drop your file here, or click to browse</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Supported: .csv, .json (FHIR Bundle)</p>
              </div>
            </div>
          </div>

          {state.fileName && (
            <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg flex items-center justify-between">
              <div className="flex items-center gap-3">
                <FileText className="w-5 h-5 text-gray-500" />
                <div>
                  <p className="font-medium">{state.fileName}</p>
                  <p className="text-xs text-gray-500">{(state.fileSize! / 1024).toFixed(2)} KB</p>
                </div>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setState({ fileName: null, fileSize: null, status: "idle", progress: 0, errors: [], previewData: [] })}>
                <X className="w-4 h-4 mr-2" /> Remove
              </Button>
            </div>
          )}

          {state.status === "validating" && (
            <div className="mt-6 flex items-center gap-3 text-blue-600 dark:text-blue-400 animate-pulse">
              <Loader2 className="w-5 h-5 animate-spin" />
              <p>Validating schema and data types...</p>
            </div>
          )}

          {state.status === "uploading" && (
            <div className="mt-6 space-y-2">
              <div className="flex justify-between text-sm mb-1">
                <span>Uploading data...</span>
                <span>{state.progress}%</span>
              </div>
              <Progress value={state.progress} className="h-2" />
            </div>
          )}

          {state.status === "completed" && (
            <div className="mt-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg flex items-center gap-3 text-green-700 dark:text-green-400">
              <CheckCircle2 className="w-5 h-5" />
              <p className="font-medium">File uploaded and processed successfully!</p>
            </div>
          )}

          {state.errors.length > 0 && (
            <div className="mt-6 space-y-4">
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  Found {state.errors.length} validation issues. Please fix the errors before uploading.
                </AlertDescription>
              </Alert>

              <div className="flex justify-end">
                <Button variant="outline" size="sm" onClick={downloadErrorReport} disabled={state.status === "uploading"}>
                  <Download className="w-4 h-4 mr-2" /> Download Error Report
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {state.previewData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-xl font-semibold">Data Preview (First 50 rows)</CardTitle>
            <CardDescription>Highlighting errors for rapid verification.</CardDescription>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-[400px] w-full border rounded-md">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[80px]">Row</TableHead>
                    {REQUIRED_COLUMNS.map(col => (
                      <TableHead key={col}>{col}</TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {state.previewData.map((row, idx) => {
                    const rowErrors = state.errors.filter(e => e.row === row._row);
                    return (
                      <TableRow key={idx} className={cn(
                        rowErrors.length > 0 && "bg-red-50 dark:bg-red-900/10",
                        rowErrors.length === 0 && "hover:bg-gray-50 dark:hover:bg-gray-800"
                      )}>
                        <TableCell className="font-mono text-xs text-gray-500">{row._row}</TableCell>
                        {REQUIRED_COLUMNS.map(col => {
                          const cellError = rowErrors.find(e => e.column === col);
                          return (
                            <TableCell key={col} className={cn(
                              "max-w-[200px] truncate text-sm",
                              cellError && "text-red-600 dark:text-red-400 font-semibold"
                            )}>
                              {row[col]}
                            </TableCell>
                          )
                        })}
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </ScrollArea>
          </CardContent>
        </Card>
      )}

      {state.status !== "uploading" && state.status !== "completed" && state.fileName && (
        <div className="flex justify-center mt-8">
          <Button
            size="lg"
            className="px-12 py-6 text-lg font-bold"
            disabled={state.errors.some(e => e.severity === "error")}
            onClick={simulateUpload}
          >
            Submit Data
          </Button>
        </div>
      )}
    </div>
  )
}
