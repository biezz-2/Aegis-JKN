import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { notFound } from "next/navigation"
import { getTranslations, getMessages } from "next-intl/server"
import { NextIntlClientProvider } from "next-intl"
import "../globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { AuthProvider } from "@/context/auth-context"

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })

const locales = ['en', 'id'] as const
type Locale = (typeof locales)[number]

interface RootLayoutProps {
  children: React.ReactNode
  params: Promise<{ locale: string }>
}

export async function generateMetadata({ params }: RootLayoutProps): Promise<Metadata> {
  const { locale } = await params
  const t = await getTranslations({ locale, namespace: 'common' })

  return {
    title: locale === 'id' ? "Aegis-JKN | Platform Intelijen Kecurangan" : "Aegis-JKN | Fraud Intelligence Platform",
    description: locale === 'id'
      ? "Multi-Channel Graph Segmentation Learning untuk Deteksi Fraud Klaim JKN"
      : "Multi-Channel Graph Segmentation Learning for JKN Claim Fraud Detection",
    keywords: ["fraud detection", "JKN", "healthcare", "graph neural networks", "machine learning"],
  }
}

export async function generateStaticParams() {
  return locales.map((locale) => ({ locale }))
}

export default async function RootLayout({
  children,
  params,
}: RootLayoutProps) {
  const { locale } = await params

  if (!locales.includes(locale as Locale)) {
    notFound()
  }

  const messages = await getMessages()

  return (
    <html lang={locale} suppressHydrationWarning dir="ltr">
      <body className={`${inter.variable} font-sans antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <NextIntlClientProvider messages={messages}>
            <AuthProvider>
              {children}
            </AuthProvider>
          </NextIntlClientProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}