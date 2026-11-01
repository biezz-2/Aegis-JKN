"use client";

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/hooks/use-auth';

interface AuthContextType {
  isLoading: boolean;
  isAuthenticated: boolean;
  user: any | null;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { user, token, clearAuth, isAuthenticated: storeIsAuthenticated } = useAuthStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function validateSession() {
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await fetch('/api/auth/validate', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error('Session expired');
        }
      } catch (error) {
        clearAuth();
        router.push('/login');
      } finally {
        setIsLoading(false);
      }
    }

    validateSession();
  }, [token, router, clearAuth]);

  const logout = () => {
    clearAuth();
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{
      isLoading,
      isAuthenticated: storeIsAuthenticated(),
      user,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
