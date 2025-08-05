from bson import ObjectId

from modules.comment.errors import CommentTaskNotFoundError
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
