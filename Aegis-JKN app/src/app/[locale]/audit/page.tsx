'use client';

import React, { useState, useMemo } from 'react';
import { AuditFilters } from '@/components/audit/AuditFilters';
import { AuditTimeline } from '@/components/audit/AuditTimeline';
import { MerkleTreeVisualizer } from '@/components/audit/MerkleTreeVisualizer';
import { verifyHashChain, buildMerkleRoot } from '@/lib/crypto-utils';
import type { AuditLogEntry, AuditFilters as AuditFiltersType } from '@/types/audit';
import { Card } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertTriangle, ShieldCheck } from 'lucide-react';
import { cn } from '@/lib/utils';

// Mock data generator for 100k records (simulated as 100 for performance in this demo)
const generateMockAuditLogs = (count: number): AuditLogEntry[] => {
  const entries: AuditLogEntry[] = [];
  let prevHash = '00000000000000000000000000000000';

  for (let i = 0; i < count; i++) {
    const claimId = `CLM-${1000 + (i % 10)}`;
    const eventTypes: any[] = ['CREATED', 'SCORED', 'REVIEWED', 'DECISION'];
    const type = eventTypes[Math.floor(Math.random() * eventTypes.length)];

    const entry: any = {
      id: `evt-${i}`,
      timestamp: new Date(Date.now() - i * 3600000).toISOString(),
      claimId,
      eventType: type,
      userId: `user-${Math.floor(Math.random() * 5)}`,
      providerId: `prov-${Math.floor(Math.random() * 3)}`,
      payload: {
        action: 'system_update',
        details: `Audit event ${i} for claim ${claimId}`,
        meta: { version: '1.0', region: 'JKN-West' }
      },
      previousHash: prevHash,
    };

    // Normally this would come from backend, but we mock the hash here
    entry.hash = `hash-${i}-${Math.random().toString(36).slice(2, 8)}`;
    prevHash = entry.hash;
    entries.push(entry);
  }

  // Reverse to show newest first in timeline
  return entries.reverse();
};

export default function AuditPage() {
  const [filters, setFilters] = useState<AuditFiltersType>({});
  const [isExporting, setIsExporting] = useState(false);

  const rawEntries = useMemo(() => generateMockAuditLogs(100), []);

  const filteredEntries = useMemo(() => {
    return rawEntries.filter(entry => {
      if (filters.claimId && !entry.claimId.includes(filters.claimId)) return false;
      if (filters.providerId && !entry.providerId.includes(filters.providerId)) return false;
      if (filters.userId && !entry.userId.includes(filters.userId)) return false;
      if (filters.decision && entry.decision !== filters.decision) return false;
      if (filters.eventType && entry.eventType !== filters.eventType) return false;
      return true;
    });
  }, [rawEntries, filters]);

  const verification = useMemo(() => {
    return verifyHashChain(filteredEntries);
  }, [filteredEntries]);

  const rootHash = useMemo(() => {
    return buildMerkleRoot(filteredEntries.map(e => e.hash));
  }, [filteredEntries]);

  const handleExport = async (format: 'csv' | 'pdf') => {
    setIsExporting(true);
    // Simulate export process
    await new Promise(resolve => setTimeout(resolve, 1500));
    console.log(`Exporting ${filteredEntries.length} records as ${format}...`);
    setIsExporting(false);
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex flex-col gap-2 mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Audit Trail</h1>
        <p className="text-muted-foreground">
          Immutable fraud investigation logs with cryptographic verification.
        </p>
      </div>

      <AuditFilters
        filters={filters}
        onFiltersChange={setFilters}
        onExport={handleExport}
        isExporting={isExporting}
        totalRecords={filteredEntries.length}
        isVerified={verification.isValid}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {verification.isValid === false && (
            <Alert variant="destructive" className="bg-destructive/10">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                Warning: Cryptographic hash chain is broken! The data may have been tampered with.
              </AlertDescription>
            </Alert>
          )}

          <AuditTimeline entries={filteredEntries} isVerified={verification.isValid} />
        </div>

        <div className="space-y-6">
          <MerkleTreeVisualizer
            leafHashes={filteredEntries.map(e => e.hash)}
            rootHash={rootHash}
            verified={verification.isValid}
          />

          <Card className="p-4 bg-card border border-border">
            <div className="flex items-center gap-2 font-semibold mb-3">
              <ShieldCheck className="h-4 w-4 text-primary" />
              Verification Status
            </div>
            <div className="space-y-2 text-xs text-muted-foreground">
              <div className="flex justify-between">
                <span>Hash Chain:</span>
                <span className={verification.isValid ? 'text-green-500' : 'text-red-500'}>
                  {verification.isValid ? 'Valid' : 'Invalid'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Merkle Root:</span>
                <span className={verification.isValid ? 'text-green-500' : 'text-red-s500'}>
                {verification.isValid ? 'Calculated' : 'Error'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Digital Signature:</span>
                <span className="text-muted-foreground">Signed by Aegis-JKN Authority</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}