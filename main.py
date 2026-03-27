from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import math

app = FastAPI(title="Linguist's Lab: Academic Engine")

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- ACADEMIC DATA (Topic explanations) ---
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

# --- MAIN PAGE ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- CHEMISTRY ---
@app.get("/hesapla/ph")
def get_ph(h_derisimi: float):
    """pH = -log10[H+]"""
    if h_derisimi <= 0:
        raise HTTPException(status_code=400, detail="H iyonu derişimi pozitif olmalıdır.")
    return {"islem": "pH Hesaplama", "sonuc": round(-math.log10(h_derisimi), 2)}

@app.get("/hesapla/mol")
def get_mol(kutle: float, ma: float):
    """n = m / Ma"""
    if ma <= 0:
        raise HTTPException(status_code=400, detail="Mol kütlesi (Ma) 0 olamaz.")
    return {"islem": "Mol Hesaplama", "sonuc": round(kutle / ma, 4)}

# --- MATHEMATICS ---
@app.get("/hesapla/ustel")
def ustel_hesapla(taban: float, us: float):
    """f(x) = a^x"""
    try:
        return {"islem": "Üstel Fonksiyon", "sonuc": round(math.pow(taban, us), 4)}
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz işlem.")

@app.get("/hesapla/denklem")
def denklem_coz(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float):
    """
    Solves:
      a1x + b1y = c1
      a2x + b2y = c2
    """
    det = (a1 * b2) - (a2 * b1)
    if det == 0:
        return {"hata": "Sistemin tek bir çözümü yok (Paralel doğrular)."}
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return {"x": round(x, 2), "y": round(y, 2)}

# --- WORD PROBLEMS ---
@app.get("/hesapla/hiz")
def hiz_problemi(yol: float = None, hiz: float = None, zaman: float = None):
    """x = v * t — finds the missing variable."""
    try:
        if yol is None:
            return {"sonuc": round(hiz * zaman, 2), "birim": "metre/km"}
        if hiz is None:
            return {"sonuc": round(yol / zaman, 2), "birim": "hız (v)"}
        if zaman is None:
            return {"sonuc": round(yol / hiz, 2), "birim": "saat/sn"}
        raise HTTPException(status_code=400, detail="En az bir parametre boş bırakılmalıdır.")
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Sıfıra bölme hatası.")

@app.get("/hesapla/isci")
def isci_problemi(kapasite_liste: str):
    """
    Worker/Pool problem: 1/t1 + 1/t2 + ... = 1/T
    Example input: "3,6,12"
    """
    try:
        times = [float(x) for x in kapasite_liste.split(",")]
        toplam_kapasite = sum(1 / t for t in times)
        return {"sonuc": round(1 / toplam_kapasite, 2), "birim": "saat"}
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz giriş. Virgülle ayrılmış sayılar girin.")

# --- ACADEMIC CONTENT ---
@app.get("/konu/{konu_id}")
def get_konu(konu_id: str):
    if konu_id not in KAYNAKCA:
        raise HTTPException(status_code=404, detail="Konu bulunamadı.")
    return KAYNAKCA[konu_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
