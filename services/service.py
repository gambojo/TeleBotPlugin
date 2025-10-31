"""
Модуль сервисов плагина
Содержит бизнес-логику и операции с данными
"""

from sqlalchemy import select
from databases import DatabaseManager
from ..models import Data
from datetime import datetime


class Service:
    """
    Сервис для работы с данными плагина
    Параметры: db - менеджер БД
    Возвращает: экземпляр Service

    Пример использования:
        service = Service(db)
        data = await service.create(123, 'Заголовок', 'Текст')
    """

    def __init__(self, db: DatabaseManager):
        """
        Инициализация сервиса
        Параметры: db (DatabaseManager) - менеджер базы данных
        Возвращает: None
        """
        self.db = db

    async def create(self, user_id: int, title: str, content: str):
        """
        Создает новую запись в базе данных
        Параметры:
            user_id (int): ID пользователя
            title (str): заголовок записи
            content (str): содержимое записи
        Возвращает: Data - созданная запись

        Пример:
            data = await service.create(123, 'Заголовок', 'Текст записи')
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
        Получает все записи пользователя
        Параметры: user_id (int) - ID пользователя
        Возвращает: list[Data] - список записей пользователя

        Пример:
            records = await service.get(123)
            for record in records:
                print(record.title)
        """
        session = self.db.create_session()
        async with session:
            result = await session.execute(
                select(Data).where(Data.user_id == user_id)
            )
            return result.scalars().all()
