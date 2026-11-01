declare module 'next' {
  export interface Metadata {
    title?: string | { default: string; template: string };
    description?: string;
    keywords?: string[];
    [key: string]: any;
  }
  export type ResolvingMetadata = Promise<Metadata>;
  export type ResolvingViewport = Promise<any>;
}

declare module 'next/types.js' {
  export type * from 'next';
  export type ResolvingMetadata = Promise<any>;
  export type ResolvingViewport = Promise<any>;
}

declare module 'next/types' {
  export type * from 'next';
  export type ResolvingMetadata = Promise<any>;
  export type ResolvingViewport = Promise<any>;
}

declare module 'next/link' {
  import type { ElementType } from 'react';
  const Link: ElementType<any>;
  export default Link;
}

declare module 'next/navigation' {
  export function useRouter(): {
    push(href: string, options?: any): void;
    replace(href: string, options?: any): void;
    refresh(): void;
    back(): void;
    forward(): void;
    prefetch(href: string): void;
  };
  export function usePathname(): string;
  export function useSearchParams(): URLSearchParams;
  export function useParams(): Record<string, string | string[]>;
  export function notFound(): never;
  export function redirect(url: string, type?: any): never;
}

declare module 'next/font/google' {
  export function Inter(options?: any): {
    className: string;
    style: { fontFamily: string };
    variable?: string;
  };
}

declare module '*.css' {
  const content: Record<string, string>;
  export default content;
}
