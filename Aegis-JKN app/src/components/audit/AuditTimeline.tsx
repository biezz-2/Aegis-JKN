'use client';

import React, { useMemo } from 'react';
import { Badge } from '@/components/ui/badge';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import {
  ScrollArea,
} from '@/components/ui/scroll-area';
import { CheckCircle2, XCircle, AlertCircle, Clock } from 'lucide-react';
import type { AuditLogEntry } from '@/types/audit';
import { EVENT_TYPE_LABELS, EVENT_TYPE_COLORS, DECISION_COLORS } from '@/types/audit';

interface TimelineEventProps {
  entry: AuditLogEntry;
  isVerified: boolean;
  isBrokenChain?: boolean;
}

function TimelineEvent({ entry, isVerified, isBrokenChain }: TimelineEventProps) {
  return (
    <div className="relative pl-8 pb-8 first:pt-0 last:pb-0">
      {/* Vertical Line */}
      <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-border" />

      {/* Indicator Dot */}
      <div
        className={`absolute left-0 top-1.5 w-6 h-6 rounded-full border-4 border-background z-10 flex items-center justify-center ${EVENT_TYPE_COLORS[entry.eventType]}`}
      />

      <Card className={`relative overflow-hidden transition-all hover:shadow-md ${isBrokenChain ? 'border-destructive ring-1 ring-destructive' : ''}`}>
        <CardContent className="p-4">
          <div className="flex flex-col gap-3">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="font-bold">{EVENT_TYPE_LABELS[entry.eventType]}</span>
                {entry.decision && (
                  <Badge className={`text-[10px] uppercase ${DECISION_COLORS[entry.decision]}`}>
                    {entry.decision}
                  </Badge>
                )}
              </div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Clock className="h-3 w-3" />
                {new Date(entry.timestamp).toLocaleString()}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground uppercase font-semibold">Claim ID</div>
                <div className="font-mono">{entry.claimId}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground uppercase font-semibold">User/Actor</div>
                <div>{entry.userId}</div>
              </div>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground uppercase font-semibold">Provider</div>
                <div>{entry.providerId}</div>
              </div>
            </div>

            <div className="p-3 bg-muted rounded-md font-mono text-xs overflow-x-auto">
              <div className="flex justify-between items-center mb-1">
                <span className="text-muted-foreground font-sans">Payload</span>
                <div className="flex items-center gap-1">
                   {isVerified ? (
                     <><CheckCircle2 className="h-3 w-3 text-green-500" /> <span className="text-green-500">Verified</span></>
                   ) : (
                     <><XCircle className="h-3 w-3 text-red-500" /> <span className="text-red-500">Invalid</span></>
                   )}
                </div>
              </div>
              <pre className="whitespace-pre-wrap">{JSON.stringify(entry.payload, null, 2)}</pre>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-border">
               <div className="flex flex-col gap-1">
                  <div className="text-[10px] text-muted-foreground uppercase">Current Hash</div>
                  <div className="font-mono text-[10px] opacity-60 truncate max-w-[200px]">
                    {entry.hash}
                  </div>
               </div>
               <div className="flex flex-col gap-1 text-right">
                  <div className="text-[10px] text-muted-foreground uppercase">Previous Hash</div>
                  <div className="font-mono text-[10px] opacity-60 truncate max-w-[200px]">
                    {entry.previousHash}
                  </div>
               </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export function AuditTimeline({ entries, isVerified }: { entries: AuditLogEntry[], isVerified: boolean }) {
  if (entries.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
        <AlertCircle className="h-10 w-10 mb-4 opacity-20" />
        <p>No audit events found matching the filters.</p>
      </div>
    );
  }

  return (
    <div className="relative max-w-4xl mx-auto py-4">
      {entries.map((entry, index) => (
        <TimelineEvent
          key={entry.id}
          entry={entry}
          isVerified={isVerified}
          isBrokenChain={index > 0 && entry.previousHash !== entries[index-1].hash}
        />
      ))}
    </div>
  );
}