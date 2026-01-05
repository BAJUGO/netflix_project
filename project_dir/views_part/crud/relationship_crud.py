from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from project_dir.models import Author
import project_dir.views_part.schemas as schemas


async def get_author_series_session(session: AsyncSession):
    stmt = select(Author).options(selectinload(Author.series)).order_by(Author.id)
    authors_list = await session.scalars(stmt)
    result = {}
    for author in authors_list:
        list_of_series = [schemas.SeriesSchema.model_validate(series).model_dump() for series in author.series]
        result[f"Author {author.id} series"] = list_of_series if author.series else ["No series"]
    return result