"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getProperties } from "@/lib/api";
import type { Property } from "@/lib/types";
import { formatPrice } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  MapPin, BedDouble, Bath, Car, Ruler, Train,
  Shield, TrendingUp, ArrowLeft, Calendar, PawPrint, Building2
} from "lucide-react";

function InfoRow({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center justify-between py-2.5 border-b border-gray-100 last:border-0">
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <span className="text-gray-400">{icon}</span>
        {label}
      </div>
      <span className="text-sm font-semibold text-gray-800">{value}</span>
    </div>
  );
}

function ScoreCircle({ value, label }: { value: number; label: string }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 85 ? "text-emerald-600 bg-emerald-50"
    : pct >= 70 ? "text-blue-600 bg-blue-50"
    : "text-amber-600 bg-amber-50";
  return (
    <div className={`flex flex-col items-center justify-center w-20 h-20 rounded-2xl ${color}`}>
      <span className="text-2xl font-bold">{pct}</span>
      <span className="text-[10px] opacity-70 mt-0.5">{label}</span>
    </div>
  );
}

export default function PropertyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const [property, setProperty] = useState<Property | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProperties()
      .then((props) => {
        const found = props.find((p) => p.id === id) ?? null;
        setProperty(found);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 space-y-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-100 animate-pulse rounded-xl" />
        ))}
      </div>
    );
  }

  if (!property) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-24 text-center">
        <Building2 className="w-12 h-12 mx-auto text-gray-300 mb-4" />
        <h1 className="text-xl font-bold text-gray-700">Propiedad no encontrada</h1>
        <Button variant="outline" className="mt-4" onClick={() => router.back()}>
          Volver
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10 space-y-6">
      {/* Back button */}
      <Button variant="ghost" size="sm" className="gap-2" onClick={() => router.back()}>
        <ArrowLeft className="w-4 h-4" /> Volver
      </Button>

      {/* Header */}
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline">{property.property_type}</Badge>
          {property.pet_friendly && (
            <Badge variant="secondary" className="gap-1">
              <PawPrint className="w-3 h-3" /> Mascotas OK
            </Badge>
          )}
          {property.available && (
            <Badge className="bg-emerald-600">Disponible</Badge>
          )}
        </div>
        <h1 className="text-2xl font-bold text-gray-900">{property.title}</h1>
        <div className="flex items-center gap-1.5 text-gray-500">
          <MapPin className="w-4 h-4" />
          <span>
            {property.neighborhood}, {property.city} · Estrato{" "}
            {property.stratum}
          </span>
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-3xl font-bold text-gray-900">
            {formatPrice(property.price)}
          </span>
          <span className="text-sm text-gray-400">
            ${(property.price_per_m2 / 1_000_000).toFixed(1)}M/m²
          </span>
        </div>
      </div>

      <Separator />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Quick stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { icon: <BedDouble className="w-5 h-5" />, value: `${property.bedrooms}`, label: "Habitaciones" },
              { icon: <Bath className="w-5 h-5" />, value: `${property.bathrooms}`, label: "Baños" },
              { icon: <Ruler className="w-5 h-5" />, value: `${property.area_m2}`, label: "m²" },
              { icon: <Car className="w-5 h-5" />, value: `${property.parking_spots}`, label: "Parqueaderos" },
            ].map((s) => (
              <div
                key={s.label}
                className="flex flex-col items-center justify-center bg-gray-50 rounded-xl py-4 px-3 text-center"
              >
                <span className="text-gray-400 mb-1">{s.icon}</span>
                <span className="text-xl font-bold text-gray-900">{s.value}</span>
                <span className="text-xs text-gray-500 mt-0.5">{s.label}</span>
              </div>
            ))}
          </div>

          {/* Description */}
          <div>
            <h2 className="font-semibold text-gray-900 mb-2">Descripción</h2>
            <p className="text-gray-600 leading-relaxed">{property.description}</p>
          </div>

          {/* Amenities */}
          <div>
            <h2 className="font-semibold text-gray-900 mb-3">
              Amenidades ({property.amenities.length})
            </h2>
            <div className="flex flex-wrap gap-2">
              {property.amenities.map((a) => (
                <Badge key={a} variant="outline">
                  {a}
                </Badge>
              ))}
            </div>
          </div>

          {/* Details table */}
          <div>
            <h2 className="font-semibold text-gray-900 mb-3">Información adicional</h2>
            <div className="bg-gray-50 rounded-xl px-4">
              <InfoRow icon={<Train className="w-4 h-4" />} label="Distancia al metro" value={`${property.distance_to_metro_km} km`} />
              <InfoRow icon={<MapPin className="w-4 h-4" />} label="Vecindario" value={property.neighborhood} />
              <InfoRow icon={<Building2 className="w-4 h-4" />} label="Tipo" value={property.property_type} />
              <InfoRow icon={<Calendar className="w-4 h-4" />} label="Fecha publicación" value={property.listing_date} />
              <InfoRow icon={<Ruler className="w-4 h-4" />} label="Precio por m²" value={`$${property.price_per_m2.toLocaleString("es-CO")} COP`} />
            </div>
          </div>
        </div>

        {/* Scores sidebar */}
        <div className="space-y-6">
          <div>
            <h2 className="font-semibold text-gray-900 mb-3">Scores de zona</h2>
            <div className="flex flex-wrap gap-2">
              <ScoreCircle value={property.zone_safety_score} label="Seguridad" />
              <ScoreCircle value={property.investment_score} label="Inversión" />
              <ScoreCircle value={property.transport_score} label="Transporte" />
            </div>
          </div>

          {/* Map placeholder */}
          <div>
            <h2 className="font-semibold text-gray-900 mb-3">Ubicación</h2>
            <div className="bg-gray-100 rounded-xl h-40 flex flex-col items-center justify-center text-gray-400">
              <MapPin className="w-8 h-8 mb-2" />
              <p className="text-xs text-center">
                {property.latitude.toFixed(4)}, {property.longitude.toFixed(4)}
              </p>
              <p className="text-xs mt-1">{property.neighborhood}</p>
            </div>
          </div>

          <Button className="w-full" size="lg">
            Contactar agente
          </Button>
          <Button variant="outline" className="w-full" onClick={() => router.back()}>
            Ver más opciones
          </Button>
        </div>
      </div>
    </div>
  );
}
