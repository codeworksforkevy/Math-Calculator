import os
import math
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI(title="Kimya ve Matematik İçin Çalışmayı Sevme Planlarım")

current_dir   = os.path.dirname(os.path.realpath(__file__))
static_path   = os.path.join(current_dir, "static ")
templates_path = os.path.join(current_dir, "templates ")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hesapla/ph")
def get_ph(h_derisimi: float):
    if h_derisimi <= 0:
        raise HTTPException(400, detail="Derişim 0'dan büyük olmalıdır.")
    return {"sonuc": round(-math.log10(h_derisimi), 4)}


@app.get("/hesapla/zayif_asit")
def zayif_asit_ph(ka: float, derisim: float):
    if ka <= 0 or derisim <= 0:
        raise HTTPException(400, detail="Ka ve derişim 0'dan büyük olmalıdır.")
    delta = ka**2 + 4 * ka * derisim
    h = (-ka + math.sqrt(delta)) / 2
    if h <= 0:
        raise HTTPException(400, detail="Geçersiz değerler.")
    ph_hassas  = -math.log10(h)
    ph_yaklasik = -math.log10(math.sqrt(ka * derisim))
    return {
        "h_derisimi": round(h, 8),
        "ph_hassas": round(ph_hassas, 4),
        "ph_yaklasik": round(ph_yaklasik, 4),
        "iyonlasma_yuzdesi": round((h / derisim) * 100, 2),
    }


@app.get("/hesapla/mol")
def mol_hesapla(kutle: float, ma: float):
    if ma <= 0:
        raise HTTPException(400, detail="Mol kütlesi 0'dan büyük olmalıdır.")
    return {"sonuc": round(kutle / ma, 6)}


@app.get("/hesapla/hiz")
def hiz_problemi(
    yol: Optional[float] = None,
    hiz: Optional[float] = None,
    zaman: Optional[float] = None,
):
    try:
        if yol is None:   return {"sonuc": round(hiz * zaman, 4), "birim": "birim mesafe"}
        if hiz is None:   return {"sonuc": round(yol / zaman, 4), "birim": "birim hız"}
        if zaman is None: return {"sonuc": round(yol / hiz, 4),  "birim": "birim zaman"}
    except (ZeroDivisionError, TypeError):
        raise HTTPException(400, detail="Sıfıra bölme veya eksik değer hatası!")


@app.get("/hesapla/denklem")
def denklem_coz(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float):
    det = a1 * b2 - a2 * b1
    if det == 0:
        return {"hata": "Sistem çözümsüz veya sonsuz çözümlü (det=0)."}
    return {
        "x": round((c1 * b2 - c2 * b1) / det, 6),
        "y": round((a1 * c2 - a2 * c1) / det, 6),
    }


@app.get("/hesapla/ustel")
def ustel_hesapla(taban: float, us: float):
    try:
        return {"sonuc": round(taban ** us, 6)}
    except Exception:
        raise HTTPException(400, detail="Geçersiz değerler.")


@app.get("/hesapla/isci")
def isci_hesapla(kapasite_liste: str):
    try:
        sureler = [float(x.strip()) for x in kapasite_liste.split(",") if x.strip()]
        if not sureler or any(s <= 0 for s in sureler):
            raise ValueError
        return {"sonuc": round(1 / sum(1 / s for s in sureler), 4), "birim": "saat"}
    except ValueError:
        raise HTTPException(400, detail="Geçerli pozitif sayılar girin.")
