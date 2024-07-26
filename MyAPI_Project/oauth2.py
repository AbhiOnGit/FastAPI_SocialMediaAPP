from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = "3435skdfkgkffk45dfdfd343535385039503kdfdlr"  # Any random string
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 65

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES

def create_Token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})             # To add expiration time along with payload in encrypted token

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def verify_Token(token:str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("email") 
        if id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return id

def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Could not verify.", headers={"WWW.Authenticate": "Bearer"})
    return verify_Token(token, credential_exception)


