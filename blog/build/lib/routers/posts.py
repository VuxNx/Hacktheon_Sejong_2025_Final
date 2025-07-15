from typing import Annotated, List, Union
from uuid import UUID

from fastapi.params import Depends
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from models.token import get_current_user
from models.user import User
from models.post import Post
from notify import send_new_post_email
from repositories.post import PostRepository

router = APIRouter()


@router.get("/posts/{user_id}/{post_id}", response_model=Post)
async def get_post(user_id: Union[UUID, str], post_id: UUID) -> Post:
    try:
        return PostRepository.get_post(user_id, post_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/posts", response_model=List[UUID])
async def get_posts(user_id: Union[UUID, str]) -> List[UUID]:
    return PostRepository.get_posts(user_id)


class PostPostsBody(BaseModel):
    title: str
    content: str


@router.post("/posts")
async def new_post(
    current_user: Annotated[User, Depends(get_current_user)], body: PostPostsBody
) -> UUID:
    post = Post(
        title=body.title,
        content=body.content,
        author=current_user.user_id,
    )
    try:
        PostRepository.new_post(current_user.user_id, post)

        await send_new_post_email(current_user, post)

        return post.post_id
    except ValueError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_ERROR)
