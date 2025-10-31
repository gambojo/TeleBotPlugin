"""
Главный модуль плагина
Содержит основной класс плагина и интеграцию с ядром системы
"""

from core.plugins.base import PluginBase
from core.config import ConfigManager
from aiogram import Router
from aiogram.types import InlineKeyboardButton, CallbackQuery
from databases import DatabaseManager
from .config import PluginSettings


# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
class Plugin(PluginBase):
    """
    Главный класс плагина
    Наследует: PluginBase (ядро системы)
    Параметры: config - менеджер конфигурации, db - менеджер БД
    Возвращает: экземпляр плагина

    Пример использования:
        plugin = Plugin(config_manager, database_manager)
        router = plugin.get_router()
    """

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
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

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_router(self) -> Router:
        """
        Создает и возвращает роутер плагина
        Возвращает: Router - роутер с обработчиками плагина

        Пример:
            router = plugin.get_router()
            dp.include_router(router)
        """
        router = Router(name=self.plugin_name)

        # 🔧 НАСТРОЙТЕ ЭТО - добавьте ваши обработчики
        @router.callback_query(lambda c: c.data == f"plugin:{self.plugin_name}")
        async def entry_point(callback: CallbackQuery):
            """
            Обработчик входа в плагин
            Параметры: callback (CallbackQuery) - callback данные
            Возвращает: None

            Пример сценария:
                Пользователь нажимает кнопку плагина → показывается приветствие
            """
            await callback.message.answer(
                f"Привет! Это {self.settings.PLUGIN_TITLE}",
                reply_markup=self._get_main_keyboard()
            )

        return router

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_integrated_buttons(self) -> list[list[InlineKeyboardButton]]:
        """
        Возвращает кнопки для интегрированного режима отображения
        Возвращает: list[list[InlineKeyboardButton]] - список рядов кнопок

        Пример:
            buttons = plugin.get_integrated_buttons()
            # → [[InlineKeyboardButton(text="Мой плагин", callback_data="plugin:TEMPLATE")]]
        """
        # 🔧 НАСТРОЙТЕ ЭТО - ваши кнопки для главного меню
        return [
            [InlineKeyboardButton(
                text=self.settings.BUTTON_TEXT,
                callback_data=f"plugin:{self.plugin_name}"
            )]
        ]

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_entry_button(self) -> list[list[InlineKeyboardButton]]:
        """
        Возвращает кнопку входа для entry режима отображения
        Возвращает: list[list[InlineKeyboardButton]] - список с одной кнопкой

        Пример:
            button = plugin.get_entry_button()
            # → [[InlineKeyboardButton(text="Открыть плагин", callback_data="plugin:TEMPLATE")]]
        """
        # 🔧 НАСТРОЙТЕ ЭТО - кнопка входа (если нужен entry режим)
        return self.get_integrated_buttons()

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_config(self) -> type[PluginSettings]:
        """
        Возвращает класс конфигурации плагина
        Возвращает: type[PluginSettings] - класс настроек

        Пример:
            config_class = plugin.get_config()
            settings = config_class()
        """
        return PluginSettings

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_settings(self) -> PluginSettings:
        """
        Возвращает экземпляр настроек плагина
        Возвращает: PluginSettings - загруженные настройки

        Пример:
            settings = plugin.get_settings()
            title = settings.PLUGIN_TITLE
        """
        return self.settings

    # ⚡ ОПЦИОНАЛЬНО - вспомогательные методы
    def _get_main_keyboard(self):
        """
        Создает клавиатуру для главного меню плагина
        Возвращает: InlineKeyboardMarkup - клавиатура с кнопками

        Пример использования:
            keyboard = self._get_main_keyboard()
            await message.answer("Меню:", reply_markup=keyboard)
        """
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="core:main_menu")]
        ])
