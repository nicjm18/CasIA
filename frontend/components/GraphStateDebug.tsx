"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, Activity, Database, Filter, Star } from "lucide-react";
import type { RecommendationResponse } from "@/lib/types";

interface GraphStateDebugProps {
  response: RecommendationResponse;
}

export default function GraphStateDebug({ response }: GraphStateDebugProps) {
  const [open, setOpen] = useState(false);
  const summary = response.graph_state_summary;

  const pipeline = [
    { label: "Propiedades cargadas", value: summary.raw_properties, icon: <Database className="w-3.5 h-3.5" /> },
    { label: "Después de filtros", value: summary.filtered_properties, icon: <Filter className="w-3.5 h-3.5" /> },
    { label: "Propiedades puntuadas", value: summary.scored_properties, icon: <Star className="w-3.5 h-3.5" /> },
    { label: "Recomendadas", value: response.recommendations.length, icon: <Activity className="w-3.5 h-3.5" /> },
  ];

  return (
    <div className="rounded-xl border border-gray-200 bg-gray-50 overflow-hidden">
      <button
        className="w-full flex items-center justify-between px-4 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-100 transition-colors"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-blue-500" />
          Estado del grafo LangGraph
          <span className="text-xs font-normal text-gray-400">
            ({response.iterations_used} iter · {response.processing_time_ms.toFixed(0)}ms)
          </span>
        </div>
        {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </button>

      {open && (
        <div className="px-4 pb-4 space-y-4 border-t border-gray-200">
          {/* Pipeline funnel */}
          <div className="pt-3">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
              Pipeline de procesamiento
            </p>
            <div className="flex items-center gap-1 flex-wrap">
              {pipeline.map((stage, i) => (
                <div key={i} className="flex items-center gap-1">
                  <div className="flex items-center gap-1.5 bg-white border rounded-lg px-2 py-1 text-xs">
                    <span className="text-gray-400">{stage.icon}</span>
                    <span className="text-gray-500">{stage.label}:</span>
                    <span className="font-bold text-gray-800">{stage.value}</span>
                  </div>
                  {i < pipeline.length - 1 && (
                    <span className="text-gray-300 text-sm">→</span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Zones */}
          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
              Zonas seleccionadas ({summary.selected_zones.length})
            </p>
            <div className="flex flex-wrap gap-1">
              {summary.selected_zones.map((z) => (
                <span key={z} className="text-xs bg-blue-100 text-blue-700 rounded-full px-2 py-0.5">
                  {z.replace(/_/g, " ")}
                </span>
              ))}
            </div>
          </div>

          {/* Relaxation */}
          <div className="flex items-center gap-4 text-xs text-gray-600">
            <span>
              Nivel relajación: <strong>{summary.relaxation_level}</strong>
            </span>
            <span>
              Relajación aplicada: <strong>{response.relaxation_applied ? "Sí" : "No"}</strong>
            </span>
          </div>

          {/* Failure reasons */}
          {summary.failure_reasons.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-amber-600 uppercase tracking-wide mb-1">
                Diagnóstico de fallo
              </p>
              <ul className="space-y-1">
                {summary.failure_reasons.map((r, i) => (
                  <li key={i} className="text-xs text-amber-700 bg-amber-50 rounded px-2 py-1">
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
