from sqlalchemy import select
from databases import DatabaseManager
from ..models import Data
from datetime import datetime


class Service:
    """
    Сервис для работы с данными плагина-шаблона
    Параметры: db - менеджер БД
    Возвращает: экземпляр Service
    Пример: service = Service(db)
    """

    def __init__(self, db: DatabaseManager):
        self.db = db

    async def create(self, user_id: int, title: str, content: str):
        """
        Создает новую запись примера
        Параметры: user_id - ID пользователя, title - заголовок, content - содержимое
        Возвращает: Data - созданная запись
        Пример: example = await service.create(123, 'Заголовок', 'Текст')
        """
        session = self.db.create_session()
        async with session:
            example = Data(
                user_id=user_id,
                title=title,
                content=content,
                created_at=datetime.now()
            )
            session.add(example)
            await session.commit()
            await session.refresh(example)
            return example

    async def get(self, user_id: int):
        """
        Получает все примеры пользователя
        Параметры: user_id - ID пользователя
        Возвращает: list[ExampleData] - список записей пользователя
        Пример: examples = await service.get(123)
        """
        session = self.db.create_session()
        async with session:
            result = await session.execute(
                select(Data).where(Data.user_id == user_id)
            )
            return result.scalars().all()
