from pydantic_settings import BaseSettings, SettingsConfigDict

ENABLED: bool = True


class PluginSettings(BaseSettings):
    """
    Конфигурация для плагина-шаблона
    Параметры: наследует от BaseSettings
    Возвращает: экземпляр с настройками плагина
    Пример: settings = PluginSettings()
    """

    API_KEY: str = "your_api_key_here"
    MAX_USERS: int = 100
    ENABLED_FEATURES: list = ["feature_a", "feature_b"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
