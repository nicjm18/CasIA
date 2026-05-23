"use client";

import { useEffect, useState } from "react";
import { getNeighborhoods } from "@/lib/api";
import type { Neighborhood } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { MapPin, Train, Shield, TrendingUp, TreePine, Building2 } from "lucide-react";

function ScoreBar({ value, label }: { value: number; label: string }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 85 ? "bg-emerald-500"
    : pct >= 70 ? "bg-blue-500"
    : pct >= 55 ? "bg-amber-500"
    : "bg-red-400";
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className="w-20 text-xs text-gray-500 flex-shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="w-8 text-right text-xs font-semibold text-gray-700">{pct}</span>
    </div>
  );
}

export default function NeighborhoodsPage() {
  const [neighborhoods, setNeighborhoods] = useState<Neighborhood[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState<keyof Neighborhood>("safety_score");

  useEffect(() => {
    getNeighborhoods()
      .then((data) => {
        setNeighborhoods(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const sorted = [...neighborhoods].sort(
    (a, b) => (b[sortBy] as number) - (a[sortBy] as number)
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Vecindarios de Medellín
          </h1>
          <p className="text-gray-500 mt-1">
            Análisis completo de {neighborhoods.length} zonas con scores de
            seguridad, transporte e inversión.
          </p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className="text-sm text-gray-500">Ordenar por:</span>
          <select
            className="text-sm border rounded-lg px-2 py-1.5 bg-white"
            value={String(sortBy)}
            onChange={(e) => setSortBy(e.target.value as keyof Neighborhood)}
          >
            <option value="safety_score">Seguridad</option>
            <option value="investment_score">Inversión</option>
            <option value="transport_score">Transporte</option>
            <option value="average_price_m2">Precio/m²</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-64 bg-gray-100 animate-pulse rounded-xl" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sorted.map((n) => (
            <Card key={n.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between">
                  <div>
                    <h2 className="font-bold text-gray-900">{n.name}</h2>
                    <div className="flex items-center gap-1 text-xs text-gray-500 mt-0.5">
                      <Train className="w-3 h-3" />
                      {n.metro_station}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-base font-bold text-gray-900">
                      ${(n.average_price_m2 / 1_000_000).toFixed(1)}M/m²
                    </div>
                    <div className="text-xs text-gray-400">
                      Estrato {n.avg_stratum.toFixed(1)}
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-xs text-gray-600 line-clamp-2">
                  {n.description}
                </p>
                <div className="space-y-1.5">
                  <ScoreBar value={n.safety_score} label="Seguridad" />
                  <ScoreBar value={n.transport_score} label="Transporte" />
                  <ScoreBar value={n.investment_score} label="Inversión" />
                  <ScoreBar value={n.green_areas_score} label="Verde" />
                </div>
                <div className="flex flex-wrap gap-1 pt-1">
                  {n.lifestyle_tags.slice(0, 4).map((tag) => (
                    <Badge key={tag} variant="outline" className="text-[10px] capitalize">
                      {tag.replace(/_/g, " ")}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
