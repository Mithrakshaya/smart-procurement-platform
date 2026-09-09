from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    notification_id: str
    farmer_id: str
    notification_type: str
    title: str
    message: str
    status: str
    created_at: str
    sent_at: str | None

    @classmethod
    def create(
        cls,
        notification_id: str,
        farmer_id: str,
        notification_type: str,
        title: str,
        message: str,
    ):
        if not farmer_id.strip():
            raise ValueError("Farmer ID is required")

        if not notification_type.strip():
            raise ValueError("Notification type is required")

        if not title.strip():
            raise ValueError("Notification title is required")

        if not message.strip():
            raise ValueError("Notification message is required")

        return cls(
            notification_id=notification_id,
            farmer_id=farmer_id,
            notification_type=notification_type,
            title=title,
            message=message,
            status="PENDING",
            created_at=datetime.now().isoformat(),
            sent_at=None,
        )

    def send(self):
        if self.status != "PENDING":
            raise ValueError("Only pending notifications can be sent")

        self.status = "SENT"
        self.sent_at = datetime.now().isoformat()

    def fail(self):
        if self.status != "PENDING":
            raise ValueError("Only pending notifications can be marked as failed")

        self.status = "FAILED"