"""
Модуль обработчиков плагина
Содержит обработчики сообщений и callback-запросов
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from .keyboards import PluginKeyboardBuilder
from databases import DatabaseManager
from .services.service import Service

class PluginHandlers:
    """
    Класс обработчиков плагина-шаблона
    Параметры: config - настройки плагина, plugin_name - имя плагина, db - менеджер БД
    Возвращает: экземпляр обработчиков

    Пример использования:
        handlers = PluginHandlers(settings, "TEMPLATE", db)
        handlers.register(router)
    """

    def __init__(self, config, plugin_name: str, db: DatabaseManager):
        """
        Инициализация обработчиков
        Параметры:
            config: настройки плагина
            plugin_name (str): имя плагина
            db (DatabaseManager): менеджер базы данных
        Возвращает: None
        """
        self.config = config
        self.plugin_name = plugin_name
        self.service = Service(db)

    def register(self, router: Router):
        """
        Регистрирует обработчики в роутере
        Параметры: router (Router) - роутер для регистрации
        Возвращает: None

        Пример:
            handlers.register(router)
        """
        router.callback_query.register(
            self.entry_callback,
            F.data == f"plugin:{self.plugin_name}"
        )

        router.callback_query.register(
            self.bt1,
            F.data == f"{self.plugin_name.lower()}:bt1"
        )

        router.callback_query.register(
            self.bt2,
            F.data == f"{self.plugin_name.lower()}:bt2"
        )

    async def entry_callback(self, callback: CallbackQuery):
        """
        Обработчик входа в плагин
        Параметры: callback (CallbackQuery) - callback данные
        Возвращает: None

        Пример сценария:
            Пользователь нажимает кнопку плагина → показывается меню плагина
        """
        text = "EntryPoint"
        keyboard = PluginKeyboardBuilder(self.config, self.plugin_name).plugin_menu().build_markup()
        await callback.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode="HTML")

    async def bt1(self, callback: CallbackQuery):
        """
        Обработчик кнопки bt1 - запись данных
        Параметры: callback (CallbackQuery) - callback данные
        Возвращает: None

        Пример сценария:
            Пользователь нажимает "Записать" → данные сохраняются в БД → показывается результат
        """
        response = await self.service.create(123, 'bt1', 'Buton1')
        text = f"<b>Внесли данные:</b>\nID: {response.id}, Заголовок: {response.title}"
        keyboard = PluginKeyboardBuilder(self.config, self.plugin_name).plugin_menu().build_markup()
        await callback.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode="HTML")

    async def bt2(self, callback: CallbackQuery):
        """
        Обработчик кнопки bt2 - чтение данных
        Параметры: callback (CallbackQuery) - callback данные
        Возвращает: None

        Пример сценария:
            Пользователь нажимает "Прочитать" → данные читаются из БД → показывается список
        """
        try:
            # Получаем данные из БД
            responses = await self.service.get(123)

            # Форматируем данные в строку
            if responses:
                text_lines = ["<b>Внесенные данные:</b>"]
                for response in responses:
                    text_lines.append(f"• ID: {response.id}, Заголовок: {response.title}")
                text = "\n".join(text_lines)
            else:
                text = "📭 <b>В базе данных нет записей</b>"

            keyboard = PluginKeyboardBuilder(self.config, self.plugin_name).plugin_menu().build_markup()
            await callback.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode="HTML")

        except Exception as e:
            self.logger.error(f"Error in bt2: {e}")
            await callback.answer("❌ Ошибка при получении данных", show_alert=True)
