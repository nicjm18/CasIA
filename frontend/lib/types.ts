// ── Property ──────────────────────────────────────────────────────────────

export interface Property {
  id: string;
  title: string;
  city: string;
  neighborhood: string;
  neighborhood_id: string;
  price: number;
  area_m2: number;
  bedrooms: number;
  bathrooms: number;
  parking_spots: number;
  property_type: string;
  stratum: number;
  distance_to_metro_km: number;
  description: string;
  amenities: string[];
  pet_friendly: boolean;
  zone_safety_score: number;
  investment_score: number;
  transport_score: number;
  latitude: number;
  longitude: number;
  available: boolean;
  listing_date: string;
  price_per_m2: number;
}

// ── Scores ────────────────────────────────────────────────────────────────

export interface ScoreBreakdown {
  final_score: number;
  budget_score: number;
  location_score: number;
  area_score: number;
  transport_score: number;
  investment_score: number;
  semantic_score: number;
}

// ── Recommendation ────────────────────────────────────────────────────────

export interface RecommendationItem {
  property: Property;
  scores: ScoreBreakdown;
  explanation: string;
  criteria_satisfaction_pct: number;
  rank: number;
}

// ── Relaxation history ────────────────────────────────────────────────────

export interface RelaxationStep {
  iteration: number;
  relaxation_level: number;
  action: string;
  changed_field: string;
  old_value: unknown;
  new_value: unknown;
  reason: string;
}

// ── API response ──────────────────────────────────────────────────────────

export interface RecommendationResponse {
  status: "success" | "partial" | "error";
  query: string;
  recommendations: RecommendationItem[];
  total_found: number;
  iterations_used: number;
  relaxation_applied: boolean;
  relaxation_history: RelaxationStep[];
  evaluator_feedback: string;
  processing_time_ms: number;
  graph_state_summary: {
    raw_properties: number;
    filtered_properties: number;
    scored_properties: number;
    selected_zones: string[];
    relaxation_level: number;
    failure_reasons: string[];
  };
}

// ── Neighbourhood ─────────────────────────────────────────────────────────

export interface Neighborhood {
  id: string;
  name: string;
  city: string;
  safety_score: number;
  transport_score: number;
  investment_score: number;
  average_price_m2: number;
  lifestyle_tags: string[];
  green_areas_score: number;
  latitude: number;
  longitude: number;
  description: string;
  metro_station: string;
  avg_stratum: number;
}

// ── Graph state ───────────────────────────────────────────────────────────

export interface GraphStateResponse {
  iteration_count: number;
  relaxation_level: number;
  is_solution_acceptable: boolean;
  selected_zones: string[];
  raw_properties_count: number;
  filtered_properties_count: number;
  scored_properties_count: number;
  failure_reasons: string[];
  decision_history: RelaxationStep[];
  evaluator_feedback: string;
  current_criteria: Record<string, unknown> | null;
}

// ── UI state ──────────────────────────────────────────────────────────────

export type SearchStatus =
  | "idle"
  | "parsing"
  | "analyzing"
  | "retrieving"
  | "scoring"
  | "evaluating"
  | "complete"
  | "error";

export interface SearchState {
  status: SearchStatus;
  query: string;
  response: RecommendationResponse | null;
  error: string | null;
}
