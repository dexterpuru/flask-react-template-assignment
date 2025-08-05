from modules.application.errors import AppError
from modules.comment.types import CommentErrorCode


class CommentNotFoundError(AppError):
    def __init__(self, message: str = "Comment not found"):
        super().__init__(message=message, code=CommentErrorCode.NOT_FOUND, http_status_code=404)


class CommentBadRequestError(AppError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, code=CommentErrorCode.BAD_REQUEST, http_status_code=400)


class CommentTaskNotFoundError(AppError):
    def __init__(self, message: str = "Task not found for comment"):
        super().__init__(message=message, code=CommentErrorCode.TASK_NOT_FOUND, http_status_code=404)
