# PRD: Sudan Ekosisteme (Mini Web Uygulaması)

## 1. Proje Vizyonu (Executive Summary)
**Sudan Ekosisteme**, tüketicilerin satın aldığı ürünlerin arkasındaki "görünmez su" (sanal su ayak izi) maliyetini görünür kılan bir farkındalık platformudur. Uygulama, kuru rakamlar yerine, kullanıcının tüketim tercihlerine göre anlık olarak değişen (yeşeren veya kuruyan) **interaktif bir dijital ekosistem** simülasyonu sunar.

## 2. Hedef Kitle
* **Bilinçli Tüketiciler:** Günlük tercihlerinin ekolojik etkisini merak eden Z ve Y kuşağı.
* **Eğitim ve Farkındalık:** Okullar veya çevre toplulukları için interaktif bir öğrenme aracı.
* **Sürdürülebilir Markalar:** Düşük su ayak izine sahip ürünlerini "alternatif" olarak sunmak isteyen yeşil girişimler.

## 3. Kullanıcı Hikayeleri (User Stories)
1. **Keşif:** Bir kullanıcı olarak, içtiğim bir bardak kahvenin doğada kaç litre suya mal olduğunu basit bir aramayla görmek istiyorum.
2. **Görsel Etki:** Bir kullanıcı olarak, yüksek su tüketen bir ürün seçtiğimde ekrandaki doğanın kuruduğunu görerek duygusal bir bağ kurmak istiyorum.
3. **Değişim:** Bir kullanıcı olarak, sistemin bana sunduğu daha çevreci alternatiflere tıklayarak ekosistemimi anında nasıl kurtarabileceğimi deneyimlemek istiyorum.

## 4. Fonksiyonel Gereksinimler (MVP Scope)

### 4.1. Arama ve Veri Eşleştirme
* Kullanıcı metin girişi yapabilmelidir (Örn: "Kot Pantolon", "Dana Eti").
* Sistem, girilen anahtar kelimeyi yerel bir veri tabanında (JSON) aramalı ve karşılık gelen litre değerini dönmelidir.

### 4.2. Dinamik Ekosistem Görselleştirmesi
* **Durum A (Kritik):** Su ayak izi > 1000L ise ekosistem görseli "kurak/çatlamış toprak" moduna geçmelidir.
* **Durum B (Orta):** 100L < Su ayak izi < 1000L ise ekosistem "sararmış/bozkır" moduna geçmelidir.
* **Durum C (İyi):** Su ayak izi < 100L ise ekosistem "yeşil/sulak/canlı" moduna geçmelidir.

### 4.3. Alternatif Öneri Motoru
* Yüksek su ayak izine sahip her ürün için en az bir adet düşük su ayak izli alternatif sunulmalıdır.
* Alternatife tıklandığında ekosistem görseli pozitif yönde güncellenmelidir.

## 5. Teknik Gereksinimler & Stack

| Katman | Teknoloji Önerisi | Neden? |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) | Hızlı yüklenme ve kolay kurulum için. |
| **Backend** | Python (Flask veya FastAPI) | Hafif yapı ve kolay veri işleme kapasitesi. |
| **Veritabanı** | JSON File | Başlangıç aşamasında (MVP) hız ve taşınabilirlik sağlar. |
| **Editör** | Cursor AI | Kod yazım hızını artırmak ve AI yardımıyla hata ayıklamak için. |

## 6. Kullanıcı Akış Diyagramı (User Flow)
1. **Giriş:** Sade bir ana sayfa ve arama kutusu.
2. **Sorgu:** Kullanıcı ürünü yazar ve "Hesapla"ya basar.
3. **Sonuç:** Ekranda litre bazında veri ve değişen ekosistem animasyonu belirir.
4. **Öneri:** Ekranın altında "Bunu değil, şunu dene" butonu çıkar.
5. **Dönüşüm:** Alternatife basıldığında ekosistem yeşerir ve "Teşekkürler, X litre su kurtarıldı!" mesajı görünür.

## 7. Başarı Metrikleri
* Kullanıcının sitede geçirdiği ortalama süre (etkileşim oranı).
* "Alternatifi Dene" butonuna tıklanma oranı (dönüşüm oranı).
* Sosyal medyada paylaşılan "Ekosistem Durumu" ekran görüntüsü sayısı.

## 8. Gelecek Planları (Roadmap)
* **V2:** Yapay zeka ile fotoğraf üzerinden ürün tanıma (Image Recognition).
* **V3:** Kullanıcının kendi dijital bahçesini oluşturup kaydedebildiği bir üyelik sistemi.
* **V4:** Gerçek zamanlı coğrafi su stresi verilerinin API ile entegre edilmesi.