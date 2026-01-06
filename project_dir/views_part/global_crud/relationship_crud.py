from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, InstrumentedAttribute

from project_dir.models import Author, Movie, Series
import project_dir.views_part.schemas as schemas
from typing import TypeVar

T = TypeVar("T", Movie, Series)


async def get_author_content_session(
    session: AsyncSession, base_class_attribute: InstrumentedAttribute, schema: type[BaseModel]
):
    stmt = select(Author).options(selectinload(base_class_attribute)).order_by(Author.id)
    authors_list = await session.scalars(stmt)
    result = {}
    for author in authors_list:
        items = getattr(author, base_class_attribute.key)
        result[f"Author {author.id} {base_class_attribute.key}"] = (
            [schema.model_validate(item).model_dump() for item in items] if items else ["No data"]
        )
    return result

async def get_author_of_content(
    session: AsyncSession, base_class: type[T], base_class_author: InstrumentedAttribute, content_id: int
):
    stmt = (
        select(base_class).where(base_class.id==content_id).options(selectinload(base_class_author)).order_by(base_class.id)
    )
    obj = await session.scalar(stmt)
    if obj:
        return schemas.AuthorSchema.model_validate(obj.author).model_dump()
    raise HTTPException(status_code=404, detail=f"No such {str(base_class.__name__).lower()} found")