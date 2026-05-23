import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Building2, Home, MapPin } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CasaIA — Recomendador Inteligente de Vivienda",
  description:
    "Encuentra tu propiedad ideal en Medellín con inteligencia artificial.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        {/* Top navigation */}
        <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-sm border-b border-gray-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-14">
              <Link
                href="/"
                className="flex items-center gap-2 text-blue-600 font-bold text-lg"
              >
                <Building2 className="w-5 h-5" />
                CasaIA
              </Link>
              <div className="flex items-center gap-1">
                <Link
                  href="/"
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <Home className="w-3.5 h-3.5" />
                  Inicio
                </Link>
                <Link
                  href="/neighborhoods"
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  <MapPin className="w-3.5 h-3.5" />
                  Vecindarios
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
          {children}
        </main>

        <footer className="border-t border-gray-100 py-6 mt-12">
          <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-400">
            CasaIA · Powered by LangGraph + GPT-4o-mini + OpenRouter ·
            Medellín, Colombia
          </div>
        </footer>
      </body>
    </html>
  );
}
