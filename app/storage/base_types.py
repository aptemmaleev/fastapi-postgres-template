from typing import Any, List, Optional, Type, TypeVar

from sqlmodel import SQLModel
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T", bound="BaseModel")


class BaseModel(SQLModel):
    class Config:
        orm_mode = True

    async def save(self: T, session: AsyncSession) -> T:
        """Сохраняет (insert/update) объект в БД."""
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    @classmethod
    async def save_many(
        cls: Type[T], session: AsyncSession, objects: List[T]
    ) -> List[T]:
        session.add_all(objects)
        await session.commit()
        await session.refresh_all(objects)
        return objects

    @classmethod
    async def insert_many(
        cls: Type[T], session: AsyncSession, objects: List[T]
    ) -> List[T]:
        data = [obj.model_dump(exclude_unset=True) for obj in objects]
        stmt = insert(cls).values(data)
        await session.execute(stmt)
        await session.commit()
        return objects

    @classmethod
    async def find_one(
        cls: Type[T], session: AsyncSession, **kwargs: Any
    ) -> Optional[T]:
        """Находит один объект по фильтрам."""
        result = await session.execute(select(cls).filter_by(**kwargs).limit(1))
        return result.scalars().first()

    @classmethod
    async def find_many(
        cls: Type[T],
        session: AsyncSession,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> List[T]:
        """Находит все объекты по фильтрам."""
        stmt = select(cls).filter_by(**kwargs).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def update(
        cls: Type[T],
        session: AsyncSession,
        filter_kwargs: dict[str, Any],
        update_kwargs: dict[str, Any],
    ) -> T:
        stmt = (
            update(cls)
            .where(
                *[getattr(cls, key) == value for key, value in filter_kwargs.items()]
            )
            .values(**update_kwargs)
            .returning(cls)
        )

        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls: Type[T], session: AsyncSession, **kwargs: Any) -> None:
        stmt = delete(cls).filter_by(**kwargs)
        await session.execute(stmt)
        await session.commit()
