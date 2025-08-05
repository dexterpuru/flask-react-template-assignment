from flask import Blueprint

from modules.comment.rest_api.comment_view import CommentView


class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        comment_view = CommentView.as_view("comment_view")

        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments", view_func=comment_view, methods=["POST", "GET"]
        )

        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments/<comment_id>",
            view_func=comment_view,
            methods=["GET", "PATCH", "DELETE"],
        )
