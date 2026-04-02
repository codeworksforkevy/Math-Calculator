import os
import math
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Kimya ve Matematik İçin Çalışmayı Sevme Planlarım")

# Railway/Docker üzerinde klasör yollarını garantiye almak için:
current_dir = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(current_dir, "static")
templates_path = os.path.join(current_dir, "templates")

# Eğer klasörler yoksa hata almamak için mount işlemini dizin kontrolüyle yapıyoruz
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)

# --- GÜNCELLENMİŞ AKADEMİK VERİLER ---
KAYNAKCA = {
    "ph_logaritma": {
        "baslik": "pH ve Logaritma İlişkisi Özeti",
        "icerik": "pH, bir çözeltideki hidrojen iyonu (H+) aktivitesinin negatif logaritmasıdır (pH = -log[H+]). Logaritmik bir ölçek olduğu için, pH değerindeki 1 birimlik değişim, asitlikte 10 katlık bir değişime karşılık gelir. Örneğin; pH 4 olan bir sıvı, pH 5 olandan 10 kat daha asidiktir.",
        "kaynak": "Akademik Kimya Notları"
    },
    "ph_kuramlari": {
        "baslik": "Asit-Baz Kuramları",
        "icerik": "Arrhenius, Brønsted-Lowry ve Lewis kuramları modern kimyanın temelidir.",
        "kaynak": "Harvard University - Dept. of Chemistry"
    },
    "turev_analiz": {
        "baslik": "Türev ve Değişim Oranı",
        "icerik": "Türev, bir fonksiyonun anlık değişim hızıdır. Geometrik olarak teğet eğimidir.",
        "kaynak": "MIT OpenCourseWare"
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "kaynakca": KAYNAKCA})

@app.get("/hesapla/ph")
def get_ph(h_derisimi: float):
    if h_derisimi <= 0:
        raise HTTPException(status_code=400, detail="Derişim 0'dan büyük olmalıdır.")
    ph = -math.log10(h_derisimi)
    return {"sonuc": round(ph, 2)}

@app.get("/hesapla/hiz")
def hiz_problemi(yol: float = None, hiz: float = None, zaman: float = None):
    try:
        if yol is None: return {"sonuc": round(hiz * zaman, 2), "birim": "birim mesafe"}
        if hiz is None: return {"sonuc": round(yol / zaman, 2), "birim": "birim hız"}
        if zaman is None: return {"sonuc": round(yol / hiz, 2), "birim": "birim zaman"}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Sıfıra bölme hatası!")
