from pydantic import BaseModel, Field, EmailStr, ConfigDict

class ORMBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    email: EmailStr
    name: str


class UserGetSchema(ORMBaseSchema, UserSchema):
    id: int