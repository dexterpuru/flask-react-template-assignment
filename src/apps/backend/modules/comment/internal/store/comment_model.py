from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson import ObjectId

from modules.application.base_model import BaseModel


@dataclass
class CommentModel(BaseModel):
    task_id: str
    account_id: str
    content: str
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    id: Optional[ObjectId | str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    @classmethod
    def from_bson(cls, bson_data: dict) -> "CommentModel":
        return cls(
            task_id=bson_data.get("task_id", ""),
            account_id=bson_data.get("account_id", ""),
            content=bson_data.get("content", ""),
            active=bson_data.get("active", True),
            created_at=bson_data.get("created_at"),
            updated_at=bson_data.get("updated_at"),
            id=bson_data.get("_id"),
        )

    @staticmethod
    def get_collection_name() -> str:
        return "comments"
