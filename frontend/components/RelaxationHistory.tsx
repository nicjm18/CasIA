"use client";

import { AlertCircle, CheckCircle2, ChevronRight, TrendingUp, Map, Ruler, Train } from "lucide-react";
import type { RelaxationStep } from "@/lib/types";

interface RelaxationHistoryProps {
  steps: RelaxationStep[];
  evaluatorFeedback: string;
  iterationsUsed: number;
}

const ACTION_CONFIG: Record<string, { icon: React.ReactNode; color: string; label: string }> = {
  budget_relaxed:   { icon: <TrendingUp className="w-4 h-4" />, color: "text-amber-600 bg-amber-50 border-amber-200", label: "Presupuesto ampliado" },
  zone_expanded:    { icon: <Map className="w-4 h-4" />, color: "text-blue-600 bg-blue-50 border-blue-200", label: "Zonas expandidas" },
  area_relaxed:     { icon: <Ruler className="w-4 h-4" />, color: "text-purple-600 bg-purple-50 border-purple-200", label: "Área mínima reducida" },
  transport_relaxed:{ icon: <Train className="w-4 h-4" />, color: "text-green-600 bg-green-50 border-green-200", label: "Distancia metro ampliada" },
  no_change:        { icon: <CheckCircle2 className="w-4 h-4" />, color: "text-gray-600 bg-gray-50 border-gray-200", label: "Sin cambios" },
};

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return "N/A";
  if (typeof value === "number") {
    if (value > 1_000_000) return `$${(value / 1_000_000).toFixed(0)}M`;
    if (value < 10) return `${value.toFixed(2)} km`;
    return String(value);
  }
  if (Array.isArray(value)) return value.join(", ");
  return String(value);
}

export default function RelaxationHistory({
  steps,
  evaluatorFeedback,
  iterationsUsed,
}: RelaxationHistoryProps) {
  const hasRelaxation = steps.length > 0;

  return (
    <div className="space-y-4">
      {/* Evaluator feedback */}
      <div className="flex items-start gap-3 p-4 rounded-xl border border-gray-200 bg-gray-50">
        <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-semibold text-gray-800 mb-0.5">
            Evaluación del sistema
          </p>
          <p className="text-sm text-gray-600">{evaluatorFeedback}</p>
          <p className="text-xs text-gray-400 mt-1">
            Iteraciones utilizadas: {iterationsUsed}
          </p>
        </div>
      </div>

      {/* Relaxation steps */}
      {hasRelaxation ? (
        <div className="space-y-2">
          <h4 className="text-sm font-semibold text-gray-700">
            Historial de relajación de criterios
          </h4>
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-5 top-0 bottom-0 w-px bg-gray-200" />
            <div className="space-y-3">
              {steps.map((step, i) => {
                const config = ACTION_CONFIG[step.action] ?? ACTION_CONFIG.no_change;
                return (
                  <div key={i} className="relative pl-12">
                    {/* Timeline dot */}
                    <div
                      className={`absolute left-3 top-3 w-4 h-4 rounded-full flex items-center justify-center border ${config.color}`}
                    >
                      <div className="w-1.5 h-1.5 rounded-full bg-current" />
                    </div>
                    <div className={`rounded-xl border p-3 ${config.color}`}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {config.icon}
                          <span className="text-sm font-semibold">{config.label}</span>
                        </div>
                        <span className="text-xs opacity-60">Iteración {step.iteration}</span>
                      </div>
                      <p className="text-xs mt-1.5 opacity-80">{step.reason}</p>
                      {step.old_value !== null && step.new_value !== null && (
                        <div className="flex items-center gap-1.5 mt-1.5 text-xs font-mono opacity-70">
                          <span className="line-through">{formatValue(step.old_value)}</span>
                          <ChevronRight className="w-3 h-3" />
                          <span className="font-bold">{formatValue(step.new_value)}</span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      ) : (
        <div className="flex items-center gap-2 text-sm text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-xl p-3">
          <CheckCircle2 className="w-4 h-4" />
          Criterios originales satisfechos — no se requirió relajación
        </div>
      )}
    </div>
  );
}
