from jose import JWTError,jwt
from datetime import datetime,timedelta
import schemas
from fastapi import status,HTTPException , Depends
from fastapi.security import OAuth2PasswordBearer
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data : dict):
    to_encode = data.copy()
    expird = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expird})
    encode_jwt = jwt.encode(to_encode,algorithm=ALGORITHM,key=SECRET_KEY)
    return encode_jwt

def verify_access_token(token: str, cred_except):
    try:
        payload = jwt.decode(token, key=SECRET_KEY)
        id: int = payload.get("user_id")
        if not id:
            raise cred_except
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise cred_except
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, credentials_exception)
    return token_data



