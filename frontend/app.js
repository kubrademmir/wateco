const form = document.querySelector("#searchForm");
const queryInput = document.querySelector("#query");
const submitBtn = document.querySelector("#submitBtn");

const emptyStateEl = document.querySelector("#emptyState");
const errorEl = document.querySelector("#error");
const resultEl = document.querySelector("#result");
const altEl = document.querySelector("#alternatives");
const savedEl = document.querySelector("#saved");
const insightEl = document.querySelector("#insight");

const ecosystemEl = document.querySelector("#ecosystem");
const ecosystemTitleEl = document.querySelector("#ecoTitle");
const ecosystemDescEl = document.querySelector("#ecoDesc");

let lastProduct = null;
let map = null;
let markerLayer = null;

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? "Hesaplanıyor..." : "Hesapla";
}

function statusText(status) {
  if (status === "critical") return "Kritik";
  if (status === "medium") return "Orta";
  return "İyi";
}

function statusDesc(status) {
  if (status === "critical") return "Toprak çatlıyor; ekosistem ciddi stres altında.";
  if (status === "medium") return "Doğa sararıyor; daha iyi bir seçimle toparlanabilir.";
  return "Ekosistem canlı; iyi bir tercih yaptın.";
}

function setEcosystem(status) {
  ecosystemEl.classList.remove("ecosystem--good", "ecosystem--medium", "ecosystem--critical");
  ecosystemEl.classList.add(`ecosystem--${status}`);
  ecosystemTitleEl.textContent = `Ekosistem Durumu: ${statusText(status)}`;
  ecosystemDescEl.textContent = statusDesc(status);
}

function show(el) {
  el.hidden = false;
}

function hide(el) {
  el.hidden = true;
}

function formatLiters(n) {
  return new Intl.NumberFormat("tr-TR").format(Math.round(n));
}

function formatCalories(n) {
  if (n === null || n === undefined) return "-";
  return `${new Intl.NumberFormat("tr-TR").format(Math.round(n))} kcal`;
}

function initMap() {
  if (map || !window.L) return;
  map = L.map("map", { worldCopyJump: true }).setView([20, 0], 2);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 8,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);
  markerLayer = L.layerGroup().addTo(map);
}

function riskColor(level) {
  if (level === "critical") return "#e74c3c";
  if (level === "bad") return "#e67e22";
  if (level === "medium") return "#f1c40f";
  return "#2ecc71";
}

function riskText(level) {
  if (level === "critical") return "Kritik";
  if (level === "bad") return "Kotu";
  if (level === "medium") return "Orta";
  return "Iyi";
}

function renderMapRegions(product) {
  initMap();
  if (!map || !markerLayer) return;

  markerLayer.clearLayers();
  const regions = Array.isArray(product.regions) ? product.regions : [];
  if (!regions.length) {
    map.setView([20, 0], 2);
    return;
  }

  const bounds = [];
  regions.forEach((r) => {
    if (typeof r.lat !== "number" || typeof r.lng !== "number") return;
    const color = riskColor(r.risk);
    const marker = L.circleMarker([r.lat, r.lng], {
      radius: 8,
      color,
      fillColor: color,
      fillOpacity: 0.8,
      weight: 1,
    });
    marker.bindPopup(`<strong>${r.name}</strong><br/>Risk: ${riskText(r.risk)}`);
    marker.addTo(markerLayer);
    bounds.push([r.lat, r.lng]);
  });

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [24, 24], maxZoom: 4 });
  }
}

function renderInsight(p) {
  if (p.product_type === "clothing") {
    const alternatives = Array.isArray(p.material_alternatives) ? p.material_alternatives : [];
    insightEl.innerHTML = `
      <div><strong>Urun Materyali ve Surdurulebilir Alternatifler</strong></div>
      <div class="muted" style="margin-top:6px">Malzeme: ${p.material_info || "Bilgi yok"}</div>
      <div class="muted" style="margin-top:6px">Alternatif malzemeler: ${
        alternatives.length ? alternatives.join(", ") : "Alternatif bilgi yok"
      }</div>
    `;
    return;
  }

  insightEl.innerHTML = `
    <div><strong>Beslenme Notu</strong></div>
    <div class="muted" style="margin-top:6px">Kalori: ${formatCalories(p.calories_per_unit)} / secilen birim</div>
    <div class="muted" style="margin-top:6px">${p.health_note || "Saglik notu bulunamadi."}</div>
  `;
}

function renderProduct(p) {
  hide(emptyStateEl);
  hide(errorEl);
  show(resultEl);

  resultEl.innerHTML = `
    <div class="pill" data-status="${p.status}">
      <strong>${p.name}</strong>
      <span class="muted">• ${formatLiters(p.water_liters)} L</span>
      <span class="muted">• ${statusText(p.status)}</span>
    </div>
    <div style="margin-top:10px" class="muted">
      Bu seçim, görünmez su maliyetiyle ekosistemi etkiler.
    </div>
  `;

  setEcosystem(p.status);
  renderMapRegions(p);
  renderInsight(p);
  renderAlternatives(p);
}

function renderAlternatives(p) {
  altEl.innerHTML = "";
  savedEl.innerHTML = "";

  if (!p.alternatives || p.alternatives.length === 0) {
    altEl.innerHTML = `<div class="muted">Bu ürün için şu an alternatif önerimiz yok.</div>`;
    return;
  }

  altEl.innerHTML = `
    <div><strong>Bunu değil, şunu dene</strong></div>
    <div class="muted" style="margin-top:4px">Daha düşük su ayak izli alternatiflere tıklayabilirsin.</div>
    <div class="alt-list" id="altList"></div>
  `;

  const altList = altEl.querySelector("#altList");
  for (const a of p.alternatives) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = `${a.name} • ${formatLiters(a.water_liters)} L`;
    btn.addEventListener("click", () => onAlternativeClick(a, p));
    altList.appendChild(btn);
  }
}

async function onAlternativeClick(alt, current) {
  // Alternatife basınca onu aratıyoruz (MVP için en basit akış).
  await search(alt.name, current);
}

function renderSaved(previous, next) {
  const diff = previous.water_liters - next.water_liters;
  if (diff <= 0) return;
  savedEl.innerHTML = `<div class="card"><strong>Teşekkürler!</strong> Yaklaşık <strong>${formatLiters(diff)} litre</strong> su kurtarıldı.</div>`;
}

async function search(q, previousProduct = null) {
  setLoading(true);
  hide(errorEl);

  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const data = await res.json();

    if (!res.ok) {
      const examples = Array.isArray(data.examples) ? data.examples : [];
      show(errorEl);
      errorEl.innerHTML = `
        <div class="alert">
          <strong>${data.message || "Bir hata oluştu."}</strong>
          ${
            examples.length
              ? `<div class="muted" style="margin-top:6px">Örnek: ${examples.join(", ")}</div>`
              : ""
          }
        </div>
      `;
      hide(resultEl);
      altEl.innerHTML = "";
      savedEl.innerHTML = "";
      return;
    }

    lastProduct = data;
    renderProduct(data);

    if (previousProduct) {
      renderSaved(previousProduct, data);
    }
  } catch (e) {
    show(errorEl);
    errorEl.innerHTML = `<div class="alert"><strong>Ağ hatası:</strong> Backend çalışıyor mu?</div>`;
  } finally {
    setLoading(false);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = queryInput.value.trim();
  if (!q) return;
  await search(q, lastProduct);
});

// İlk görünüm
setEcosystem("good");
initMap();
