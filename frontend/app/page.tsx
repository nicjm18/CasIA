"use client";

import { useState, useCallback } from "react";
import { getRecommendations, getNeighborhoods } from "@/lib/api";
import type {
  RecommendationResponse,
  SearchStatus,
  Neighborhood,
} from "@/lib/types";
import SearchInterface from "@/components/SearchInterface";
import RecommendationCard from "@/components/RecommendationCard";
import RelaxationHistory from "@/components/RelaxationHistory";
import NeighborhoodInsights from "@/components/NeighborhoodInsights";
import GraphStateDebug from "@/components/GraphStateDebug";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Building2 } from "lucide-react";

// Stage progression to simulate step-by-step UX feedback
const STAGES: SearchStatus[] = [
  "parsing",
  "analyzing",
  "retrieving",
  "scoring",
  "evaluating",
];

export default function HomePage() {
  const [searchStatus, setSearchStatus] = useState<SearchStatus>("idle");
  const [response, setResponse] = useState<RecommendationResponse | null>(null);
  const [neighborhoods, setNeighborhoods] = useState<Neighborhood[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = useCallback(async (query: string) => {
    setSearchStatus("parsing");
    setResponse(null);
    setError(null);

    // Animate through stages while the real request runs
    let stageIdx = 0;
    const stageInterval = setInterval(() => {
      stageIdx++;
      if (stageIdx < STAGES.length) {
        setSearchStatus(STAGES[stageIdx]);
      } else {
        clearInterval(stageInterval);
      }
    }, 900);

    try {
      const [rec, nbhds] = await Promise.all([
        getRecommendations(query),
        getNeighborhoods(),
      ]);
      clearInterval(stageInterval);
      setResponse(rec);
      setNeighborhoods(nbhds);
      setSearchStatus("complete");
    } catch (err) {
      clearInterval(stageInterval);
      setError(err instanceof Error ? err.message : "Error desconocido");
      setSearchStatus("error");
    }
  }, []);

  const selectedZones = response?.graph_state_summary.selected_zones ?? [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Search section */}
      <section className="flex flex-col items-center">
        <SearchInterface onSearch={handleSearch} status={searchStatus} />
      </section>

      {/* Error state */}
      {error && (
        <div className="max-w-3xl mx-auto flex items-start gap-3 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-sm">Error en la búsqueda</p>
            <p className="text-sm mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Results section */}
      {response && searchStatus === "complete" && (
        <section className="space-y-6">
          {/* Summary bar */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                {response.recommendations.length > 0
                  ? `${response.recommendations.length} propiedades recomendadas`
                  : "No se encontraron propiedades"}
              </h2>
              <p className="text-sm text-gray-500 mt-0.5">
                De {response.total_found} propiedades analizadas ·{" "}
                {response.processing_time_ms.toFixed(0)}ms
                {response.relaxation_applied && (
                  <span className="ml-2 text-amber-600 font-medium">
                    · Criterios relajados ({response.relaxation_history.length}{" "}
                    ajustes)
                  </span>
                )}
              </p>
            </div>
          </div>

          {response.recommendations.length > 0 ? (
            <Tabs defaultValue="recommendations">
              <TabsList className="mb-4">
                <TabsTrigger value="recommendations">
                  Recomendaciones ({response.recommendations.length})
                </TabsTrigger>
                <TabsTrigger value="analysis">Análisis</TabsTrigger>
                <TabsTrigger value="graph">Estado del Grafo</TabsTrigger>
              </TabsList>

              {/* Tab: Recommendations */}
              <TabsContent value="recommendations">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  {response.recommendations.map((item) => (
                    <RecommendationCard
                      key={item.property.id}
                      item={item}
                      isTop={item.rank === 1}
                    />
                  ))}
                </div>
              </TabsContent>

              {/* Tab: Analysis */}
              <TabsContent value="analysis">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 mb-3">
                      Historial de decisiones
                    </h3>
                    <RelaxationHistory
                      steps={response.relaxation_history}
                      evaluatorFeedback={response.evaluator_feedback}
                      iterationsUsed={response.iterations_used}
                    />
                  </div>
                  <div>
                    <NeighborhoodInsights
                      neighborhoods={neighborhoods}
                      selectedZones={selectedZones}
                    />
                  </div>
                </div>
              </TabsContent>

              {/* Tab: Graph State */}
              <TabsContent value="graph">
                <GraphStateDebug response={response} />
              </TabsContent>
            </Tabs>
          ) : (
            <div className="text-center py-16 text-gray-400">
              <Building2 className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p className="text-lg font-medium">
                No encontramos propiedades con esos criterios
              </p>
              <p className="text-sm mt-1">
                Intenta ampliar el presupuesto o cambiar la zona
              </p>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
