"""
Модуль конфигурации плагина
Содержит настройки и переменные окружения плагина
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
ENABLED: bool = True
"""
Флаг включения/отключения плагина
Тип: bool
Значение по умолчанию: True
Пример: ENABLED = False  # отключает плагин
"""

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
class PluginSettings(BaseSettings):
    """
    Класс настроек плагина
    Наследует: BaseSettings (pydantic)
    Возвращает: экземпляр с загруженными настройками
    Используется для: загрузки конфигурации из .env файла

    Пример использования:
        settings = PluginSettings()
        api_key = settings.API_KEY
    """

    # 🔧 НАСТРОЙТЕ ЭТО - ваши переменные здесь
    PLUGIN_TITLE: str = "Мой плагин"
    """
    Название плагина для отображения пользователям
    Тип: str
    Значение по умолчанию: "Мой плагин"
    Пример: PLUGIN_TITLE = "VPN Сервис"
    """

    BUTTON_TEXT: str = "Нажми меня"
    """
    Текст кнопки плагина в главном меню
    Тип: str  
    Значение по умолчанию: "Нажми меня"
    Пример: BUTTON_TEXT = "Управление VPN"
    """

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
