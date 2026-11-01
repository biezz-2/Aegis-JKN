'use client';

import React, { useState, useCallback, useEffect } from 'react';
import { Calendar, Search, X, Filter, Download, ShieldCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { format } from 'date-fns';
import { z } from 'zod';

import type { AuditFilters, AuditDecision, AuditEventType } from '@/types/audit';

interface AuditFiltersProps {
  filters: AuditFilters;
  onFiltersChange: (filters: AuditFilters) => void;
  onExport: (format: 'csv' | 'pdf') => void;
  isExporting?: boolean;
  totalRecords: number;
  isVerified: boolean;
}

const FILTER_SCHEMA = z.object({
  claimId: z.string().optional(),
  providerId: z.string().optional(),
  userId: z.string().optional(),
  decision: z.enum(['APPROVED', 'DENIED', 'FLAGGED', 'PENDING']).optional(),
  eventType: z.enum(['CREATED', 'SCORED', 'REVIEWED', 'DECISION']).optional(),
});

export function AuditFilters({
  filters,
  onFiltersChange,
  onExport,
  isExporting,
  totalRecords,
  isVerified,
}: AuditFiltersProps) {
  const [dateFrom, setDateFrom] = useState<Date | undefined>(filters.dateRange?.from);
  const [dateTo, setDateTo] = useState<Date | undefined>(filters.dateRange?.to);
  const [isDatePopoverOpen, setIsDatePopoverOpen] = useState(false);
  const [claimId, setClaimId] = useState(filters.claimId || '');
  const [providerId, setProviderId] = useState(filters.providerId || '');
  const [userId, setUserId] = useState(filters.userId || '');
  const [decision, setDecision] = useState<AuditDecision | ''>(filters.decision || '');
  const [eventType, setEventType] = useState<AuditEventType | ''>(filters.eventType || '');

  useEffect(() => {
    const newFilters: AuditFilters = {
      dateRange: dateFrom && dateTo ? { from: dateFrom, to: dateTo } : undefined,
      claimId: claimId || undefined,
      providerId: providerId || undefined,
      userId: userId || undefined,
      decision: decision || undefined,
      eventType: eventType || undefined,
    };
    onFiltersChange(newFilters);
  }, [dateFrom, dateTo, claimId, providerId, userId, decision, eventType, onFiltersChange]);

  const handleClearFilters = useCallback(() => {
    setDateFrom(undefined);
    setDateTo(undefined);
    setClaimId('');
    setProviderId('');
    setUserId('');
    setDecision('');
    setEventType('');
  }, []);

  const hasActiveFilters = dateFrom || dateTo || claimId || providerId || userId || decision || eventType;

  return (
    <div className="flex flex-col gap-4 p-4 bg-card border border-border rounded-lg">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="text-lg font-semibold">Audit Trail Filters</h2>
          {hasActiveFilters && (
            <Badge variant="secondary" className="gap-1">
              <Filter className="h-3 w-3" />
              Active
              <Button
                variant="ghost"
                size="icon"
                className="h-4 w-4 p-0"
                onClick={handleClearFilters}
              >
                <X className="h-3 w-3" />
              </Button>
            </Badge>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Badge
            variant={isVerified ? 'default' : 'secondary'}
            className="gap-1"
          >
            <ShieldCheck className="h-3 w-3" />
            {isVerified ? 'Chain Verified' : 'Not Verified'}
          </Badge>
          <Badge variant="outline" className="ml-2">
            {totalRecords.toLocaleString()} records
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Popover open={isDatePopoverOpen} onOpenChange={setIsDatePopoverOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              className="w-full justify-start gap-2 h-10"
            >
              <Calendar className="h-4 w-4" />
              <span>
                {dateFrom && dateTo
                  ? `${format(dateFrom, 'MMM d, yyyy')} - ${format(dateTo, 'MMM d, yyyy')}`
                  : 'Date Range'}
              </span>
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-80 p-4" align="start">
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium mb-1 block">From</label>
                <Input
                  type="date"
                  value={dateFrom ? format(dateFrom, 'yyyy-MM-dd') : ''}
                  onChange={(e) => setDateFrom(e.target.value ? new Date(e.target.value) : undefined)}
                  className="w-full"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-1 block">To</label>
                <Input
                  type="date"
                  value={dateTo ? format(dateTo, 'yyyy-MM-dd') : ''}
                  onChange={(e) => setDateTo(e.target.value ? new Date(e.target.value) : undefined)}
                  className="w-full"
                />
              </div>
              <Button className="w-full" onClick={() => setIsDatePopoverOpen(false)}>
                Apply
              </Button>
            </div>
          </PopoverContent>
        </Popover>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Claim ID"
            value={claimId}
            onChange={(e) => setClaimId(e.target.value)}
            className="pl-10"
          />
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Provider ID"
            value={providerId}
            onChange={(e) => setProviderId(e.target.value)}
            className="pl-10"
          />
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="pl-10"
          />
        </div>

        <Select value={decision} onValueChange={(v: string) => setDecision(v as AuditDecision | "")}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Decision" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All Decisions</SelectItem>
            <SelectItem value="APPROVED">Approved</SelectItem>
            <SelectItem value="DENIED">Denied</SelectItem>
            <SelectItem value="FLAGGED">Flagged</SelectItem>
            <SelectItem value="PENDING">Pending</SelectItem>
          </SelectContent>
        </Select>

        <Select value={eventType} onValueChange={(v: string) => setEventType(v as AuditEventType | "")}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Event Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All Events</SelectItem>
            <SelectItem value="CREATED">Claim Created</SelectItem>
            <SelectItem value="SCORED">Risk Scored</SelectItem>
            <SelectItem value="REVIEWED">Manual Review</SelectItem>
            <SelectItem value="DECISION">Decision Made</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex flex-wrap items-center justify-end gap-2 pt-2 border-t">
        <Button
          variant="outline"
          onClick={() => onExport('csv')}
          disabled={isExporting}
          className="gap-2"
        >
          <Download className="h-4 w-4" />
          Export CSV
        </Button>
        <Button
          onClick={() => onExport('pdf')}
          disabled={isExporting}
          className="gap-2"
        >
          <Download className="h-4 w-4" />
          Export PDF
        </Button>
      </div>
    </div>
  );
}