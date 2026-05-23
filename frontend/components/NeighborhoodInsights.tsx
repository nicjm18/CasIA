"use client";

import { Shield, Train, TrendingUp, TreePine, Star } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { formatPrice } from "@/lib/api";
import type { Neighborhood } from "@/lib/types";

interface NeighborhoodInsightsProps {
  neighborhoods: Neighborhood[];
  selectedZones?: string[];
}

function ScorePill({ value, label }: { value: number; label: string }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 85 ? "bg-emerald-100 text-emerald-700"
    : pct >= 70 ? "bg-blue-100 text-blue-700"
    : "bg-amber-100 text-amber-700";
  return (
    <div className={`rounded-lg px-2 py-1 text-center ${color}`}>
      <div className="text-lg font-bold">{pct}</div>
      <div className="text-[10px] opacity-80">{label}</div>
    </div>
  );
}

export default function NeighborhoodInsights({
  neighborhoods,
  selectedZones = [],
}: NeighborhoodInsightsProps) {
  const relevant = selectedZones.length
    ? neighborhoods.filter((n) => selectedZones.includes(n.id))
    : neighborhoods.slice(0, 4);

  if (!relevant.length) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-gray-700">
        Vecindarios analizados
      </h3>
      <div className="grid gap-3">
        {relevant.map((n) => (
          <div
            key={n.id}
            className="rounded-xl border border-gray-200 bg-white p-4 space-y-3"
          >
            <div className="flex items-start justify-between gap-2">
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-semibold text-gray-900 text-sm">{n.name}</h4>
                  {selectedZones.includes(n.id) && (
                    <Badge className="text-[10px] py-0 h-4 bg-blue-600">Seleccionado</Badge>
                  )}
                </div>
                <p className="text-xs text-gray-500 mt-0.5">
                  Metro: {n.metro_station} · Estrato promedio: {n.avg_stratum.toFixed(1)}
                </p>
              </div>
              <div className="text-right flex-shrink-0">
                <div className="text-sm font-bold text-gray-900">
                  ${(n.average_price_m2 / 1_000_000).toFixed(1)}M/m²
                </div>
                <div className="text-[10px] text-gray-400">precio prom.</div>
              </div>
            </div>

            {/* Score grid */}
            <div className="grid grid-cols-4 gap-1.5">
              <ScorePill value={n.safety_score} label="Seguridad" />
              <ScorePill value={n.transport_score} label="Transporte" />
              <ScorePill value={n.investment_score} label="Inversión" />
              <ScorePill value={n.green_areas_score} label="Verde" />
            </div>

            {/* Tags */}
            {n.lifestyle_tags.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {n.lifestyle_tags.slice(0, 5).map((tag) => (
                  <Badge key={tag} variant="outline" className="text-[10px] capitalize">
                    {tag.replace("_", " ")}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
