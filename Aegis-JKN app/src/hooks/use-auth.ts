import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type UserRole = 'Verifier' | 'Auditor' | 'Admin';

export interface UserPermissions {
  read: boolean;
  score: boolean;
  audit: boolean;
  export: boolean;
  all: boolean;
}

interface AuthState {
  user: {
    id: string;
    username: string;
    role: UserRole;
    permissions: UserPermissions;
  } | null;
  token: string | null;
  setAuth: (user: any, token: string) => void;
  clearAuth: () => void;
  isAuthenticated: () => boolean;
}

const ROLE_PERMISSIONS: Record<UserRole, UserPermissions> = {
  Verifier: { read: true, score: true, audit: false, export: false, all: false },
  Auditor: { read: true, score: false, audit: true, export: true, all: false },
  Admin: { read: true, score: true, audit: true, export: true, all: true },
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      setAuth: (userData, token) => {
        const role = userData.role as UserRole;
        set({
          token,
          user: {
            ...userData,
            role,
            permissions: ROLE_PERMISSIONS[role] || ROLE_PERMISSIONS.Verifier,
          },
        });
      },
      clearAuth: () => set({ user: null, token: null }),
      isAuthenticated: () => !!get().token,
    }),
    {
      name: 'aegis-auth-storage',
    }
  )
);

export const checkPermission = (permission: keyof UserPermissions) => {
  const { user } = useAuthStore.getState();
  if (!user) return false;
  if (user.permissions.all) return true;
  return !!user.permissions[permission];
};
