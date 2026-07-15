from pydantic import BaseModel,EmailStr,Field , ConfigDict
import uuid


## Auth Schemas for data validation
class UserRegisterRequest(BaseModel):
    """
    Contract for incoming data. 
    Enforces that email must be valid and password has a minimum length.
    """

    email : EmailStr
    password : str = Field(..., min_length = 8, max_length = 100)


class UserResponse(BaseModel):
    """
    Contract for outgoing data
    Ensure that we never leak password or password hash back to the client
    """
    id: uuid.UUID
    email : EmailStr

    # Modern Pydantic V2 Configuration syntax
    model_config = ConfigDict(from_attributes = True)
