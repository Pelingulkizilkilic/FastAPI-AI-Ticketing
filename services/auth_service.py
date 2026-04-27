from sqlalchemy.orm import Session
from models.user import User
from services.security import hash_password, verify_password
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# Ayarlar
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔥 KULLANICI OLUŞTURMA (Loglamalı ve Hata Yakalamalı)
def create_user(db: Session, username: str, password: str):
    try:
        print(f"\n--- [DEBUG] Kayıt İşlemi Başladı: {username} ---")
        
        # 1. Kullanıcı var mı kontrolü
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print("--- [DEBUG] Hata: Bu kullanıcı adı zaten veritabanında var.")
            return None

        # 2. Şifreleme aşaması (En çok hata burada çıkar)
        print("--- [DEBUG] Şifre hash'leniyor...")
        hashed = hash_password(password)
        print("--- [DEBUG] Şifre başarıyla hash'lendi.")

        # 3. Veritabanına kayıt
        new_user = User(
            username=username,
            password=hashed,
            role="user"
        )

        print("--- [DEBUG] Veritabanına ekleniyor...")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"--- [DEBUG] Başarılı: {username} kaydedildi! ID: {new_user.id} ---")
        return new_user

    except Exception as e:
        db.rollback()
        print("\n!!! [KRİTİK HATA] create_user fonksiyonunda patlama yaşandı !!!")
        print(f"!!! Hata Tipi: {type(e).__name__}")
        print(f"!!! Hata Mesajı: {str(e)}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        raise e

# 🔥 KİMLİK DOĞRULAMA
def authenticate_user(db: Session, username: str, password: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user
    except Exception as e:
        print(f"--- [DEBUG] Login Hatası: {e}")
        return None

# 🔥 ACCESS TOKEN ÜRETME
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 🔥 TOKEN ÇÖZME
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None