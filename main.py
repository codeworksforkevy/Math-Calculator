from fastapi import FastAPI, HTTPException
import math
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
