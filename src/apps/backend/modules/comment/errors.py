from modules.application.errors import BaseError
from modules.comment.types import CommentErrorCode


class CommentNotFoundError(BaseError):
    def __init__(self, message: str = "Comment not found"):
        super().__init__(message=message, error_code=CommentErrorCode.NOT_FOUND, status_code=404)


class CommentBadRequestError(BaseError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, error_code=CommentErrorCode.BAD_REQUEST, status_code=400)


class CommentTaskNotFoundError(BaseError):
    def __init__(self, message: str = "Task not found for comment"):
        super().__init__(message=message, error_code=CommentErrorCode.TASK_NOT_FOUND, status_code=404)
