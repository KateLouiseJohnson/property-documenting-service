from pydantic import BaseModel

class Address(BaseModel):
    street: str
    streetNumber: str

class Property(BaseModel):
    address: Address