from dataclasses import dataclass
from datetime import datetime


@dataclass
class Procurement:
    procurement_id: str
    farmer_id: str
    crop_name: str
    quantity_kg: float
    quality_grade: str
    price_per_kg: float
    total_amount: float
    centre_id: str
    status: str
    created_at: str

    @classmethod
    def create(
        cls,
        procurement_id: str,
        farmer_id: str,
        crop_name: str,
        quantity_kg: float,
        quality_grade: str,
        price_per_kg: float,
        centre_id: str,
    ):
        if quantity_kg <= 0:
            raise ValueError("Quantity must be greater than 0")

        if price_per_kg < 0:
            raise ValueError("Price cannot be negative")

        if not crop_name.strip():
            raise ValueError("Crop name is required")

        if not farmer_id.strip():
            raise ValueError("Farmer ID is required")

        total_amount = quantity_kg * price_per_kg

        return cls(
            procurement_id=procurement_id,
            farmer_id=farmer_id,
            crop_name=crop_name,
            quantity_kg=quantity_kg,
            quality_grade=quality_grade,
            price_per_kg=price_per_kg,
            total_amount=total_amount,
            centre_id=centre_id,
            status="PENDING",
            created_at=datetime.now().isoformat(),
        )

    def approve(self):
        self.status = "APPROVED"

    def reject(self):
        self.status = "REJECTED"

    def complete(self):
        if self.status != "APPROVED":
            raise ValueError("Procurement must be approved before completion")

        self.status = "COMPLETED"