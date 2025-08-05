from datetime import datetime

from bson import ObjectId

from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    UpdateCommentParams,
)


class CommentWriter:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        collection = CommentRepository.collection()

        comment_model = CommentModel(
            task_id=params.task_id,
            account_id=params.account_id,
            content=params.content,
            active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        result = collection.insert_one(comment_model.to_bson())
        comment_model.id = result.inserted_id

        return Comment(
            id=str(comment_model.id),
            task_id=comment_model.task_id,
            account_id=comment_model.account_id,
            content=comment_model.content,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        collection = CommentRepository.collection()

        # First check if comment exists and belongs to the account/task
        existing_comment = collection.find_one(
            {
                "_id": ObjectId(params.comment_id),
                "task_id": params.task_id,
                "account_id": params.account_id,
                "active": True,
            }
        )

        if not existing_comment:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        # Update the comment
        updated_at = datetime.now()
        update_result = collection.update_one(
            {
                "_id": ObjectId(params.comment_id),
                "task_id": params.task_id,
                "account_id": params.account_id,
                "active": True,
            },
            {"$set": {"content": params.content, "updated_at": updated_at}},
        )

        if update_result.matched_count == 0:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        # Return updated comment
        updated_comment = collection.find_one({"_id": ObjectId(params.comment_id)})
        comment_model = CommentModel.from_bson(updated_comment)

        return Comment(
            id=str(comment_model.id),
            task_id=comment_model.task_id,
            account_id=comment_model.account_id,
            content=comment_model.content,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        collection = CommentRepository.collection()

        # Soft delete - set active to False
        deleted_at = datetime.now()
        update_result = collection.update_one(
            {
                "_id": ObjectId(params.comment_id),
                "task_id": params.task_id,
                "account_id": params.account_id,
                "active": True,
            },
            {"$set": {"active": False, "updated_at": deleted_at}},
        )

        if update_result.matched_count == 0:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        return CommentDeletionResult(comment_id=params.comment_id, deleted_at=deleted_at, success=True)
