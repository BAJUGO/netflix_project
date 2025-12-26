from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from project_dir.models import Author


async def get_author_series_session(session: AsyncSession):
    stmt = select(Author).options(selectinload(Author.series)).order_by(Author.id)
    authors_list = await session.scalars(stmt)
    result: dict[str, list] = {}
    for author in authors_list:
        result[f"Author {author.id} series"] = author.series if author.series else ["No series"]
    return result