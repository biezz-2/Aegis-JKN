'use client';

import React from 'react';
import { useAuthStore } from '@/hooks/use-auth';

interface PermissionGateProps {
  permission: 'read' | 'score' | 'audit' | 'export';
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function PermissionGate({
  permission,
  children,
  fallback = null
}: PermissionGateProps) {
  const hasPermission = useAuthStore((state) => {
    if (!state.user) return false;
    if (state.user.permissions.all) return true;
    return !!state.user.permissions[permission];
  });

  if (!hasPermission) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}

interface RoleGateProps {
  roles: ('Verifier' | 'Auditor' | 'Admin')[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function RoleGate({ roles, children, fallback = null }: RoleGateProps) {
  const userRole = useAuthStore((state) => state.user?.role);

  if (!userRole || !roles.includes(userRole)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}