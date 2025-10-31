"""
Главный модуль плагина
Содержит основной класс плагина и интеграцию с ядром системы
"""

from core.plugins.base import PluginBase
from core.config import ConfigManager
from aiogram import Router
from aiogram.types import InlineKeyboardButton
from core.middlewares import PluginLoggerMiddleware
from modules.databases import DatabaseManager
from .config import PluginSettings
from .handlers import PluginHandlers
from .keyboards import PluginKeyboardBuilder

class Plugin(PluginBase):
    """
    Главный класс плагина-шаблона для создания новых плагинов
    Наследует: PluginBase (ядро системы)
    Параметры: config - менеджер конфигурации, db - менеджер БД
    Возвращает: экземпляр плагина

    Пример использования:
        plugin = Plugin(config, db)
        router = plugin.get_router()
    """

    def __init__(self, config: ConfigManager, db: DatabaseManager):
        """
        Инициализация плагина
        Параметры:
            config (ConfigManager): менеджер конфигурации ядра
            db (DatabaseManager): менеджер базы данных
        Возвращает: None

        Пример:
            plugin = Plugin(config, db)
        """
        self.config = config
        self.db = db
        self.plugin_name = self.get_name()
        self.settings: PluginSettings = config.load_plugin_config(self.plugin_name, PluginSettings)

    def get_router(self) -> Router:
        """
        Создает и возвращает роутер плагина с обработчиками
        Возвращает: Router - роутер с зарегистрированными обработчиками

        Пример:
            router = plugin.get_router()
            dp.include_router(router)
        """
        router = Router(name=self.plugin_name)
        PluginHandlers(self.settings, self.plugin_name, self.db).register(router)
        router.message.middleware(PluginLoggerMiddleware(self.plugin_name))
        router.callback_query.middleware(PluginLoggerMiddleware(self.plugin_name))
        return router

    def get_config(self) -> type[PluginSettings]:
        """
        Возвращает класс конфигурации плагина
        Возвращает: type[PluginSettings] - класс настроек плагина

        Пример:
            config_class = plugin.get_config()
            settings = config_class()
        """
        return PluginSettings

    def get_integrated_buttons(self) -> list[list[InlineKeyboardButton]]:
        """
        Возвращает кнопки для интеграции в главное меню (integrated режим)
        Возвращает: list[list[InlineKeyboardButton]] - список рядов кнопок

        Пример:
            buttons = plugin.get_integrated_buttons()
            # → [[InlineKeyboardButton(text="Записать", callback_data="template:bt1")],
            #     [InlineKeyboardButton(text="Прочитать", callback_data="template:bt2")]]
        """
        builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
        return builder.integrated_buttons().keyboard

    def get_entry_button(self) -> list[list[InlineKeyboardButton]]:
        """
        Возвращает кнопку входа в плагин (entry режим)
        Возвращает: list[list[InlineKeyboardButton]] - список с одной кнопкой

        Пример:
            button = plugin.get_entry_button()
            # → [[InlineKeyboardButton(text="Перейти в сервис", callback_data="plugin:TEMPLATE")]]
        """
        builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
        return builder.entry_button().keyboard

    def get_settings(self) -> PluginSettings:
        """
        Возвращает экземпляр настроек плагина
        Возвращает: PluginSettings - загруженные настройки плагина

        Пример:
            settings = plugin.get_settings()
            variable = settings.EXAMPLE_STRING_VAR
        """
        return self.settings

    def get_menu_buttons(self) -> list[list[InlineKeyboardButton]]:
        """
        Совместимость со старым интерфейсом
        Возвращает: list[list[InlineKeyboardButton]] - кнопки для меню

        Пример:
            buttons = plugin.get_menu_buttons()
        """
        return self.get_integrated_buttons()
