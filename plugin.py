from core.plugins.base import PluginBase
from core.config import ConfigManager
from aiogram import Router
from aiogram.types import InlineKeyboardButton
from core.middlewares import PluginLoggerMiddleware
from databases import DatabaseManager
from .config import PluginSettings
from .handlers import PluginHandlers
from .keyboards import PluginKeyboardBuilder



class Plugin(PluginBase):
    """
    Пример плагина-шаблона для создания новых плагинов
    Параметры: config - менеджер конфигурации, db - менеджер БД
    Возвращает: экземпляр плагина
    Пример: plugin = Plugin(config, db)
    """

    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
        self.plugin_name = self.get_name()
        self.settings: PluginSettings = config.load_plugin_config(self.plugin_name, PluginSettings)

    def get_router(self) -> Router:
        router = Router(name=self.plugin_name)
        PluginHandlers(self.settings, self.plugin_name, self.db).register(router)
        router.message.middleware(PluginLoggerMiddleware(self.plugin_name))
        router.callback_query.middleware(PluginLoggerMiddleware(self.plugin_name))
        return router

    def get_config(self) -> type[PluginSettings]:
        return PluginSettings

    def get_integrated_buttons(self) -> list[list[InlineKeyboardButton]]:
        builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
        return builder.integrated_buttons().keyboard

    def get_entry_button(self) -> list[list[InlineKeyboardButton]]:
        builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
        return builder.entry_button().keyboard

    def get_settings(self) -> PluginSettings:
        return self.settings

    def get_menu_buttons(self) -> list[list[InlineKeyboardButton]]:
        return self.get_integrated_buttons()
