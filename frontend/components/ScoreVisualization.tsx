"use client";

import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from "recharts";
import type { ScoreBreakdown } from "@/lib/types";
import { formatScore } from "@/lib/api";

interface ScoreVisualizationProps {
  scores: ScoreBreakdown;
  compact?: boolean;
}

const SCORE_LABELS: Record<keyof ScoreBreakdown, string> = {
  final_score: "Total",
  budget_score: "Presupuesto",
  location_score: "Ubicación",
  area_score: "Área",
  transport_score: "Transporte",
  investment_score: "Inversión",
  semantic_score: "Compatibilidad",
};

const SCORE_COLORS: Record<string, string> = {
  high: "#10b981",
  medium: "#3b82f6",
  low: "#f59e0b",
  very_low: "#ef4444",
};

function getBarColor(score: number): string {
  if (score >= 0.85) return SCORE_COLORS.high;
  if (score >= 0.70) return SCORE_COLORS.medium;
  if (score >= 0.55) return SCORE_COLORS.low;
  return SCORE_COLORS.very_low;
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const pct = Math.round(value * 100);
  const color = getBarColor(value);
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-gray-600">{label}</span>
        <span className="font-semibold" style={{ color }}>{pct}%</span>
      </div>
      <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

export default function ScoreVisualization({ scores, compact = false }: ScoreVisualizationProps) {
  const radarData = [
    { subject: "Presupuesto", value: Math.round(scores.budget_score * 100) },
    { subject: "Ubicación", value: Math.round(scores.location_score * 100) },
    { subject: "Área", value: Math.round(scores.area_score * 100) },
    { subject: "Transporte", value: Math.round(scores.transport_score * 100) },
    { subject: "Inversión", value: Math.round(scores.investment_score * 100) },
    { subject: "Semántico", value: Math.round(scores.semantic_score * 100) },
  ];

  if (compact) {
    return (
      <div className="space-y-2">
        <ScoreBar label="Presupuesto" value={scores.budget_score} />
        <ScoreBar label="Ubicación" value={scores.location_score} />
        <ScoreBar label="Área" value={scores.area_score} />
        <ScoreBar label="Transporte" value={scores.transport_score} />
        <ScoreBar label="Inversión" value={scores.investment_score} />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={radarData}>
            <PolarGrid stroke="#e5e7eb" />
            <PolarAngleAxis
              dataKey="subject"
              tick={{ fontSize: 11, fill: "#6b7280" }}
            />
            <Radar
              name="Score"
              dataKey="value"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.2}
              dot={{ fill: "#3b82f6", r: 3 }}
            />
            <Tooltip
              formatter={(v) => [`${v}%`, "Score"]}
              contentStyle={{ fontSize: 12, borderRadius: 8 }}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-2 gap-x-6 gap-y-2">
        <ScoreBar label="Presupuesto (30%)" value={scores.budget_score} />
        <ScoreBar label="Ubicación (20%)" value={scores.location_score} />
        <ScoreBar label="Área (15%)" value={scores.area_score} />
        <ScoreBar label="Transporte (15%)" value={scores.transport_score} />
        <ScoreBar label="Inversión (10%)" value={scores.investment_score} />
        <ScoreBar label="Compatibilidad (10%)" value={scores.semantic_score} />
      </div>
    </div>
  );
}
