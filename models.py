from databases.database_manager import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


class Data(Base):
    """
    Пример модели данных для плагина
    Параметры: наследует от Base
    Возвращает: экземпляр модели Data
    Пример: data = Data(user_id=123, title='Заголовок')
    """

    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime)
