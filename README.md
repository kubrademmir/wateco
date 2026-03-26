# Sudan Ekosisteme (MVP)

Tükettiğimiz ürünlerin **sanal su ayak izini** (litre) görünür kılan mini web uygulaması.

## Klasör yapısı

- `backend/`: Flask API
- `data/`: Ürün verisi (`products.json`)
- `frontend/`: HTML/CSS/JS arayüz

## Kurulum (Windows / PowerShell)

Proje kök dizininde:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Çalıştırma

Backend’i başlat:

```powershell
python .\backend\app.py
```

Sonra tarayıcıdan aç:

- `http://127.0.0.1:5000`

## API

- `GET /api/search?q=kahve`
