from bson import ObjectId

from modules.application.common.base_model import BaseModel
from modules.application.common.types import PaginationResult
from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.comment_util import CommentUtil
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
        query = {"task_id": params.task_id, "account_id": params.account_id, "active": True}

        total_count = CommentRepository.collection().count_documents(query)

        pagination_params, skip, total_pages = BaseModel.calculate_pagination_values(
            params.pagination_params, total_count
        )

        cursor = CommentRepository.collection().find(query)

        if params.sort_params:
            cursor = BaseModel.apply_sort_params(cursor, params.sort_params)
        else:
            cursor = cursor.sort([("created_at", -1), ("_id", -1)])

        comments_bson = list(cursor.skip(skip).limit(pagination_params.size))

        comments = [CommentUtil.convert_bson_to_model(comment_bson) for comment_bson in comments_bson]

        return PaginationResult(
            items=comments, pagination_params=pagination_params, total_count=total_count, total_pages=total_pages
        )
