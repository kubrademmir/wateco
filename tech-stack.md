# Teknoloji Yığını (Tech Stack): Sudan Ekosisteme

Bu projede başlangıç seviyesine en uygun, karmaşık kurulum gerektirmeyen ve doğrudan sonuca götüren "Modern & Minimal" bir mimari kullanıyoruz.

## 1. Backend (Arka Plan ve Mantık): Python + Flask
* **Neden Seçtik?** Python, kod dizilimi İngilizce okur gibi olan en kolay programlama dilidir. Flask ise Python'un "mikro" web kütüphanesidir. Karmaşık ayarlar istemez; sadece 5-10 satır kodla bir web sitesini ayağa kaldırabilirsin.
* **Ne İşe Yarayacak?** Kullanıcının arayüzden gönderdiği kelimeyi (örn: "Kahve") alacak, Gemini API'ye gönderecek ve oradan gelen sonucu tekrar ön yüze iletecek köprü görevini görecek.

## 2. Yapay Zeka (AI): Google Gemini API
* **Neden Seçtik?** Sabit bir veri tabanı (JSON dosyası) hazırlamak yerine, Gemini'ın devasa bilgi birikimini kullanacağız. Çok hızlıdır ve doğrudan Python üzerinden tek bir kütüphane ile çalışır.
* **Ne İşe Yarayacak?** Kullanıcı "1 kg sığır eti" yazdığında, Gemini bunu analiz edip bize şu yanıtı verecek: *"Su ayak izi: 15.000 Litre. Durum: Kritik. Alternatif: Tavuk (4.300 Litre)."* Yani projenin "beyni" olacak.

## 3. Frontend (Kullanıcı Arayüzü): HTML + Tailwind CSS + Vanilla JS
* **Neden Seçtik?** React veya Vue gibi öğrenmesi aylar süren karmaşık sistemler yerine işin temeline iniyoruz. Tailwind CSS, harici bir dosya yazmadan HTML içine kod yazarak (CDN üzerinden) çok modern ve şık tasarımlar (butonlar, arama çubuğu) yapmamızı sağlar.
* **Ne İşe Yarayacak?** Kullanıcının göreceği ekranı, arama çubuğunu ve su miktarına göre değişen o "kuruyan/yeşeren ekosistem" görselini oluşturacak.

---

## 🛠️ Kurulum Adımları (Terminal Komutları)

Cursor'ın alt kısmında bulunan Terminal (siyah komut ekranı) bölümünü açarak projeyi kodlamaya hazır hale getirmek için sırasıyla şu adımları uygulayacağız:

**1. Gerekli Kütüphaneleri İndirme:**
Terminal ekranına aşağıdaki komutu kopyalayıp Enter'a basarak Flask, Gemini API ve güvenlik (API anahtarını gizlemek için) paketlerini kur:
`pip install flask google-generativeai python-dotenv`

**2. Güvenlik Dosyasını Oluşturma (.env):**
Proje klasörünün içine `.env` adında yeni bir dosya oluştur (başında nokta olmak zorunda). İçine Google AI Studio'dan aldığın anahtarı şu şekilde yapıştır:
`GEMINI_API_KEY=senin_api_anahtarin_buraya_gelecek`

**3. Klasör Yapısını Kurma:**
Sol taraftaki dosya gezgininde şu yapıyı oluştur:
* 📄 `app.py` (Python kodlarımızı yazacağımız ana dosya)
* 📄 `.env` (API anahtarımızın olduğu gizli dosya)
* 📁 `templates` (Adında bir klasör oluştur)
  * 📄 `index.html` (Bu klasörün içine sitenin ön yüz dosyasını oluştur)