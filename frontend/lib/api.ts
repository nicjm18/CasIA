import type {
  GraphStateResponse,
  Neighborhood,
  Property,
  RecommendationResponse,
} from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function getRecommendations(
  query: string
): Promise<RecommendationResponse> {
  return apiFetch<RecommendationResponse>("/recommendations", {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export async function getProperties(params?: {
  neighborhood_id?: string;
  property_type?: string;
  max_price?: number;
  min_price?: number;
  min_bedrooms?: number;
  pet_friendly?: boolean;
  limit?: number;
  offset?: number;
}): Promise<Property[]> {
  const qs = new URLSearchParams();
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined) qs.set(k, String(v));
    });
  }
  const query = qs.toString();
  return apiFetch<Property[]>(`/properties${query ? `?${query}` : ""}`);
}

export async function getNeighborhoods(): Promise<Neighborhood[]> {
  return apiFetch<Neighborhood[]>("/neighborhoods");
}

export async function getGraphState(): Promise<GraphStateResponse> {
  return apiFetch<GraphStateResponse>("/graph-state");
}

export function formatPrice(price: number): string {
  if (price >= 1_000_000_000) {
    return `$${(price / 1_000_000_000).toFixed(2)}B COP`;
  }
  if (price >= 1_000_000) {
    return `$${(price / 1_000_000).toFixed(0)}M COP`;
  }
  return `$${price.toLocaleString("es-CO")} COP`;
}

export function formatScore(score: number): string {
  return `${(score * 100).toFixed(0)}%`;
}

export function getScoreColor(score: number): string {
  if (score >= 0.85) return "text-emerald-600";
  if (score >= 0.70) return "text-blue-600";
  if (score >= 0.55) return "text-amber-600";
  return "text-red-500";
}

export function getScoreBg(score: number): string {
  if (score >= 0.85) return "bg-emerald-100 text-emerald-800";
  if (score >= 0.70) return "bg-blue-100 text-blue-800";
  if (score >= 0.55) return "bg-amber-100 text-amber-800";
  return "bg-red-100 text-red-800";
}
