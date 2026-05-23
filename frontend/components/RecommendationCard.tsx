"use client";

import { useState } from "react";
import Link from "next/link";
import {
  MapPin, BedDouble, Bath, Car, Ruler, Train, Shield,
  TrendingUp, ChevronDown, ChevronUp, PawPrint, Star
} from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import ScoreVisualization from "./ScoreVisualization";
import { formatPrice, formatScore, getScoreBg } from "@/lib/api";
import type { RecommendationItem } from "@/lib/types";

interface RecommendationCardProps {
  item: RecommendationItem;
  isTop?: boolean;
}

const SCORE_ICON: Record<string, React.ReactNode> = {
  budget_score: null,
  location_score: <Shield className="w-3 h-3" />,
  transport_score: <Train className="w-3 h-3" />,
  investment_score: <TrendingUp className="w-3 h-3" />,
};

export default function RecommendationCard({ item, isTop = false }: RecommendationCardProps) {
  const [expanded, setExpanded] = useState(isTop);
  const { property: prop, scores, explanation, criteria_satisfaction_pct, rank } = item;

  const finalPct = Math.round(scores.final_score * 100);
  const satisfactionPct = Math.round(criteria_satisfaction_pct * 100);

  return (
    <Card
      className={`overflow-hidden transition-all duration-200 hover:shadow-md ${
        isTop ? "ring-2 ring-blue-500 shadow-blue-50 shadow-sm" : ""
      }`}
    >
      <CardHeader className="pb-3">
        {/* Rank + score badge */}
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <div
              className={`flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold ${
                rank === 1
                  ? "bg-yellow-400 text-yellow-900"
                  : rank === 2
                  ? "bg-gray-200 text-gray-700"
                  : rank === 3
                  ? "bg-amber-600/20 text-amber-700"
                  : "bg-gray-100 text-gray-500"
              }`}
            >
              {rank === 1 ? <Star className="w-3.5 h-3.5" /> : rank}
            </div>
            <Badge variant="outline" className="text-xs font-medium">
              {prop.property_type}
            </Badge>
            {prop.pet_friendly && (
              <Badge variant="secondary" className="text-xs gap-1">
                <PawPrint className="w-2.5 h-2.5" /> Mascotas OK
              </Badge>
            )}
            {isTop && (
              <Badge className="text-xs bg-blue-600">Mejor opción</Badge>
            )}
          </div>
          {/* Score circle */}
          <div className="flex flex-col items-center flex-shrink-0">
            <div
              className={`relative w-14 h-14 rounded-full flex items-center justify-center font-bold text-lg ${
                finalPct >= 85
                  ? "bg-emerald-100 text-emerald-700"
                  : finalPct >= 70
                  ? "bg-blue-100 text-blue-700"
                  : "bg-amber-100 text-amber-700"
              }`}
            >
              {finalPct}%
            </div>
            <span className="text-[10px] text-gray-400 mt-0.5">Match</span>
          </div>
        </div>

        {/* Title & location */}
        <div>
          <h3 className="font-semibold text-gray-900 text-base leading-snug">
            {prop.title}
          </h3>
          <div className="flex items-center gap-1.5 text-sm text-gray-500 mt-1">
            <MapPin className="w-3.5 h-3.5 flex-shrink-0" />
            <span>{prop.neighborhood}, {prop.city}</span>
            <span className="text-gray-300">·</span>
            <span>Estrato {prop.stratum}</span>
          </div>
        </div>

        {/* Price */}
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-gray-900">
            {formatPrice(prop.price)}
          </span>
          <span className="text-sm text-gray-400">
            ${(prop.price_per_m2 / 1_000_000).toFixed(1)}M/m²
          </span>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Quick stats grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {[
            { icon: <BedDouble className="w-4 h-4" />, label: `${prop.bedrooms} hab.` },
            { icon: <Bath className="w-4 h-4" />, label: `${prop.bathrooms} baños` },
            { icon: <Ruler className="w-4 h-4" />, label: `${prop.area_m2} m²` },
            { icon: <Car className="w-4 h-4" />, label: prop.parking_spots > 0 ? `${prop.parking_spots} parq.` : "Sin parq." },
          ].map((stat, i) => (
            <div
              key={i}
              className="flex items-center gap-1.5 bg-gray-50 rounded-lg px-2.5 py-1.5 text-sm text-gray-700"
            >
              <span className="text-gray-400">{stat.icon}</span>
              {stat.label}
            </div>
          ))}
        </div>

        {/* Score pills */}
        <div className="flex flex-wrap gap-1.5">
          {[
            { label: "Transporte", value: scores.transport_score },
            { label: "Seguridad", value: prop.zone_safety_score },
            { label: "Inversión", value: scores.investment_score },
          ].map((s) => (
            <span key={s.label} className={`text-xs px-2 py-0.5 rounded-full font-medium ${getScoreBg(s.value)}`}>
              {s.label}: {formatScore(s.value)}
            </span>
          ))}
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getScoreBg(criteria_satisfaction_pct)}`}>
            Criterios: {satisfactionPct}%
          </span>
        </div>

        {/* Explanation */}
        {explanation && (
          <div className="bg-blue-50 rounded-xl p-3 text-sm text-blue-900 leading-relaxed border border-blue-100">
            <span className="font-semibold text-blue-600 text-xs uppercase tracking-wide block mb-1">
              Por qué te recomendamos esta propiedad
            </span>
            {explanation}
          </div>
        )}

        {/* Expandable section */}
        <Button
          variant="ghost"
          size="sm"
          className="w-full text-xs text-gray-500 gap-1"
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? (
            <>
              <ChevronUp className="w-3 h-3" /> Ocultar detalles
            </>
          ) : (
            <>
              <ChevronDown className="w-3 h-3" /> Ver análisis de scores
            </>
          )}
        </Button>

        {expanded && (
          <div className="space-y-4 pt-2">
            <Separator />
            <div>
              <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Análisis de compatibilidad
              </h4>
              <ScoreVisualization scores={scores} compact />
            </div>

            {/* Metro distance */}
            <div className="flex items-center justify-between text-sm bg-gray-50 rounded-lg p-3">
              <div className="flex items-center gap-2 text-gray-600">
                <Train className="w-4 h-4" />
                <span>Distancia al metro</span>
              </div>
              <span className="font-semibold">{prop.distance_to_metro_km} km</span>
            </div>

            {/* Amenities */}
            {prop.amenities.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Amenidades ({prop.amenities.length})
                </p>
                <div className="flex flex-wrap gap-1">
                  {prop.amenities.slice(0, 8).map((a) => (
                    <Badge key={a} variant="outline" className="text-xs">
                      {a}
                    </Badge>
                  ))}
                  {prop.amenities.length > 8 && (
                    <Badge variant="outline" className="text-xs text-gray-400">
                      +{prop.amenities.length - 8} más
                    </Badge>
                  )}
                </div>
              </div>
            )}

            <Link href={`/property/${prop.id}`}>
              <Button className="w-full" size="sm">
                Ver detalles completos
              </Button>
            </Link>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
