from typing import Any

from bson import ObjectId

from modules.comment.errors import CommentTaskNotFoundError
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.types import Comment
from modules.task.errors import TaskNotFoundError
from modules.task.task_service import TaskService
from modules.task.types import GetTaskParams


class CommentUtil:
    @staticmethod
    def validate_task_exists(*, account_id: str, task_id: str) -> bool:
        """
        Validate that a task exists and belongs to the account
        """
        try:
            TaskService.get_task(params=GetTaskParams(account_id=account_id, task_id=task_id))
            return True
        except TaskNotFoundError:
            raise CommentTaskNotFoundError(f"Task with id {task_id} not found")

    @staticmethod
    def validate_object_id(*, object_id: str) -> bool:
        """
        Validate that a string is a valid MongoDB ObjectId
        """
        try:
            ObjectId(object_id)
            return True
        except Exception:
            return False

    @staticmethod
    def convert_bson_to_model(comment_bson: dict[str, Any]) -> Comment:
        validated_comment_data = CommentModel.from_bson(comment_bson)
        return CommentModel(
            task_id=validated_comment_data.task_id,
            account_id=validated_comment_data.account_id,
            content=validated_comment_data.content,
            active=validated_comment_data.active,
            created_at=validated_comment_data.created_at,
            updated_at=validated_comment_data.updated_at,
            id=str(validated_comment_data.id),
        )
