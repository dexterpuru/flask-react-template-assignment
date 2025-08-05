from modules.authentication.types import AccessTokenErrorCode
from modules.comment.types import CommentErrorCode
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):

    # POST /accounts/{account_id}/tasks/{task_id}/comments Tests

    def test_create_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment_data = {"content": self.DEFAULT_COMMENT_CONTENT}

        response = self.make_authenticated_request("POST", account.id, task.id, token, data=comment_data)

        assert response.status_code == 201
        assert response.json is not None
        self.assert_comment_response(
            response.json, content=self.DEFAULT_COMMENT_CONTENT, account_id=account.id, task_id=task.id
        )

    def test_create_comment_missing_content(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment_data = {}

        response = self.make_authenticated_request("POST", account.id, task.id, token, data=comment_data)

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Content is required" in response.json.get("message")

    def test_create_comment_empty_content(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment_data = {"content": "   "}

        response = self.make_authenticated_request("POST", account.id, task.id, token, data=comment_data)

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Content cannot be empty" in response.json.get("message")

    def test_create_comment_invalid_task_id(self) -> None:
        account, token = self.create_account_and_get_token()
        invalid_task_id = "invalid-id"
        comment_data = {"content": self.DEFAULT_COMMENT_CONTENT}

        response = self.make_authenticated_request("POST", account.id, invalid_task_id, token, data=comment_data)

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Invalid task ID format" in response.json.get("message")

    def test_create_comment_task_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        non_existent_task_id = "507f1f77bcf86cd799439011"
        comment_data = {"content": self.DEFAULT_COMMENT_CONTENT}

        response = self.make_authenticated_request("POST", account.id, non_existent_task_id, token, data=comment_data)

        self.assert_error_response(response, 404, CommentErrorCode.TASK_NOT_FOUND)

    def test_create_comment_unauthenticated(self) -> None:
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        comment_data = {"content": self.DEFAULT_COMMENT_CONTENT}

        response = self.make_unauthenticated_request("POST", account.id, task.id, data=comment_data)

        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

    def test_create_comment_cross_account_access(self) -> None:
        # Create two accounts
        account1, token1 = self.create_account_and_get_token()
        account2, _ = self.create_account_and_get_token(username="other@example.com")

        # Create task for account2
        task2 = self.create_test_task(account_id=account2.id)
        comment_data = {"content": self.DEFAULT_COMMENT_CONTENT}

        # Try to create comment on account2's task using account1's token
        response = self.make_cross_account_request("POST", account2.id, task2.id, token1, data=comment_data)

        self.assert_error_response(response, 401, AccessTokenErrorCode.UNAUTHORIZED_ACCESS)

    # GET /accounts/{account_id}/tasks/{task_id}/comments Tests (Pagination)

    def test_get_paginated_comments_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        # Create multiple comments
        created_comments = self.create_multiple_test_comments(account_id=account.id, task_id=task.id, count=5)

        response = self.make_authenticated_request("GET", account.id, task.id, token, query_params="page=1&size=3")

        assert response.status_code == 200
        assert response.json is not None
        self.assert_pagination_response(
            response.json, expected_items_count=3, expected_total_count=5, expected_page=1, expected_size=3
        )

    def test_get_paginated_comments_default_pagination(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        # Create multiple comments
        self.create_multiple_test_comments(account_id=account.id, task_id=task.id, count=3)

        response = self.make_authenticated_request("GET", account.id, task.id, token)

        assert response.status_code == 200
        assert response.json is not None
        self.assert_pagination_response(response.json, expected_items_count=3, expected_total_count=3)

    def test_get_paginated_comments_invalid_pagination(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_authenticated_request("GET", account.id, task.id, token, query_params="page=0&size=5")

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Page must be greater than 0" in response.json.get("message")

    def test_get_paginated_comments_empty_result(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_authenticated_request("GET", account.id, task.id, token)

        assert response.status_code == 200
        assert response.json is not None
        self.assert_pagination_response(response.json, expected_items_count=0, expected_total_count=0)

    def test_get_paginated_comments_invalid_task_id(self) -> None:
        account, token = self.create_account_and_get_token()
        invalid_task_id = "invalid-id"

        response = self.make_authenticated_request("GET", account.id, invalid_task_id, token)

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Invalid task ID format" in response.json.get("message")

    def test_get_paginated_comments_unauthenticated(self) -> None:
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)

        response = self.make_unauthenticated_request("GET", account.id, task.id)

        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

    # GET /accounts/{account_id}/tasks/{task_id}/comments/{comment_id} Tests

    def test_get_comment_by_id_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        response = self.make_authenticated_request("GET", account.id, task.id, token, comment_id=comment.id)

        assert response.status_code == 200
        assert response.json is not None
        self.assert_comment_response(response.json, expected_comment=comment)

    def test_get_comment_by_id_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        non_existent_comment_id = "507f1f77bcf86cd799439011"

        response = self.make_authenticated_request(
            "GET", account.id, task.id, token, comment_id=non_existent_comment_id
        )

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_get_comment_by_id_invalid_comment_id(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        invalid_comment_id = "invalid-id"

        response = self.make_authenticated_request("GET", account.id, task.id, token, comment_id=invalid_comment_id)

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Invalid comment ID format" in response.json.get("message")

    def test_get_comment_by_id_invalid_task_id(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)
        invalid_task_id = "invalid-id"

        response = self.make_authenticated_request("GET", account.id, invalid_task_id, token, comment_id=comment.id)

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Invalid task ID format" in response.json.get("message")

    def test_get_comment_by_id_unauthenticated(self) -> None:
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        response = self.make_unauthenticated_request("GET", account.id, task.id, comment_id=comment.id)

        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

    # PATCH /accounts/{account_id}/tasks/{task_id}/comments/{comment_id} Tests

    def test_update_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        new_content = "Updated comment content"
        update_data = {"content": new_content}

        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=update_data
        )

        assert response.status_code == 200
        assert response.json is not None
        self.assert_comment_response(response.json, content=new_content, account_id=account.id, task_id=task.id)

    def test_update_comment_missing_content(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        update_data = {}

        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=update_data
        )

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Content is required" in response.json.get("message")

    def test_update_comment_empty_content(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        update_data = {"content": "   "}

        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=comment.id, data=update_data
        )

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Content cannot be empty" in response.json.get("message")

    def test_update_comment_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        non_existent_comment_id = "507f1f77bcf86cd799439011"

        update_data = {"content": "Updated content"}

        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=non_existent_comment_id, data=update_data
        )

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_update_comment_invalid_ids(self) -> None:
        account, token = self.create_account_and_get_token()
        invalid_task_id = "invalid-task-id"
        invalid_comment_id = "invalid-comment-id"

        update_data = {"content": "Updated content"}

        response = self.make_authenticated_request(
            "PATCH", account.id, invalid_task_id, token, comment_id=invalid_comment_id, data=update_data
        )

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Invalid task ID format" in response.json.get("message")

    def test_update_comment_unauthenticated(self) -> None:
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        update_data = {"content": "Updated content"}

        response = self.make_unauthenticated_request(
            "PATCH", account.id, task.id, comment_id=comment.id, data=update_data
        )

        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

    # DELETE /accounts/{account_id}/tasks/{task_id}/comments/{comment_id} Tests

    def test_delete_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        response = self.make_authenticated_request("DELETE", account.id, task.id, token, comment_id=comment.id)

        assert response.status_code == 204
        assert response.data == b""

        # Verify comment is actually deleted
        get_response = self.make_authenticated_request("GET", account.id, task.id, token, comment_id=comment.id)
        self.assert_error_response(get_response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        non_existent_comment_id = "507f1f77bcf86cd799439011"

        response = self.make_authenticated_request(
            "DELETE", account.id, task.id, token, comment_id=non_existent_comment_id
        )

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_invalid_ids(self) -> None:
        account, token = self.create_account_and_get_token()
        invalid_task_id = "invalid-task-id"
        invalid_comment_id = "invalid-comment-id"

        response = self.make_authenticated_request(
            "DELETE", account.id, invalid_task_id, token, comment_id=invalid_comment_id
        )

        self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)
        assert "Invalid task ID format" in response.json.get("message")

    def test_delete_comment_unauthenticated(self) -> None:
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(account_id=account.id, task_id=task.id)

        response = self.make_unauthenticated_request("DELETE", account.id, task.id, comment_id=comment.id)

        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

    def test_delete_comment_cross_account_access(self) -> None:
        # Create two accounts
        account1, token1 = self.create_account_and_get_token()
        account2, _ = self.create_account_and_get_token(username="other@example.com")

        # Create task and comment for account2
        task2 = self.create_test_task(account_id=account2.id)
        comment2 = self.create_test_comment(account_id=account2.id, task_id=task2.id)

        # Try to delete account2's comment using account1's token
        response = self.make_cross_account_request("DELETE", account2.id, task2.id, token1, comment_id=comment2.id)

        self.assert_error_response(response, 401, AccessTokenErrorCode.UNAUTHORIZED_ACCESS)
