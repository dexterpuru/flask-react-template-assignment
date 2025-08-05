from dataclasses import asdict
from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.application.common.constants import DEFAULT_PAGINATION_PARAMS
from modules.application.common.types import PaginationParams
from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentBadRequestError
from modules.comment.internal.comment_util import CommentUtil
from modules.comment.types import (
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)


class CommentView(MethodView):
    @access_auth_middleware
    def post(self, account_id: str, task_id: str) -> ResponseReturnValue:
        """Create a new comment for a task"""
        request_data = request.get_json()

        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        if not request_data.get("content").strip():
            raise CommentBadRequestError("Content cannot be empty")

        # Validate task_id format
        if not CommentUtil.validate_object_id(object_id=task_id):
            raise CommentBadRequestError("Invalid task ID format")

        create_comment_params = CreateCommentParams(
            account_id=account_id, task_id=task_id, content=request_data["content"].strip()
        )

        created_comment = CommentService.create_comment(params=create_comment_params)
        comment_dict = asdict(created_comment)

        return jsonify(comment_dict), 201

    @access_auth_middleware
    def get(self, account_id: str, task_id: str, comment_id: Optional[str] = None) -> ResponseReturnValue:
        """Get comments for a task (paginated) or a specific comment"""
        # Validate task_id format
        if not CommentUtil.validate_object_id(object_id=task_id):
            raise CommentBadRequestError("Invalid task ID format")

        if comment_id:
            # Get specific comment
            if not CommentUtil.validate_object_id(object_id=comment_id):
                raise CommentBadRequestError("Invalid comment ID format")

            comment_params = GetCommentParams(account_id=account_id, task_id=task_id, comment_id=comment_id)
            comment = CommentService.get_comment(params=comment_params)
            comment_dict = asdict(comment)
            return jsonify(comment_dict), 200
        else:
            # Get paginated comments
            page = request.args.get("page", type=int)
            size = request.args.get("size", type=int)

            if page is not None and page < 1:
                raise CommentBadRequestError("Page must be greater than 0")

            if size is not None and size < 1:
                raise CommentBadRequestError("Size must be greater than 0")

            if page is None:
                page = DEFAULT_PAGINATION_PARAMS.page
            if size is None:
                size = DEFAULT_PAGINATION_PARAMS.size

            pagination_params = PaginationParams(page=page, size=size, offset=0)
            comments_params = GetPaginatedCommentsParams(
                account_id=account_id, task_id=task_id, pagination_params=pagination_params
            )

            pagination_result = CommentService.get_paginated_comments(params=comments_params)
            response_data = asdict(pagination_result)

            return jsonify(response_data), 200

    @access_auth_middleware
    def patch(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        """Update a comment"""
        request_data = request.get_json()

        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        if not request_data.get("content").strip():
            raise CommentBadRequestError("Content cannot be empty")

        # Validate IDs format
        if not CommentUtil.validate_object_id(object_id=task_id):
            raise CommentBadRequestError("Invalid task ID format")

        if not CommentUtil.validate_object_id(object_id=comment_id):
            raise CommentBadRequestError("Invalid comment ID format")

        update_comment_params = UpdateCommentParams(
            account_id=account_id, task_id=task_id, comment_id=comment_id, content=request_data["content"].strip()
        )

        updated_comment = CommentService.update_comment(params=update_comment_params)
        comment_dict = asdict(updated_comment)

        return jsonify(comment_dict), 200

    @access_auth_middleware
    def delete(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        """Delete a comment"""
        # Validate IDs format
        if not CommentUtil.validate_object_id(object_id=task_id):
            raise CommentBadRequestError("Invalid task ID format")

        if not CommentUtil.validate_object_id(object_id=comment_id):
            raise CommentBadRequestError("Invalid comment ID format")

        delete_params = DeleteCommentParams(account_id=account_id, task_id=task_id, comment_id=comment_id)

        CommentService.delete_comment(params=delete_params)

        return "", 204
