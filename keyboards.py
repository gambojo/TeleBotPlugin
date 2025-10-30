from plugins.vpn.config import PluginSettings
from core.keyboards import KeyboardBuilderBase


class PluginKeyboardBuilder(KeyboardBuilderBase):
    """
    Построитель клавиатур для плагина-шаблона
    Параметры: plugin_conf - конфигурация плагина
    Возвращает: экземпляр PluginKeyboardBuilder
    Пример: builder = PluginKeyboardBuilder(settings)
    """

    def __init__(self, plugin_conf: PluginSettings, plugin_name: str):
        super().__init__()
        self.plugin_conf = plugin_conf
        self.plugin_name = plugin_name

    def integrated_buttons(self) -> "PluginKeyboardBuilder":
        self.keyboard = []
        self.add_button("Записать", f"{self.plugin_name.lower()}:bt1")
        self.add_button("Прочитать", f"{self.plugin_name.lower()}:bt2")
        return self

    def entry_button(self) -> "PluginKeyboardBuilder":
        self.keyboard = []
        self.add_button("Перейти в сервис", f"plugin:{self.plugin_name}")
        return self

    def plugin_menu(self) -> "PluginKeyboardBuilder":
        self.keyboard = []
        self.add_button("Записать", f"{self.plugin_name.lower()}:bt1")
        self.add_button("Прочитать", f"{self.plugin_name.lower()}:bt2")
        return self.add_core_buttons()
