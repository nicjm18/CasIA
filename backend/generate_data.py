"""Generate realistic mock datasets for the Medellin housing recommendation system."""
import json
import random
import math
import os
from typing import List, Dict, Any

random.seed(42)

# ──────────────────────────────────────────────
# NEIGHBORHOODS
# ──────────────────────────────────────────────
NEIGHBORHOODS: List[Dict[str, Any]] = [
    {
        "id": "el_poblado",
        "name": "El Poblado",
        "city": "Medellín",
        "safety_score": 0.93,
        "transport_score": 0.85,
        "investment_score": 0.91,
        "average_price_m2": 8_800_000,
        "lifestyle_tags": ["upscale", "nightlife", "restaurants", "expats", "luxury", "shopping", "parks"],
        "green_areas_score": 0.78,
        "latitude": 6.2108,
        "longitude": -75.5687,
        "description": "El Poblado is Medellín's most prestigious neighborhood, famous for its vibrant nightlife, gourmet restaurants, and large expatriate community. It offers the highest safety and quality of life scores in the city.",
        "metro_station": "El Poblado",
        "distance_to_centro_km": 4.5,
        "avg_stratum": 5.8,
        "popular_for": ["families", "expats", "young_professionals", "investors"],
        "new_construction_rate": 0.85,
    },
    {
        "id": "laureles",
        "name": "Laureles",
        "city": "Medellín",
        "safety_score": 0.88,
        "transport_score": 0.82,
        "investment_score": 0.83,
        "average_price_m2": 6_500_000,
        "lifestyle_tags": ["residential", "family", "quiet", "upscale", "sports", "shopping"],
        "green_areas_score": 0.72,
        "latitude": 6.2439,
        "longitude": -75.5897,
        "description": "Laureles is a well-established residential neighborhood known for its wide tree-lined streets, sports facilities, and family-friendly atmosphere. It offers excellent connectivity via Metro Line B.",
        "metro_station": "Estadio",
        "distance_to_centro_km": 3.2,
        "avg_stratum": 4.9,
        "popular_for": ["families", "professionals", "retirees"],
        "new_construction_rate": 0.55,
    },
    {
        "id": "envigado",
        "name": "Envigado",
        "city": "Medellín",
        "safety_score": 0.89,
        "transport_score": 0.80,
        "investment_score": 0.86,
        "average_price_m2": 5_800_000,
        "lifestyle_tags": ["family", "quiet", "suburban", "parks", "schools", "community"],
        "green_areas_score": 0.82,
        "latitude": 6.1716,
        "longitude": -75.5900,
        "description": "Envigado is a peaceful municipality adjacent to Medellín, renowned for its family-friendly environment, excellent schools, abundant green spaces, and strong sense of community. Offers great investment potential.",
        "metro_station": "Envigado",
        "distance_to_centro_km": 7.8,
        "avg_stratum": 4.5,
        "popular_for": ["families", "retirees", "long_term_investors"],
        "new_construction_rate": 0.70,
    },
    {
        "id": "sabaneta",
        "name": "Sabaneta",
        "city": "Medellín",
        "safety_score": 0.87,
        "transport_score": 0.77,
        "investment_score": 0.88,
        "average_price_m2": 5_200_000,
        "lifestyle_tags": ["family", "growing", "commercial", "parks", "community", "modern"],
        "green_areas_score": 0.76,
        "latitude": 6.1486,
        "longitude": -75.6165,
        "description": "Sabaneta is the fastest-growing municipality in the Aburrá Valley, offering modern infrastructure, excellent commercial zones, and outstanding investment potential. Known for its vibrant commercial center.",
        "metro_station": "Sabaneta",
        "distance_to_centro_km": 10.5,
        "avg_stratum": 4.2,
        "popular_for": ["families", "investors", "young_professionals"],
        "new_construction_rate": 0.90,
    },
    {
        "id": "bello",
        "name": "Bello",
        "city": "Medellín",
        "safety_score": 0.71,
        "transport_score": 0.78,
        "investment_score": 0.70,
        "average_price_m2": 3_100_000,
        "lifestyle_tags": ["working_class", "affordable", "industrial", "community", "large"],
        "green_areas_score": 0.54,
        "latitude": 6.3358,
        "longitude": -75.5589,
        "description": "Bello is a large northern municipality with excellent Metro connectivity. It offers affordable housing options and is undergoing significant urban renewal. Popular among working-class families seeking metro access.",
        "metro_station": "Bello",
        "distance_to_centro_km": 8.2,
        "avg_stratum": 2.5,
        "popular_for": ["working_class", "budget_buyers"],
        "new_construction_rate": 0.40,
    },
    {
        "id": "itagui",
        "name": "Itagüí",
        "city": "Medellín",
        "safety_score": 0.73,
        "transport_score": 0.75,
        "investment_score": 0.73,
        "average_price_m2": 3_400_000,
        "lifestyle_tags": ["industrial", "affordable", "commercial", "working_class"],
        "green_areas_score": 0.48,
        "latitude": 6.1849,
        "longitude": -75.5994,
        "description": "Itagüí is an industrial municipality south of Medellín with affordable housing and good commercial infrastructure. It connects to Medellín via Metro Line A and offers budget-friendly options.",
        "metro_station": "Itagüí",
        "distance_to_centro_km": 6.5,
        "avg_stratum": 2.8,
        "popular_for": ["budget_buyers", "workers"],
        "new_construction_rate": 0.35,
    },
    {
        "id": "robledo",
        "name": "Robledo",
        "city": "Medellín",
        "safety_score": 0.74,
        "transport_score": 0.70,
        "investment_score": 0.68,
        "average_price_m2": 3_600_000,
        "lifestyle_tags": ["middle_class", "residential", "hilly", "community", "traditional"],
        "green_areas_score": 0.65,
        "latitude": 6.2825,
        "longitude": -75.5893,
        "description": "Robledo is a traditional middle-class neighborhood in western Medellín, known for its hilly terrain, strong community ties, and affordable residential options. Connected via Metro Cable.",
        "metro_station": "Universidad",
        "distance_to_centro_km": 3.8,
        "avg_stratum": 3.1,
        "popular_for": ["families", "students", "middle_class"],
        "new_construction_rate": 0.30,
    },
    {
        "id": "belen",
        "name": "Belén",
        "city": "Medellín",
        "safety_score": 0.79,
        "transport_score": 0.73,
        "investment_score": 0.75,
        "average_price_m2": 4_200_000,
        "lifestyle_tags": ["residential", "family", "parks", "shopping", "middle_class"],
        "green_areas_score": 0.68,
        "latitude": 6.2268,
        "longitude": -75.6041,
        "description": "Belén is a large western residential sector of Medellín, popular for its parks, shopping centers, and family-friendly environment. It offers good connectivity to the city center.",
        "metro_station": "Aguacatala",
        "distance_to_centro_km": 4.0,
        "avg_stratum": 3.8,
        "popular_for": ["families", "middle_class"],
        "new_construction_rate": 0.50,
    },
    {
        "id": "castilla",
        "name": "Castilla",
        "city": "Medellín",
        "safety_score": 0.69,
        "transport_score": 0.76,
        "investment_score": 0.65,
        "average_price_m2": 2_900_000,
        "lifestyle_tags": ["working_class", "affordable", "industrial", "northern"],
        "green_areas_score": 0.50,
        "latitude": 6.2983,
        "longitude": -75.5632,
        "description": "Castilla is a northern working-class neighborhood with excellent Metro access and affordable housing. It's undergoing urban improvement initiatives that are gradually raising property values.",
        "metro_station": "Acevedo",
        "distance_to_centro_km": 5.5,
        "avg_stratum": 2.3,
        "popular_for": ["budget_buyers", "workers"],
        "new_construction_rate": 0.25,
    },
    {
        "id": "floresta",
        "name": "La Floresta",
        "city": "Medellín",
        "safety_score": 0.81,
        "transport_score": 0.78,
        "investment_score": 0.79,
        "average_price_m2": 4_800_000,
        "lifestyle_tags": ["upscale", "residential", "quiet", "family", "modern"],
        "green_areas_score": 0.70,
        "latitude": 6.2510,
        "longitude": -75.5920,
        "description": "La Floresta is an upscale residential neighborhood in western Medellín, known for its modern constructions, quiet streets, and proximity to Laureles. Excellent for families seeking a premium but more affordable alternative to El Poblado.",
        "metro_station": "Floresta",
        "distance_to_centro_km": 3.0,
        "avg_stratum": 4.4,
        "popular_for": ["families", "professionals", "investors"],
        "new_construction_rate": 0.60,
    },
    {
        "id": "la_america",
        "name": "La América",
        "city": "Medellín",
        "safety_score": 0.76,
        "transport_score": 0.80,
        "investment_score": 0.72,
        "average_price_m2": 3_900_000,
        "lifestyle_tags": ["residential", "central", "commercial", "middle_class", "accessible"],
        "green_areas_score": 0.58,
        "latitude": 6.2449,
        "longitude": -75.5821,
        "description": "La América is a centrally located residential neighborhood with excellent transport connections. It offers a balanced lifestyle with access to commercial areas and parks at mid-range prices.",
        "metro_station": "La América",
        "distance_to_centro_km": 2.5,
        "avg_stratum": 3.5,
        "popular_for": ["professionals", "middle_class", "renters"],
        "new_construction_rate": 0.42,
    },
    {
        "id": "buenos_aires",
        "name": "Buenos Aires",
        "city": "Medellín",
        "safety_score": 0.72,
        "transport_score": 0.74,
        "investment_score": 0.69,
        "average_price_m2": 3_300_000,
        "lifestyle_tags": ["historic", "central", "traditional", "community", "hills"],
        "green_areas_score": 0.61,
        "latitude": 6.2333,
        "longitude": -75.5570,
        "description": "Buenos Aires is a traditional hillside neighborhood east of the city center, offering historic charm and stunning views of Medellín. It's connected via Metro Cable and is undergoing gentrification.",
        "metro_station": "San Antonio (cable)",
        "distance_to_centro_km": 2.2,
        "avg_stratum": 3.0,
        "popular_for": ["artists", "young_professionals", "budget_buyers"],
        "new_construction_rate": 0.35,
    },
    {
        "id": "manrique",
        "name": "Manrique",
        "city": "Medellín",
        "safety_score": 0.66,
        "transport_score": 0.72,
        "investment_score": 0.62,
        "average_price_m2": 2_600_000,
        "lifestyle_tags": ["working_class", "traditional", "community", "affordable", "eastern"],
        "green_areas_score": 0.55,
        "latitude": 6.2642,
        "longitude": -75.5536,
        "description": "Manrique is a large northeastern neighborhood with a strong working-class community. While safety scores are moderate, it offers very affordable housing and is served by Metro and Cable Car systems.",
        "metro_station": "Acevedo / Cable",
        "distance_to_centro_km": 4.8,
        "avg_stratum": 2.2,
        "popular_for": ["budget_buyers", "renters"],
        "new_construction_rate": 0.20,
    },
    {
        "id": "san_antonio_prado",
        "name": "San Antonio de Prado",
        "city": "Medellín",
        "safety_score": 0.80,
        "transport_score": 0.62,
        "investment_score": 0.77,
        "average_price_m2": 3_700_000,
        "lifestyle_tags": ["suburban", "family", "quiet", "nature", "affordable", "growing"],
        "green_areas_score": 0.88,
        "latitude": 6.1472,
        "longitude": -75.6502,
        "description": "San Antonio de Prado is a suburban community southwest of Medellín, offering a peaceful semi-rural environment with excellent green spaces. Popular for families seeking tranquility with growing investment potential.",
        "metro_station": "None (bus connection)",
        "distance_to_centro_km": 12.0,
        "avg_stratum": 3.2,
        "popular_for": ["families", "retirees", "nature_lovers"],
        "new_construction_rate": 0.65,
    },
    {
        "id": "el_estadio",
        "name": "El Estadio",
        "city": "Medellín",
        "safety_score": 0.82,
        "transport_score": 0.86,
        "investment_score": 0.80,
        "average_price_m2": 5_400_000,
        "lifestyle_tags": ["sports", "nightlife", "restaurants", "metro", "young", "vibrant"],
        "green_areas_score": 0.65,
        "latitude": 6.2528,
        "longitude": -75.5820,
        "description": "El Estadio sector, surrounding the Atanasio Girardot Sports Complex, is a vibrant neighborhood with excellent Metro Line B connectivity. Popular among young professionals for its nightlife, restaurants, and sports culture.",
        "metro_station": "Estadio",
        "distance_to_centro_km": 2.8,
        "avg_stratum": 4.2,
        "popular_for": ["young_professionals", "sports_fans", "students"],
        "new_construction_rate": 0.68,
    },
]

# ──────────────────────────────────────────────
# URBAN SIGNALS
# ──────────────────────────────────────────────
URBAN_SIGNALS: List[Dict[str, Any]] = [
    {
        "id": "us_001",
        "zone": "El Poblado",
        "neighborhood_id": "el_poblado",
        "signal_type": "infrastructure",
        "urban_growth_score": 0.85,
        "impact": "positive",
        "title": "Parques del Río Expansion Phase 3",
        "description": "The Parques del Río urban renewal project is expanding southward through El Poblado, connecting green corridors along the Medellín River. This will significantly increase property values in adjacent blocks by an estimated 12-18% over 5 years.",
        "source": "Alcaldía de Medellín - POT 2030",
        "year": 2024,
        "estimated_value_impact": 0.15,
    },
    {
        "id": "us_002",
        "zone": "El Poblado",
        "neighborhood_id": "el_poblado",
        "signal_type": "market",
        "urban_growth_score": 0.80,
        "impact": "positive",
        "title": "International Tourism Growth Drives Short-Term Rental Demand",
        "description": "El Poblado continues to attract international tourists and digital nomads, with short-term rental occupancy rates averaging 82% annually. This sustains premium property prices and investment returns.",
        "source": "ProColombia Tourism Report 2024",
        "year": 2024,
        "estimated_value_impact": 0.10,
    },
    {
        "id": "us_003",
        "zone": "Laureles",
        "neighborhood_id": "laureles",
        "signal_type": "infrastructure",
        "urban_growth_score": 0.72,
        "impact": "positive",
        "title": "Metro Line B Capacity Expansion",
        "description": "Metro de Medellín is expanding Line B capacity with new trains and increased frequency, reducing commute times from Laureles to the city center by 30%. This improves connectivity scores for the western corridor.",
        "source": "Metro de Medellín 2024 Annual Report",
        "year": 2024,
        "estimated_value_impact": 0.08,
    },
    {
        "id": "us_004",
        "zone": "Envigado",
        "neighborhood_id": "envigado",
        "signal_type": "development",
        "urban_growth_score": 0.88,
        "impact": "positive",
        "title": "Envigado Tech District Formation",
        "description": "Several major Colombian tech companies are relocating headquarters to Envigado's new business district. This is expected to drive demand for nearby housing by 25% and increase average prices by 15% over 3 years.",
        "source": "Cámara de Comercio Aburrá Sur 2024",
        "year": 2024,
        "estimated_value_impact": 0.15,
    },
    {
        "id": "us_005",
        "zone": "Sabaneta",
        "neighborhood_id": "sabaneta",
        "signal_type": "development",
        "urban_growth_score": 0.92,
        "impact": "positive",
        "title": "Sabaneta Premium Mall Expansion",
        "description": "A major commercial expansion adding 45,000 m² of retail, dining, and entertainment is under construction in central Sabaneta. This will position Sabaneta as the premier retail destination of the southern Aburrá Valley.",
        "source": "Concejo de Sabaneta - Plan Desarrollo 2024-2027",
        "year": 2024,
        "estimated_value_impact": 0.12,
    },
    {
        "id": "us_006",
        "zone": "Bello",
        "neighborhood_id": "bello",
        "signal_type": "social",
        "urban_growth_score": 0.55,
        "impact": "neutral",
        "title": "Urban Security Improvement Program",
        "description": "The Municipal government has launched a comprehensive security improvement program in Bello, adding 200 surveillance cameras and increasing police patrols. Early data shows a 20% reduction in property crime.",
        "source": "Secretaría de Seguridad Medellín 2024",
        "year": 2024,
        "estimated_value_impact": 0.06,
    },
    {
        "id": "us_007",
        "zone": "Itagüí",
        "neighborhood_id": "itagui",
        "signal_type": "infrastructure",
        "urban_growth_score": 0.60,
        "impact": "positive",
        "title": "Metro Line A Southern Extension Study",
        "description": "A feasibility study for extending Metro Line A further south through Itagüí has been approved. While construction is 5+ years away, the announcement has already generated speculative investment interest.",
        "source": "Área Metropolitana Valle de Aburrá 2024",
        "year": 2024,
        "estimated_value_impact": 0.09,
    },
    {
        "id": "us_008",
        "zone": "La Floresta",
        "neighborhood_id": "floresta",
        "signal_type": "market",
        "urban_growth_score": 0.75,
        "impact": "positive",
        "title": "Overflow Demand from El Poblado Driving Floresta Growth",
        "description": "As El Poblado reaches saturation with prices surpassing 9M COP/m², buyers are discovering La Floresta as a premium alternative. Real estate activity increased 35% year-over-year with prices appreciating 11% annually.",
        "source": "Finca Raíz Market Analysis Q3 2024",
        "year": 2024,
        "estimated_value_impact": 0.11,
    },
    {
        "id": "us_009",
        "zone": "Robledo",
        "neighborhood_id": "robledo",
        "signal_type": "social",
        "urban_growth_score": 0.52,
        "impact": "neutral",
        "title": "University District Revitalization",
        "description": "Proximity to Universidad de Antioquia and Universidad Nacional is spurring café culture, co-working spaces, and creative economy activity in parts of Robledo. Student and faculty demand keeps rental markets active.",
        "source": "Cámara Colombiana de Construcción CAMACOL 2024",
        "year": 2024,
        "estimated_value_impact": 0.05,
    },
    {
        "id": "us_010",
        "zone": "San Antonio de Prado",
        "neighborhood_id": "san_antonio_prado",
        "signal_type": "development",
        "urban_growth_score": 0.80,
        "impact": "positive",
        "title": "New Highway Connector Reduces Commute Time by 40%",
        "description": "A new highway connector between San Antonio de Prado and the southern ring road is under construction, expected to reduce downtown commute times from 55 to 32 minutes. This will make the area significantly more attractive.",
        "source": "INVIAS Nacional - Plan Vial 2024",
        "year": 2024,
        "estimated_value_impact": 0.14,
    },
    {
        "id": "us_011",
        "zone": "Buenos Aires",
        "neighborhood_id": "buenos_aires",
        "signal_type": "social",
        "urban_growth_score": 0.62,
        "impact": "positive",
        "title": "Urban Renewal Gentrification Wave",
        "description": "Buenos Aires is experiencing an art-led gentrification with new galleries, boutique cafes, and creative studios opening along the hillside streets. Young professionals attracted to central location with lower prices are driving demand.",
        "source": "Lonja de Propiedad Raíz de Medellín 2024",
        "year": 2024,
        "estimated_value_impact": 0.07,
    },
    {
        "id": "us_012",
        "zone": "Belén",
        "neighborhood_id": "belen",
        "signal_type": "infrastructure",
        "urban_growth_score": 0.68,
        "impact": "positive",
        "title": "Belén Ruta N Innovation Hub Opening",
        "description": "A new technology and innovation hub inspired by Ruta N is opening in Belén, expected to attract over 3,000 tech workers to the area. New co-working spaces and residential demand is already rising.",
        "source": "Ruta N Medellín 2024",
        "year": 2024,
        "estimated_value_impact": 0.08,
    },
    {
        "id": "us_013",
        "zone": "Castilla",
        "neighborhood_id": "castilla",
        "signal_type": "social",
        "urban_growth_score": 0.45,
        "impact": "negative",
        "title": "Persistent Security Challenges in Some Sub-Sectors",
        "description": "Certain sub-sectors of Castilla continue to face security challenges from organized crime. While the overall trend is improving, buyers should request neighborhood-specific safety assessments before purchasing.",
        "source": "Personería de Medellín - Informe Derechos Humanos 2024",
        "year": 2024,
        "estimated_value_impact": -0.05,
    },
    {
        "id": "us_014",
        "zone": "Manrique",
        "neighborhood_id": "manrique",
        "signal_type": "infrastructure",
        "urban_growth_score": 0.55,
        "impact": "positive",
        "title": "Metro Cable K Modernization",
        "description": "The Metro Cable K connecting Manrique to the Metro system is receiving a full modernization with increased capacity gondolas. This significantly improves mobility for residents and is expected to boost property values.",
        "source": "Metro de Medellín - Plan Mejoramiento 2024",
        "year": 2024,
        "estimated_value_impact": 0.06,
    },
    {
        "id": "us_015",
        "zone": "El Estadio",
        "neighborhood_id": "el_estadio",
        "signal_type": "development",
        "urban_growth_score": 0.78,
        "impact": "positive",
        "title": "Atanasio Girardot Complex Modernization for Pan-American Games Bid",
        "description": "Colombia's bid for the 2031 Pan-American Games includes a major modernization of the Atanasio Girardot complex. If approved, this will drive massive infrastructure investment and tourism to the El Estadio area.",
        "source": "Comité Olímpico Colombiano 2024",
        "year": 2024,
        "estimated_value_impact": 0.13,
    },
    {
        "id": "us_016",
        "zone": "El Poblado",
        "neighborhood_id": "el_poblado",
        "signal_type": "market",
        "urban_growth_score": 0.70,
        "impact": "negative",
        "title": "Over-Tourism Pressure on Local Infrastructure",
        "description": "The extreme popularity of El Poblado has led to traffic congestion, rising service costs, and infrastructure strain. Some long-term residents are leaving, and the neighborhood's authenticity is being discussed by urban planners.",
        "source": "Veeduría Ciudadana Medellín 2024",
        "year": 2024,
        "estimated_value_impact": -0.03,
    },
    {
        "id": "us_017",
        "zone": "Envigado",
        "neighborhood_id": "envigado",
        "signal_type": "infrastructure",
        "urban_growth_score": 0.82,
        "impact": "positive",
        "title": "Envigado-Sabaneta Metro Extension Approved",
        "description": "The formal approval of a Metro extension from the current Envigado station south through Sabaneta was announced. Construction starts in 2026, with completion expected in 2030. This is expected to be a major catalyst for the southern corridor.",
        "source": "Gobernación de Antioquia 2024",
        "year": 2024,
        "estimated_value_impact": 0.18,
    },
    {
        "id": "us_018",
        "zone": "Laureles",
        "neighborhood_id": "laureles",
        "signal_type": "market",
        "urban_growth_score": 0.71,
        "impact": "positive",
        "title": "Remote Work Trend Sustains Family Housing Demand",
        "description": "The consolidation of remote and hybrid work among Medellín's professional class continues to fuel demand for larger apartments in Laureles, where families can enjoy space, parks, and good schools without sacrificing connectivity.",
        "source": "Lonja de Propiedad Raíz 2024",
        "year": 2024,
        "estimated_value_impact": 0.07,
    },
    {
        "id": "us_019",
        "zone": "Itagüí",
        "neighborhood_id": "itagui",
        "signal_type": "development",
        "urban_growth_score": 0.65,
        "impact": "positive",
        "title": "Industrial to Mixed-Use Zoning Conversion",
        "description": "Itagüí is converting 120 hectares of former industrial land to mixed-use residential and commercial zones. This will bring new housing supply at competitive prices with modern amenities over the next 5 years.",
        "source": "Concejo de Itagüí - POT 2024",
        "year": 2024,
        "estimated_value_impact": 0.10,
    },
    {
        "id": "us_020",
        "zone": "Bello",
        "neighborhood_id": "bello",
        "signal_type": "development",
        "urban_growth_score": 0.58,
        "impact": "positive",
        "title": "Bello Affordable Housing Mega-Project",
        "description": "A public-private partnership is building 4,500 affordable housing units in Bello's northern sector near the Metro, targeting families earning 2-4 minimum wages. This brings new amenities to the area but may affect existing property values.",
        "source": "Ministerio de Vivienda Colombia 2024",
        "year": 2024,
        "estimated_value_impact": 0.04,
    },
]

# ──────────────────────────────────────────────
# PROPERTY GENERATOR
# ──────────────────────────────────────────────

PROPERTY_TYPES = ["Apartamento", "Casa", "Penthouse", "Loft", "Estudio", "Apartaestudio"]
AMENITY_POOL = [
    "Piscina", "Gimnasio", "Parque infantil", "Salón social", "Terraza",
    "BBQ", "Sauna", "Jacuzzi", "Lobby de lujo", "Ascensor", "Citófono",
    "Zona de lavandería", "Cuarto útil", "Depósito", "Portería 24h",
    "Cámaras de seguridad", "Zonas verdes", "Cancha de tenis",
    "Cancha de squash", "Zona de yoga", "Coworking", "Pet zone",
    "Ciclovía interna", "Parqueadero visitantes", "Estudio de música",
]

TITLES_TEMPLATES = [
    "Hermoso {type} en {zone} con vista espectacular",
    "{type} moderno en {zone} con excelentes acabados",
    "{type} familiar amplio en {zone}",
    "Acogedor {type} en {zone} ideal para inversión",
    "{type} de lujo en {zone} con todas las comodidades",
    "Exclusivo {type} en {zone} con acabados premium",
    "{type} central en {zone} con fácil acceso al metro",
    "Espacioso {type} en {zone} cerca de parques",
    "Moderno {type} en {zone} con terraza privada",
    "{type} en conjunto cerrado en {zone}",
    "{type} nuevo en {zone} con certificación verde",
    "{type} amplio en {zone} excelente ubicación",
    "Coqueto {type} en {zone} ideal para solteros o parejas",
    "{type} con diseño arquitectónico único en {zone}",
    "Luminoso {type} en {zone} con balcón panorámico",
]

DESCRIPTION_TEMPLATES = [
    "Excelente {type} ubicado en el corazón de {zone}, con acabados de primera calidad y amplias zonas sociales. Cerca de centros comerciales, colegios y transporte público.",
    "Moderno y espacioso {type} en {zone}. Cuenta con cocina integral, baños con jacuzzi, y una ubicación privilegiada a {metro_dist:.1f} km del metro. Conjunto con piscina y gimnasio.",
    "Impresionante {type} con vistas panorámicas en {zone}. Ideal para familias que buscan calidad de vida, seguridad y excelente valorización. Zona tranquila y residencial.",
    "Hermoso {type} de {area} m² en {zone}. Diseño contemporáneo con materiales importados, cocina abierta al living, y terraza con vista al verde. Excelente oportunidad de inversión.",
    "Amplio y luminoso {type} en {zone}, con {beds} habitaciones y {baths} baños completos. A pocos pasos de colegios, supermercados y el sistema de transporte masivo.",
    "Propiedad de alta gama en {zone}. El {type} cuenta con acabados europeos, domótica, y acceso a amenidades de primer nivel. Rentabilidad garantizada como inmueble de inversión.",
    "Cómodo {type} en {zone} perfecto para familia o inversión. Buena iluminación natural, distribución funcional y ubicación estratégica en zona segura y bien valorizada.",
    "{type} en excelente estado en {zone}. Construcción reciente, conjunto residencial cerrado con seguridad 24/7, zonas verdes y piscina. Fácil acceso a vías principales.",
]


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def generate_properties() -> List[Dict[str, Any]]:
    properties: List[Dict[str, Any]] = []
    prop_id = 1

    # Weight distribution per neighborhood (approximate number of properties)
    distribution = {
        "el_poblado": 40,
        "laureles": 28,
        "envigado": 28,
        "sabaneta": 22,
        "bello": 18,
        "itagui": 15,
        "robledo": 18,
        "belen": 20,
        "castilla": 15,
        "floresta": 20,
        "la_america": 15,
        "buenos_aires": 15,
        "manrique": 12,
        "san_antonio_prado": 18,
        "el_estadio": 16,
    }

    neighborhood_map = {n["id"]: n for n in NEIGHBORHOODS}

    for nbhd_id, count in distribution.items():
        nbhd = neighborhood_map[nbhd_id]
        base_price_m2 = nbhd["average_price_m2"]
        safety = nbhd["safety_score"]
        transport = nbhd["transport_score"]
        investment = nbhd["investment_score"]

        for _ in range(count):
            prop_type = random.choices(
                PROPERTY_TYPES,
                weights=[45, 15, 5, 8, 10, 17],
            )[0]

            # Determine size ranges per type
            if prop_type in ("Estudio", "Apartaestudio"):
                area = round(random.uniform(28, 55), 1)
                beds = random.choice([0, 1])
                baths = 1
            elif prop_type == "Loft":
                area = round(random.uniform(45, 90), 1)
                beds = random.choice([1, 2])
                baths = random.choice([1, 2])
            elif prop_type == "Penthouse":
                area = round(random.uniform(120, 280), 1)
                beds = random.choice([3, 4, 5])
                baths = random.choice([3, 4, 5])
            elif prop_type == "Casa":
                area = round(random.uniform(80, 350), 1)
                beds = random.choice([3, 4, 5])
                baths = random.choice([2, 3, 4])
            else:  # Apartamento
                area = round(random.uniform(40, 180), 1)
                beds = random.choice([1, 2, 3, 4])
                baths = max(1, beds - 1 + random.randint(0, 1))

            parking = 0 if prop_type in ("Estudio", "Apartaestudio") else random.choice([0, 1, 1, 1, 2, 2])

            # Price: base_price_m2 * area * variation
            price_variation = random.uniform(0.85, 1.25)
            # Penthouses command premium
            if prop_type == "Penthouse":
                price_variation *= random.uniform(1.3, 1.8)
            price = round(base_price_m2 * area * price_variation)

            stratum = round(nbhd["avg_stratum"] + random.uniform(-0.5, 0.5))
            stratum = max(1, min(6, stratum))

            # Metro distance (varies around neighborhood baseline)
            nbhd_lat = nbhd["latitude"]
            nbhd_lng = nbhd["longitude"]
            prop_lat = nbhd_lat + random.uniform(-0.015, 0.015)
            prop_lng = nbhd_lng + random.uniform(-0.015, 0.015)

            # Metro station distance estimate based on neighborhood transport score
            metro_dist_base = lerp(3.5, 0.2, transport)
            metro_dist = round(metro_dist_base + random.uniform(-0.3, 0.8), 2)
            metro_dist = max(0.1, metro_dist)

            pet_friendly = random.choices([True, False], weights=[0.55, 0.45])[0]

            # Zone scores with property-level variance
            zone_safety = round(safety + random.uniform(-0.08, 0.05), 3)
            zone_inv = round(investment + random.uniform(-0.07, 0.07), 3)
            zone_transport = round(transport + random.uniform(-0.08, 0.06), 3)

            # Clamp
            zone_safety = max(0.0, min(1.0, zone_safety))
            zone_inv = max(0.0, min(1.0, zone_inv))
            zone_transport = max(0.0, min(1.0, zone_transport))

            # Amenities (more premium = more amenities)
            num_amenities = max(2, int(stratum * 1.5 + random.randint(0, 3)))
            amenities = random.sample(AMENITY_POOL, min(num_amenities, len(AMENITY_POOL)))

            title_tpl = random.choice(TITLES_TEMPLATES)
            title = title_tpl.format(type=prop_type, zone=nbhd["name"])

            desc_tpl = random.choice(DESCRIPTION_TEMPLATES)
            desc = desc_tpl.format(
                type=prop_type.lower(),
                zone=nbhd["name"],
                metro_dist=metro_dist,
                area=int(area),
                beds=beds,
                baths=baths,
            )

            properties.append({
                "id": f"prop_{prop_id:04d}",
                "title": title,
                "city": "Medellín",
                "neighborhood": nbhd["name"],
                "neighborhood_id": nbhd_id,
                "price": price,
                "area_m2": area,
                "bedrooms": beds,
                "bathrooms": baths,
                "parking_spots": parking,
                "property_type": prop_type,
                "stratum": stratum,
                "distance_to_metro_km": metro_dist,
                "description": desc,
                "amenities": amenities,
                "pet_friendly": pet_friendly,
                "zone_safety_score": zone_safety,
                "investment_score": zone_inv,
                "transport_score": zone_transport,
                "latitude": round(prop_lat, 6),
                "longitude": round(prop_lng, 6),
                "available": True,
                "listing_date": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "price_per_m2": round(price / area),
            })
            prop_id += 1

    random.shuffle(properties)
    # Re-assign sequential IDs after shuffle
    for i, p in enumerate(properties, 1):
        p["id"] = f"prop_{i:04d}"

    return properties


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)

    # Neighborhoods
    with open(os.path.join(out_dir, "neighborhoods.json"), "w", encoding="utf-8") as f:
        json.dump(NEIGHBORHOODS, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(NEIGHBORHOODS)} neighborhoods")

    # Urban signals
    with open(os.path.join(out_dir, "urban_signals.json"), "w", encoding="utf-8") as f:
        json.dump(URBAN_SIGNALS, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(URBAN_SIGNALS)} urban signals")

    # Properties
    properties = generate_properties()
    with open(os.path.join(out_dir, "properties.json"), "w", encoding="utf-8") as f:
        json.dump(properties, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(properties)} properties")

    # Summary
    type_counts: Dict[str, int] = {}
    for p in properties:
        type_counts[p["property_type"]] = type_counts.get(p["property_type"], 0) + 1
    print("  Distribution by type:", type_counts)


if __name__ == "__main__":
    main()
