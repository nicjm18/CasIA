"use client";

import { useState, useRef, useEffect } from "react";
import { Search, Sparkles, ArrowRight, MapPin } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { SearchStatus } from "@/lib/types";

const EXAMPLE_QUERIES = [
  "Necesito un apartamento familiar en Medellín por menos de 450 millones, cerca al metro, zona segura y buen potencial de inversión.",
  "Busco una casa en Envigado o Sabaneta para vivir con mascotas, máximo 600 millones, 2 habitaciones.",
  "Quiero un apartaestudio moderno en El Poblado o Laureles para invertir, buena valorización, cerca de restaurantes.",
  "Necesito apartamento de 3 habitaciones en zona segura de Medellín, máximo 350 millones, que admita mascotas.",
];

interface SearchInterfaceProps {
  onSearch: (query: string) => void;
  status: SearchStatus;
}

const STAGE_LABELS: Record<SearchStatus, string> = {
  idle: "",
  parsing: "Analizando preferencias con IA...",
  analyzing: "Evaluando zonas y vecindarios...",
  retrieving: "Buscando propiedades candidatas...",
  scoring: "Calculando scores de compatibilidad...",
  evaluating: "Evaluando calidad de recomendaciones...",
  complete: "Recomendaciones listas",
  error: "Error en la búsqueda",
};

const STAGE_PROGRESS: Record<SearchStatus, number> = {
  idle: 0,
  parsing: 15,
  analyzing: 30,
  retrieving: 55,
  scoring: 70,
  evaluating: 85,
  complete: 100,
  error: 0,
};

export default function SearchInterface({ onSearch, status }: SearchInterfaceProps) {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isLoading = status !== "idle" && status !== "complete" && status !== "error";

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;
    onSearch(query.trim());
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
    textareaRef.current?.focus();
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [query]);

  const progress = STAGE_PROGRESS[status];

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      {/* Hero heading */}
      <div className="text-center space-y-2">
        <div className="flex items-center justify-center gap-2 text-blue-600 mb-3">
          <Sparkles className="w-5 h-5" />
          <span className="text-sm font-semibold uppercase tracking-widest">
            IA Inmobiliaria
          </span>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 leading-tight">
          Encuentra tu propiedad ideal
          <br />
          <span className="text-blue-600">en Medellín</span>
        </h1>
        <p className="text-gray-500 text-lg">
          Describe lo que buscas en lenguaje natural. Nuestro sistema IA analiza
          300+ propiedades y vecindarios para encontrar tu mejor opción.
        </p>
      </div>

      {/* Search form */}
      <form onSubmit={handleSubmit} className="relative">
        <div
          className={`rounded-2xl border-2 transition-all duration-200 bg-white shadow-sm ${
            focused
              ? "border-blue-500 shadow-blue-100 shadow-lg"
              : "border-gray-200 hover:border-gray-300"
          }`}
        >
          <div className="flex items-start gap-3 p-4">
            <Search className="w-5 h-5 text-gray-400 mt-1 flex-shrink-0" />
            <textarea
              ref={textareaRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              placeholder="Ej: Necesito un apartamento familiar en Medellín por menos de 450 millones, cerca al metro..."
              className="flex-1 resize-none bg-transparent outline-none text-gray-800 placeholder-gray-400 text-base min-h-[56px] leading-relaxed"
              rows={2}
              disabled={isLoading}
            />
          </div>

          {/* Progress bar when loading */}
          {isLoading && (
            <div className="px-4 pb-3">
              <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all duration-700 ease-out"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-xs text-blue-600 mt-1.5 font-medium">
                {STAGE_LABELS[status]}
              </p>
            </div>
          )}

          <div className="flex items-center justify-between px-4 pb-4">
            <div className="flex items-center gap-1.5 text-xs text-gray-400">
              <MapPin className="w-3.5 h-3.5" />
              <span>Medellín, Colombia</span>
              <span className="mx-1">•</span>
              <span>300+ propiedades</span>
            </div>
            <Button
              type="submit"
              disabled={!query.trim() || isLoading}
              size="sm"
              className="gap-2 rounded-xl"
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <span className="animate-spin h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full" />
                  Buscando...
                </span>
              ) : (
                <>
                  Buscar
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </Button>
          </div>
        </div>
      </form>

      {/* Example queries */}
      {status === "idle" && (
        <div className="space-y-3">
          <p className="text-xs text-center text-gray-400 font-medium uppercase tracking-wide">
            Ejemplos de búsqueda
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {EXAMPLE_QUERIES.map((example, i) => (
              <button
                key={i}
                onClick={() => handleExampleClick(example)}
                className="text-left text-sm text-gray-600 bg-gray-50 hover:bg-blue-50 hover:text-blue-700 border border-gray-200 hover:border-blue-200 rounded-xl p-3 transition-all duration-150 line-clamp-2"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
