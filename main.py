from fastapi import FastAPI, HTTPException
import math
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import math
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import math
# --- PROBLEM ÇÖZÜCÜ MODÜLÜ ---

@app.get("/api/hiz_problemi")
def hesapla_hiz(yol: float = None, hiz: float = None, zaman: float = None):
    """x = v * t formülüne göre eksik olanı bulur."""
    if yol is None: return {"sonuc": round(hiz * zaman, 2), "birim": "metre/km"}
    if hiz is None: return {"sonuc": round(yol / zaman, 2), "birim": "hız (v)"}
    if zaman is None: return {"sonuc": round(yol / hiz, 2), "birim": "saat/sn"}

@app.get("/api/isci_problemi")
def hesapla_isci(kapasite_liste: str):
    """
    İşçi/Havuz Problemi: 1/t1 + 1/t2 = 1/Toplam
    Girdi örneği: "3,6" (Bir işçi 3, diğeri 6 saatte bitiriyor)
    """
    try:
        times = [float(x) for x in kapasite_liste.split(",")]
        toplam_kapasite = sum(1/t for t in times)
        return {"sonuc": round(1 / toplam_kapasite, 2), "birim": "saat"}
    except:
        return {"sonuc": "Hata: Geçersiz giriş"}

app = FastAPI(title="Linguist's Lab: Academic Engine")

# Statik dosyalar ve şablonlar
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- HESAPLAMA MOTORU ---

@app.get("/api/ph")
def hesapla_ph(h: float):
    if h <= 0: return {"sonuc": "Hata: Derişim > 0 olmalı"}
    return {"sonuc": round(-math.log10(h), 2)}

@app.get("/api/ustel")
def hesapla_ustel(a: float, x: float):
    try:
        return {"sonuc": round(math.pow(a, x), 4)}
    except:
        return {"sonuc": "Hata: Geçersiz işlem"}

@app.get("/api/denklem")
def coze_denklem(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float):
    det = (a1 * b2) - (a2 * b1)
    if det == 0: return {"sonuc": "Çözüm Yok (Paralel)"}
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return {"sonuc": f"x: {round(x,2)}, y: {round(y,2)}"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- GELİŞMİŞ MATEMATİK MODÜLÜ ---

@app.get("/hesapla/ustel")
def ustel_hesapla(taban: float, us: float):
    """f(x) = a^x hesaplaması"""
    return {"islem": "Üstel Fonksiyon", "sonuc": math.pow(taban, us)}

@app.get("/hesapla/denklem")
def denklem_coz(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float):
    """
    a1x + b1y = c1
    a2x + b2y = c2  sistemini çözer.
    """
    det = (a1 * b2) - (a2 * b1)
    if det == 0:
        return {"hata": "Sistemin tek bir çözümü yok (Paralel doğrular)."}
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return {"x": round(x, 2), "y": round(y, 2)}

# --- ANA SAYFA ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
import math

app = FastAPI()

# Statik ve Template klasörlerini tanıtıyoruz
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hesapla/ph")
def get_ph(h_derisimi: float):
    if h_derisimi <= 0: return {"sonuc": "Hata!"}
    return {"sonuc": round(-math.log10(h_derisimi), 2)}

# Diğer mol ve denklem fonksiyonlarını buraya eklemeye devam edebilirsin...

app = FastAPI(title="Linguist's Lab API", description="TYT-AYT Fen ve Matematik Hesaplayıcı")

# --- AKADEMİK VERİ MERKEZİ (Konu Anlatımları) ---
# Burada dilbilim hassasiyetiyle hazırlanmış metinler tutulur.
KAYNAKCA = {
    "ph_kuramlari": {
        "baslik": "Asit-Baz Kuramları (Tarihsel Gelişim)",
        "icerik": "Arrhenius (1884), Brønsted-Lowry (1923) ve Lewis (1923) kuramları temeldir...",
        "kaynak": "Harvard University - Dept. of Chemistry"
    },
    "turev_analiz": {
        "baslik": "Türev ve Değişim Oranı",
        "icerik": "Türev, bir fonksiyonun anlık değişim hızıdır. Geometrik olarak teğet eğimidir.",
        "kaynak": "MIT OpenCourseWare - Calculus I"
    }
}

# --- HESAPLAMA FONKSİYONLARI ---

@app.get("/hesapla/ph")
def get_ph(h_derisimi: float):
    """pH = -log10[H+] formülünü uygular."""
    if h_derisimi <= 0:
        raise HTTPException(status_code=400, detail="H iyonu derişimi pozitif olmalıdır.")
    ph_degeri = -math.log10(h_derisimi)
    return {"islem": "pH Hesaplama", "sonuc": round(ph_degeri, 2)}

@app.get("/hesapla/mol")
def get_mol(kutle: float, ma: float):
    """n = m / Ma formülünü uygular."""
    if ma <= 0:
        raise HTTPException(status_code=400, detail="Mol kütlesi (Ma) 0 olamaz.")
    mol = kutle / ma
    return {"islem": "Mol Hesaplama", "sonuc": round(mol, 4)}

@app.get("/konu/{konu_id}")
def get_konu_anlatimi(konu_id: str):
    """İstenen akademik konuyu getirir."""
    if konu_id not in KAYNAKCA:
        raise HTTPException(status_code=404, detail="Konu bulunamadı.")
    return KAYNAKCA[konu_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
