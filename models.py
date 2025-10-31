"""
Модуль моделей базы данных
Содержит SQLAlchemy модели для плагина
"""

from modules.databases.database_manager import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


class Data(Base):
    """
    Модель данных для плагина
    Наследует: Base (SQLAlchemy)
    Возвращает: экземпляр модели Data

    Пример использования:
        data = Data(user_id=123, title='Заголовок', content='Текст')
    """

    __tablename__ = "data"
    """
    Название таблицы в базе данных
    Тип: str
    Значение: "data"
    """

    id = Column(Integer, primary_key=True)
    """
    Первичный ключ записи
    Тип: Integer
    Назначение: уникальный идентификатор
    """

    user_id = Column(Integer, ForeignKey("users.id"))
    """
    ID пользователя (внешний ключ)
    Тип: Integer
    Назначение: связь с таблицей users
    Пример: user_id = 123456789
    """

    title = Column(String(255))
    """
    Заголовок данных
    Тип: String(255)
    Назначение: краткое описание
    Пример: title = "Мои настройки"
    """

    content = Column(Text)
    """
    Содержимое данных
    Тип: Text
    Назначение: основной текст/данные
    Пример: content = "Подробное описание конфигурации"
    """

    created_at = Column(DateTime)
    """
    Время создания записи
    Тип: DateTime
    Назначение: отслеживание времени создания
    Пример: created_at = datetime.now()
    """
