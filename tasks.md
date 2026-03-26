# Tasks: Sudan Ekosisteme (MVP)

Bu dosya `prd.md` kapsamındaki MVP’yi adım adım geliştirmek için görev listesidir.

## 0) Proje hazırlığı
- [ ] **Repo/klasör yapısı**: `frontend/`, `backend/`, `data/` klasörlerini oluştur.
- [ ] **Dokümantasyon**: `README.md` içine kurulum/çalıştırma adımlarını ekle.
- [ ] **Ortam**: Python sanal ortamı (venv) ve bağımlılık dosyasını (`requirements.txt`) oluştur.
- [ ] **Geliştirme standardı**: Basit bir `.gitignore` ekle (venv, __pycache__, node_modules vb.).

## 1) Veri modeli (JSON) ve içerik
- [ ] **Veri şeması**: Ürün kayıt formatını tanımla.
  - Öneri alanlar: `id`, `name`, `keywords`, `water_liters`, `unit`, `category`, `alternatives` (id listesi), `source` (opsiyonel)
- [ ] **Başlangıç datası**: En az 15–25 ürün ekle (kahve, kot pantolon, dana eti gibi yüksek; mevsim sebzeleri gibi düşük).
- [ ] **Alternatif eşleştirme**: Yüksek su ayak izi olan her ürün için en az 1 düşük su ayak izli alternatif bağla.
- [ ] **Arama anahtarları**: Türkçe yazım varyasyonları için `keywords` alanını doldur (örn. “kot”, “jean”, “kot pantolon”).

## 2) Backend (Flask/FastAPI) – API
- [ ] **İskelet**: Backend uygulamasını ayağa kaldır (Flask veya FastAPI).
- [ ] **JSON yükleme**: Uygulama açılışında `data/products.json` verisini yükle (veya her istek için oku).
- [ ] **Arama endpoint’i**: `GET /api/search?q=...`
  - [ ] Eşleşen ürünü bul (tam eşleşme + keyword içeren arama).
  - [ ] Yanıt: ürün adı, litre değeri, durum (iyi/orta/kritik), alternatifler listesi.
  - [ ] Bulunamazsa: anlamlı 404 + önerilen arama ipucu döndür.
- [ ] **Alternatif endpoint’i (opsiyonel)**: `GET /api/product/{id}` (ürün + alternatif detayları).
- [ ] **CORS**: Frontend ile çalışacak şekilde CORS ayarla.
- [ ] **Hata yönetimi**: Beklenmeyen hatalarda tutarlı JSON error formatı döndür.

## 3) Su ayak izi → Ekosistem durumu hesaplama
- [ ] **Kural**: Durum eşikleri PRD’ye göre hesapla.
  - [ ] Kritik: \(> 1000L\)
  - [ ] Orta: \(100L < x < 1000L\)
  - [ ] İyi: \(< 100L\)
- [ ] **Sınır değerler**: Tam 100L ve tam 1000L davranışını netleştir ve kodda tek noktada uygula (örn. 100L “iyi” mi “orta” mı?).

## 4) Frontend – Ana akış (MVP)
- [ ] **Ana sayfa**: Sade bir sayfa, arama kutusu, “Hesapla” butonu.
- [ ] **API entegrasyonu**: Arama formu submit → backend `/api/search` çağrısı.
- [ ] **Sonuç kartı**: Ürün adı + litre değeri + kısa açıklama metni.
- [ ] **Durum mesajı**: Ekosistem durumunu metinle de göster (örn. “Kritik: ekosistem kuruyor”).
- [ ] **Boş durum**: İlk açılışta yönlendirici metin (örn. “Bir ürün yaz ve hesapla”).
- [ ] **Bulunamadı**: Kullanıcıya alternatif örnek aramalar göster.

## 5) Dinamik ekosistem görselleştirmesi
- [ ] **Görsel yaklaşım seçimi**:
  - [ ] Basit: 3 ayrı arkaplan illüstrasyon (CSS background / SVG) + yumuşak geçiş
  - [ ] Orta: Tek sahne + CSS class ile kuruma/yeşerme (filtre/opacity/ton)
- [ ] **Durum sınıfları**: `ecosystem--good`, `ecosystem--medium`, `ecosystem--critical` gibi sınıflar tanımla.
- [ ] **Animasyon**: Durum değişince geçiş animasyonu (fade/transform) uygula.
- [ ] **Erişilebilirlik**: Animasyonları “reduced motion” tercihine göre azalt.

## 6) Alternatif öneri motoru (UI + davranış)
- [ ] **Öneri bölümü**: Sonucun altında “Bunu değil, şunu dene” alanı.
- [ ] **Buton**: Alternatife tıklanınca aynı akışla yeni ürün seçimi gibi davran.
- [ ] **Kurtarılan su mesajı**: “Teşekkürler, X litre su kurtarıldı!” mesajını göster.
  - [ ] X = (eski litre - yeni litre)
  - [ ] Negatif çıkarsa mesajı bastır (veya farklı mesaj).

## 7) UI/UX parlatma (MVP kapsamı içinde)
- [ ] **Mobil uyum**: Arama ve sonuç ekranı responsive.
- [ ] **Yükleniyor durumu**: API çağrısı sırasında spinner/skeleton.
- [ ] **Hata durumu**: Ağ hatası / sunucu hatası için kullanıcı dostu mesaj.
- [ ] **Kopyalanabilir çıktı**: Litre değerini ve durum özetini kopyalama butonu (opsiyonel).

## 8) Ölçümleme (hafif)
- [ ] **Event kayıtları (opsiyonel)**: Arama sayısı, alternatif tıklama sayısı (basit console log veya backend’de minimal sayım).
- [ ] **Başarı metrikleriyle hizalama**: Alternatif tıklama oranını gözlemlemek için sayfa içi sayaç.

## 9) Test ve doğrulama
- [ ] **Manuel test senaryoları**:
  - [ ] Yüksek (>1000L) ürün arama → kritik ekosistem + alternatif gösterimi
  - [ ] Orta (100–1000L) ürün arama → bozkır
  - [ ] Düşük (<100L) ürün arama → yeşil
  - [ ] Alternatife tıkla → ekosistem iyileşiyor + “kurtarılan su” mesajı
  - [ ] Bulunamadı → doğru hata + örnek aramalar
- [ ] **Sınır testleri**: 99L/100L/101L ve 999L/1000L/1001L kayıtlarıyla doğrula.

## 10) Çalıştırma ve paketleme
- [ ] **Geliştirme çalıştırma**: Backend ve frontend için tek komutluk yönergeler (README).
- [ ] **Basit dağıtım (opsiyonel)**:
  - [ ] Backend’i bir PaaS’a (Render/Fly/Heroku alternatifi) koyma planı
  - [ ] Frontend’i statik hosta (Netlify/Vercel) koyma planı

## 11) MVP sonrası (Roadmap notları)
- [ ] **V2**: Fotoğraftan ürün tanıma (Image Recognition).
- [ ] **V3**: Kullanıcı bahçesi + üyelik sistemi.
- [ ] **V4**: Coğrafi su stresi verilerini API ile entegre etme.

