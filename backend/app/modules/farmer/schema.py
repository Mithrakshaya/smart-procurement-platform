from pydantic import BaseModel


class FarmerCreate(BaseModel):
    name: str
    phone: str
    crop: str
    quantity: float
    location: str


class FarmerResponse(FarmerCreate):
    id: int
    status: str

    class Config:
        from_attributes = True