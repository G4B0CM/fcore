import bcrypt
from src.application.ports.output.i_password_hasher import IPasswordHasher

class BcryptPasswordHasher(IPasswordHasher):
    def hash_password(self, unhashed_password: str) -> str:
        # 1. Codificamos el password de str a bytes
        password_bytes = unhashed_password.encode('utf-8')
        
        # 2. Generamos el hash (que también es de tipo bytes)
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        # 3. Decodificamos el resultado de bytes a str para cumplir con la interfaz
        return hashed_bytes.decode('utf-8')
    
    def verify_password(self, plain_password: str, hash: str) -> bool:
        # 1. Codificamos la contraseña en texto plano de str a bytes
        plain_password_bytes = plain_password.encode('utf-8')
        
        # 2. Codificamos el hash (que viene como str de la DB) a bytes
        hash_bytes = hash.encode('utf-8')
        
        # 3. bcrypt.checkpw hace la comparación
        return bcrypt.checkpw(plain_password_bytes, hash_bytes)
            