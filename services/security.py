import bcrypt

def hash_password(password: str) -> str:
    """
    Kullanıcının girdiği düz metin şifreyi güvenli bir şekilde hashler.
    """
    # 1. Şifreyi byte formatına çeviriyoruz (utf-8)
    password_bytes = password.encode('utf-8')
    
    # 2. Rastgele bir tuz (salt) oluşturuyoruz
    salt = bcrypt.gensalt()
    
    # 3. Şifreyi ve tuzu kullanarak hash oluşturuyoruz
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Veritabanına kaydedebilmek için sonucu tekrar string (metin) yapıyoruz
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Girilen şifre ile veritabanındaki hash'in eşleşip eşleşmediğini kontrol eder.
    """
    try:
        # Hem düz şifreyi hem de hashlenmiş şifreyi byte formatına çevirip kontrol ediyoruz
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        # Eğer bir format hatası olursa (geçersiz hash vb.) direkt False dön
        return False