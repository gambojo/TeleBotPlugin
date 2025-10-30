from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from .keyboards import PluginKeyboardBuilder
from databases import DatabaseManager
from .services.service import Service



class PluginHandlers:
    def __init__(self, config, plugin_name: str, db: DatabaseManager):
        self.config = config
        self.plugin_name = plugin_name
        self.service = Service(db)

    def register(self, router: Router):
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
        text = "EntryPoint"
        keyboard = PluginKeyboardBuilder(self.config, self.plugin_name).plugin_menu().build_markup()
        await callback.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode="HTML")

    async def bt1(self, callback: CallbackQuery):
        response = await self.service.create(123, 'bt1', 'Buton1')
        text = f"<b>Внесли данные:</b>\nID: {response.id}, Заголовок: {response.title}"
        keyboard = PluginKeyboardBuilder(self.config, self.plugin_name).plugin_menu().build_markup()
        await callback.message.edit_caption(caption=text, reply_markup=keyboard, parse_mode="HTML")


    async def bt2(self, callback: CallbackQuery):
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
