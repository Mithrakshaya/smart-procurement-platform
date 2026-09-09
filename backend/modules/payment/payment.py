from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    payment_id: str
    procurement_id: str
    farmer_id: str
    amount: float
    payment_method: str
    status: str
    transaction_id: str | None
    created_at: str
    paid_at: str | None

    @classmethod
    def create(
        cls,
        payment_id: str,
        procurement_id: str,
        farmer_id: str,
        amount: float,
        payment_method: str = "BANK_TRANSFER",
    ):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than 0")

        if not procurement_id.strip():
            raise ValueError("Procurement ID is required")

        if not farmer_id.strip():
            raise ValueError("Farmer ID is required")

        return cls(
            payment_id=payment_id,
            procurement_id=procurement_id,
            farmer_id=farmer_id,
            amount=amount,
            payment_method=payment_method,
            status="PENDING",
            transaction_id=None,
            created_at=datetime.now().isoformat(),
            paid_at=None,
        )

    def process_payment(self, transaction_id: str):
        if self.status != "PENDING":
            raise ValueError("Only pending payments can be processed")

        if not transaction_id.strip():
            raise ValueError("Transaction ID is required")

        self.transaction_id = transaction_id
        self.status = "PAID"
        self.paid_at = datetime.now().isoformat()

    def fail_payment(self):
        if self.status != "PENDING":
            raise ValueError("Only pending payments can be marked as failed")

        self.status = "FAILED"