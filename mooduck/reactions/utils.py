from reactions.models import Comment
from reactions.schemas import GetComment


def get_comment_response(comment: Comment) -> GetComment:
    answering_to = None
    if comment.answering_to:
        answering_to = comment.answering_to.id
    return GetComment(
        id=comment.id,
        author=comment.author,
        answering_to=answering_to,
        text=comment.text,
        created_at=comment.created_at
    )


def get_comment_list_response(comments: list[Comment]) -> list[GetComment]:
    return [get_comment_response(comment) for comment in comments]
