from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
import email_validator

class UserCreate(BaseModel):   # Create schema of request body using pydantic model.
    email: EmailStr           
    password : str

class UserResponse(BaseModel):   # Create schema of request body using pydantic model.
    id: int
    email: str           

class postBaseClass(BaseModel):   # Create schema of request body using pydantic model.
    # id : Optional[int] = None
    title: str            
    content : str
    published : bool = True   


class updateClass(BaseModel):   # Create schema of request body using pydantic model.
    model_config = ConfigDict(extra='forbid')  # To send error if any additional field is passed in request.
    title: str            
    content : str


class updateResponse(BaseModel):   # Create schema of request body using pydantic model.
    id: int
    title: str            
    content : str
    published : bool = True     
    user_id : int  
    owner : UserResponse

class postResponse(BaseModel):   # Create schema of request body using pydantic model.
    id: int
    title: str            
    content : str
    published : bool = True     
    created_at : str
    user_id : str
    vote: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id: Optional[str] = None


class votingData(BaseModel):
    post_id : int
    dir : Optional[int] = 1


class votingDataResponse(BaseModel):
    post_id : int
    user_id : int


# class voterOnPost(BaseModel):    
#     user_id : int


class UserInfo(BaseModel):       
    email: str

class voterOnPost(BaseModel):    
    # user_id : int
    userInfo : UserInfo 


class additionInfo(BaseModel):
    user_mode : bool = True
    comments : str
    remarks: str
    post: updateResponse