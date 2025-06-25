from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session

# Database session dependency
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
