from modules.application.common.types import PaginationResult
from modules.comment.internal.comment_reader import CommentReader
from modules.comment.internal.comment_util import CommentUtil
from modules.comment.internal.comment_writer import CommentWriter
from modules.comment.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)


class CommentService:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        # Validate that the task exists and belongs to the account
        CommentUtil.validate_task_exists(account_id=params.account_id, task_id=params.task_id)
        return CommentWriter.create_comment(params=params)

    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        # Validate that the task exists and belongs to the account
        CommentUtil.validate_task_exists(account_id=params.account_id, task_id=params.task_id)
        return CommentReader.get_comment(params=params)

    @staticmethod
    def get_paginated_comments(*, params: GetPaginatedCommentsParams) -> PaginationResult[Comment]:
        # Validate that the task exists and belongs to the account
        CommentUtil.validate_task_exists(account_id=params.account_id, task_id=params.task_id)
        return CommentReader.get_paginated_comments(params=params)

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        # Validate that the task exists and belongs to the account
        CommentUtil.validate_task_exists(account_id=params.account_id, task_id=params.task_id)
        return CommentWriter.update_comment(params=params)

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        # Validate that the task exists and belongs to the account
        CommentUtil.validate_task_exists(account_id=params.account_id, task_id=params.task_id)
        return CommentWriter.delete_comment(params=params)
