from modules.application.common.types import PaginationParams
from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentNotFoundError, CommentTaskNotFoundError
from modules.comment.types import (
    CommentErrorCode,
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentService(BaseTestComment):
    def setUp(self) -> None:
        super().setUp()
        self.account = self.create_test_account()
        self.task = self.create_test_task(account_id=self.account.id)

    def test_create_comment_success(self) -> None:
        comment_params = CreateCommentParams(
            account_id=self.account.id, task_id=self.task.id, content=self.DEFAULT_COMMENT_CONTENT
        )

        comment = CommentService.create_comment(params=comment_params)

        assert comment.account_id == self.account.id
        assert comment.task_id == self.task.id
        assert comment.content == self.DEFAULT_COMMENT_CONTENT
        assert comment.id is not None
        assert comment.created_at is not None
        assert comment.updated_at is not None

    def test_create_comment_task_not_found(self) -> None:
        non_existent_task_id = "507f1f77bcf86cd799439011"
        comment_params = CreateCommentParams(
            account_id=self.account.id, task_id=non_existent_task_id, content=self.DEFAULT_COMMENT_CONTENT
        )

        with self.assertRaises(CommentTaskNotFoundError) as context:
            CommentService.create_comment(params=comment_params)

        assert context.exception.code == CommentErrorCode.TASK_NOT_FOUND

    def test_create_comment_cross_account_task(self) -> None:
        # Create another account and task
        other_account = self.create_test_account(username="other@example.com")
        other_task = self.create_test_task(account_id=other_account.id)

        comment_params = CreateCommentParams(
            account_id=self.account.id,  # Using original account
            task_id=other_task.id,  # But other account's task
            content=self.DEFAULT_COMMENT_CONTENT,
        )

        with self.assertRaises(CommentTaskNotFoundError) as context:
            CommentService.create_comment(params=comment_params)

        assert context.exception.code == CommentErrorCode.TASK_NOT_FOUND

    def test_get_comment_success(self) -> None:
        created_comment = self.create_test_comment(account_id=self.account.id, task_id=self.task.id)

        get_params = GetCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id)

        retrieved_comment = CommentService.get_comment(params=get_params)

        assert retrieved_comment.id == created_comment.id
        assert retrieved_comment.account_id == self.account.id
        assert retrieved_comment.task_id == self.task.id
        assert retrieved_comment.content == self.DEFAULT_COMMENT_CONTENT

    def test_get_comment_not_found(self) -> None:
        non_existent_comment_id = "507f1f77bcf86cd799439011"
        get_params = GetCommentParams(
            account_id=self.account.id, task_id=self.task.id, comment_id=non_existent_comment_id
        )

        with self.assertRaises(CommentNotFoundError) as context:
            CommentService.get_comment(params=get_params)

        assert context.exception.code == CommentErrorCode.NOT_FOUND

    def test_get_comment_task_not_found(self) -> None:
        created_comment = self.create_test_comment(account_id=self.account.id, task_id=self.task.id)

        non_existent_task_id = "507f1f77bcf86cd799439011"
        get_params = GetCommentParams(
            account_id=self.account.id, task_id=non_existent_task_id, comment_id=created_comment.id
        )

        with self.assertRaises(CommentTaskNotFoundError) as context:
            CommentService.get_comment(params=get_params)

        assert context.exception.code == CommentErrorCode.TASK_NOT_FOUND

    def test_get_paginated_comments_success(self) -> None:
        # Create multiple comments
        created_comments = self.create_multiple_test_comments(account_id=self.account.id, task_id=self.task.id, count=5)

        pagination_params = PaginationParams(page=1, size=3, offset=0)
        get_params = GetPaginatedCommentsParams(
            account_id=self.account.id, task_id=self.task.id, pagination_params=pagination_params
        )

        result = CommentService.get_paginated_comments(params=get_params)

        assert len(result.items) == 3
        assert result.total_count == 5
        assert result.pagination_params.page == 1
        assert result.pagination_params.size == 3

    def test_get_paginated_comments_empty_result(self) -> None:
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        get_params = GetPaginatedCommentsParams(
            account_id=self.account.id, task_id=self.task.id, pagination_params=pagination_params
        )

        result = CommentService.get_paginated_comments(params=get_params)

        assert len(result.items) == 0
        assert result.total_count == 0

    def test_get_paginated_comments_task_not_found(self) -> None:
        non_existent_task_id = "507f1f77bcf86cd799439011"
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        get_params = GetPaginatedCommentsParams(
            account_id=self.account.id, task_id=non_existent_task_id, pagination_params=pagination_params
        )

        with self.assertRaises(CommentTaskNotFoundError) as context:
            CommentService.get_paginated_comments(params=get_params)

        assert context.exception.code == CommentErrorCode.TASK_NOT_FOUND

    def test_update_comment_success(self) -> None:
        created_comment = self.create_test_comment(account_id=self.account.id, task_id=self.task.id)

        new_content = "Updated comment content"
        update_params = UpdateCommentParams(
            account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id, content=new_content
        )

        updated_comment = CommentService.update_comment(params=update_params)

        assert updated_comment.id == created_comment.id
        assert updated_comment.content == new_content
        assert updated_comment.updated_at > created_comment.updated_at

    def test_update_comment_not_found(self) -> None:
        non_existent_comment_id = "507f1f77bcf86cd799439011"
        update_params = UpdateCommentParams(
            account_id=self.account.id,
            task_id=self.task.id,
            comment_id=non_existent_comment_id,
            content="Updated content",
        )

        with self.assertRaises(CommentNotFoundError) as context:
            CommentService.update_comment(params=update_params)

        assert context.exception.code == CommentErrorCode.NOT_FOUND

    def test_update_comment_task_not_found(self) -> None:
        created_comment = self.create_test_comment(account_id=self.account.id, task_id=self.task.id)

        non_existent_task_id = "507f1f77bcf86cd799439011"
        update_params = UpdateCommentParams(
            account_id=self.account.id,
            task_id=non_existent_task_id,
            comment_id=created_comment.id,
            content="Updated content",
        )

        with self.assertRaises(CommentTaskNotFoundError) as context:
            CommentService.update_comment(params=update_params)

        assert context.exception.code == CommentErrorCode.TASK_NOT_FOUND

    def test_delete_comment_success(self) -> None:
        created_comment = self.create_test_comment(account_id=self.account.id, task_id=self.task.id)

        delete_params = DeleteCommentParams(
            account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id
        )

        result = CommentService.delete_comment(params=delete_params)

        assert result.comment_id == created_comment.id
        assert result.success is True
        assert result.deleted_at is not None

        # Verify comment is actually deleted
        get_params = GetCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id)

        with self.assertRaises(CommentNotFoundError):
            CommentService.get_comment(params=get_params)

    def test_delete_comment_not_found(self) -> None:
        non_existent_comment_id = "507f1f77bcf86cd799439011"
        delete_params = DeleteCommentParams(
            account_id=self.account.id, task_id=self.task.id, comment_id=non_existent_comment_id
        )

        with self.assertRaises(CommentNotFoundError) as context:
            CommentService.delete_comment(params=delete_params)

        assert context.exception.code == CommentErrorCode.NOT_FOUND

    def test_delete_comment_task_not_found(self) -> None:
        created_comment = self.create_test_comment(account_id=self.account.id, task_id=self.task.id)

        non_existent_task_id = "507f1f77bcf86cd799439011"
        delete_params = DeleteCommentParams(
            account_id=self.account.id, task_id=non_existent_task_id, comment_id=created_comment.id
        )

        with self.assertRaises(CommentTaskNotFoundError) as context:
            CommentService.delete_comment(params=delete_params)

        assert context.exception.code == CommentErrorCode.TASK_NOT_FOUND
