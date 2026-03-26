import json
import os
import re
import socket
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "products.json")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


app = Flask(__name__)
CORS(app)


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    keywords: List[str]
    water_liters: float
    unit: str
    category: str
    alternatives: List[str]
    product_type: str
    calories_per_unit: Optional[float]
    health_note: Optional[str]
    material_info: Optional[str]
    material_alternatives: List[str]
    regions: List[Dict[str, Any]]


def load_products() -> Tuple[Dict[str, Product], List[Product]]:
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"products.json bulunamadı: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    items = raw.get("products", [])
    products: List[Product] = []
    for p in items:
        products.append(
            Product(
                id=str(p.get("id", "")),
                name=str(p.get("name", "")),
                keywords=list(p.get("keywords", [])),
                water_liters=float(p.get("water_liters", 0)),
                unit=str(p.get("unit", "")),
                category=str(p.get("category", "")),
                alternatives=list(p.get("alternatives", [])),
                product_type=str(p.get("product_type", "food")),
                calories_per_unit=(
                    float(p["calories_per_unit"])
                    if p.get("calories_per_unit") is not None
                    else None
                ),
                health_note=(
                    str(p.get("health_note")) if p.get("health_note") is not None else None
                ),
                material_info=(
                    str(p.get("material_info")) if p.get("material_info") is not None else None
                ),
                material_alternatives=list(p.get("material_alternatives", [])),
                regions=list(p.get("regions", [])),
            )
        )

    by_id = {p.id: p for p in products if p.id}
    return by_id, products


PRODUCTS_BY_ID, PRODUCTS = load_products()

PRODUCTION_ZONES: List[Dict[str, Any]] = [
    {
        "id": "konya_high",
        "label": "Konya - Yuksek Su Stresi",
        "stress_level": "high",
        "stress_multiplier": 2.0,
    },
    {
        "id": "gaziantep_medium",
        "label": "Gaziantep - Orta Su Stresi",
        "stress_level": "medium",
        "stress_multiplier": 1.4,
    },
    {
        "id": "rize_low",
        "label": "Rize - Dusuk Su Stresi",
        "stress_level": "low",
        "stress_multiplier": 1.0,
    },
]

BUTTERFLY_IMPACT_POOL: List[Dict[str, str]] = [
    {
        "region": "Kenya / Turkana Golu",
        "message": "Kurtardiginiz su, kuraklikla mucadele eden topluluklara sanal destek oldu.",
    },
    {
        "region": "Aral Havzasi",
        "message": "Sanal su transferi, ekosistem restorasyonu farkindaligina katkida bulundu.",
    },
    {
        "region": "Konya Kapali Havzasi",
        "message": "Yerel su stresi bilinci icin dijital etki puani olusturuldu.",
    },
]


def normalize_text(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("ı", "i").replace("İ", "i").replace("ş", "s").replace("Ş", "s")
    s = s.replace("ğ", "g").replace("Ğ", "g").replace("ü", "u").replace("Ü", "u")
    s = s.replace("ö", "o").replace("Ö", "o").replace("ç", "c").replace("Ç", "c")
    s = re.sub(r"\s+", " ", s)
    return s


def ecosystem_status(water_liters: float) -> str:
    # PRD eşikleri:
    # Kritik: > 1000
    # Orta: 100 < x < 1000
    # İyi: < 100
    # Sınır kararları (MVP): 100 -> orta, 1000 -> kritik
    if water_liters >= 1000:
        return "critical"
    if water_liters >= 100:
        return "medium"
    return "good"


def find_product(query: str) -> Optional[Product]:
    q = normalize_text(query)
    if not q:
        return None

    # 1) İsim tam eşleşmesi
    for p in PRODUCTS:
        if normalize_text(p.name) == q:
            return p

    # 2) Keyword tam eşleşmesi
    for p in PRODUCTS:
        for kw in p.keywords:
            if normalize_text(str(kw)) == q:
                return p

    # 3) Keyword "içerir" eşleşmesi (en basit)
    for p in PRODUCTS:
        for kw in p.keywords:
            nkw = normalize_text(str(kw))
            if q in nkw or nkw in q:
                return p

    return None


def product_to_response(p: Product) -> Dict[str, Any]:
    alt_products: List[Dict[str, Any]] = []
    for alt_id in p.alternatives:
        alt = PRODUCTS_BY_ID.get(alt_id)
        if not alt:
            continue
        alt_products.append(
            {
                "id": alt.id,
                "name": alt.name,
                "water_liters": alt.water_liters,
                "unit": alt.unit,
                "status": ecosystem_status(alt.water_liters),
            }
        )

    return {
        "id": p.id,
        "name": p.name,
        "water_liters": p.water_liters,
        "unit": p.unit,
        "category": p.category,
        "product_type": p.product_type,
        "status": ecosystem_status(p.water_liters),
        "alternatives": alt_products,
        "regions": p.regions,
        "calories_per_unit": p.calories_per_unit,
        "health_note": p.health_note,
        "material_info": p.material_info,
        "material_alternatives": p.material_alternatives,
    }


@app.get("/api/search")
def api_search():
    q = request.args.get("q", "")
    product = find_product(q)
    if not product:
        examples = [p.name for p in PRODUCTS[:6]]
        return (
            jsonify(
                {
                    "error": "not_found",
                    "message": "Ürün bulunamadı. Başka bir arama deneyin.",
                    "examples": examples,
                }
            ),
            404,
        )

    return jsonify(product_to_response(product))


@app.get("/api/health")
def api_health():
    return jsonify({"ok": True})


@app.get("/api/production-zones")
def api_production_zones():
    return jsonify({"zones": PRODUCTION_ZONES})


@app.get("/api/impact-transfer")
def api_impact_transfer():
    saved_liters = float(request.args.get("saved_liters", "0") or 0)
    bucket = int(saved_liters) % len(BUTTERFLY_IMPACT_POOL)
    selected = BUTTERFLY_IMPACT_POOL[bucket]
    return jsonify(
        {
            "region": selected["region"],
            "message": selected["message"],
            "saved_liters": round(saved_liters, 2),
        }
    )


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(FRONTEND_DIR, path)


@app.errorhandler(Exception)
def handle_unexpected_error(e: Exception):
    # Flask'in 404/400 gibi HTTP hatalarını 500'e çevirmeyelim.
    # (Örn: frontend dosyası bulunamazsa 404 dönmeli.)
    if isinstance(e, HTTPException):
        return e

    return (
        jsonify(
            {
                "error": "server_error",
                "message": "Beklenmeyen bir hata oluştu.",
            }
        ),
        500,
    )


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    preferred_port = int(os.environ.get("PORT", "5000"))

    # Port 5000 doluysa otomatik başka bir port seçelim (bağlanmayı reddetti hatasının
    # en sık nedeni: sunucunun hiç açılmaması / port çakışması).
    port = preferred_port
    for candidate in [preferred_port, 5001, 8000, 8080]:
        try:
            with socket.create_connection((host, candidate), timeout=0.2):
                # Bağlantı kurulabiliyorsa port dolu demektir -> başka port dene
                continue
        except OSError:
            port = candidate
            break

    print(f"Server: http://{host}:{port}")
    app.run(host=host, port=port, debug=True)

