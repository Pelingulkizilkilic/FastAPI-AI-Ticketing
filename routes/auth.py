from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from models.user import User
from services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    decode_token
)

# --- VERİ MODELLERİ (PYDANTIC) ---
class UserAuthSchema(BaseModel):
    username: str
    password: str

# --- BAĞIMLILIKLAR (DEPENDENCIES) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Token içeriği hatalı")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
    return user

# --- ROUTER TANIMI ---
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    # Veriler artık URL'den değil, JSON Body'den geliyor
    print("\n>>> KAYIT ISTEGI SUNUCUYA ULASTI! <<<\n") # Bunu ekle
    user = create_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=409, detail="Bu kullanıcı adı zaten alınmış")
    return {"message": "Kullanıcı başarıyla oluşturuldu"}

@router.post("/login")
def login(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı")
    
    token = create_access_token({
        "sub": user.username,
        "user_id": user.id,
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }