from fastapi import FastAPI
import uvicorn

# Kendi dosyalarından yaptığın importlar
from database import Base, engine
from models.user import User
from models.ticket import Ticket
from routes.auth import router as auth_router
from routes.ticket import router as ticket_router

# 1. Veritabanı tablolarını oluştur (Modeller import edildikten sonra olmalı)
print("--- [SISTEM] Veritabanı tabloları kontrol ediliyor... ---")
Base.metadata.create_all(bind=engine)

# 2. FastAPI uygulamasını başlat
app = FastAPI(title="Ticket System")

# 3. Router'ları sisteme dahil et
app.include_router(auth_router)
app.include_router(ticket_router)

# 4. Ana sayfa (Çalışıp çalışmadığını anlamak için)
@app.get("/")
def root():
    return {"status": "Sistem Aktif", "message": "API 8000 portunda hazir!"}

# Eğer dosyayı direkt python ile çalıştırırsan diye:
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)