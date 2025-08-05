from bson import ObjectId
from pymongo import DESCENDING

from modules.application.common.types import PaginationResult
from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import Comment, GetCommentParams, GetPaginatedCommentsParams


class CommentReader:
    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        collection = CommentRepository.collection()

        comment_doc = collection.find_one(
            {
                "_id": ObjectId(params.comment_id),
                "task_id": params.task_id,
                "account_id": params.account_id,
                "active": True,
            }
        )

        if not comment_doc:
            raise CommentNotFoundError(f"Comment with id {params.comment_id} not found")

        comment_model = CommentModel.from_bson(comment_doc)
        return Comment(
            id=str(comment_model.id),
            task_id=comment_model.task_id,
            account_id=comment_model.account_id,
            content=comment_model.content,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    @staticmethod
    def get_paginated_comments(*, params: GetPaginatedCommentsParams) -> PaginationResult[Comment]:
        collection = CommentRepository.collection()

        query = {"task_id": params.task_id, "account_id": params.account_id, "active": True}

        # Calculate offset
        offset = (params.pagination_params.page - 1) * params.pagination_params.size

        # Get total count
        total_count = collection.count_documents(query)

        # Get paginated results
        cursor = collection.find(query).sort("created_at", DESCENDING).skip(offset).limit(params.pagination_params.size)

        comments = []
        for comment_doc in cursor:
            comment_model = CommentModel.from_bson(comment_doc)
            comments.append(
                Comment(
                    id=str(comment_model.id),
                    task_id=comment_model.task_id,
                    account_id=comment_model.account_id,
                    content=comment_model.content,
                    created_at=comment_model.created_at,
                    updated_at=comment_model.updated_at,
                )
            )

        return PaginationResult(
            items=comments, total=total_count, page=params.pagination_params.page, size=params.pagination_params.size
        )
