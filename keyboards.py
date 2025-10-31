"""
Модуль клавиатур плагина
Содержит построитель кастомных клавиатур для плагина
"""

from .config import PluginSettings
from core.keyboards import KeyboardBuilderBase

class PluginKeyboardBuilder(KeyboardBuilderBase):
    """
    Построитель клавиатур для плагина-шаблона
    Наследует: KeyboardBuilderBase (ядро системы)
    Параметры: plugin_conf - настройки плагина, plugin_name - имя плагина
    Возвращает: экземпляр построителя

    Пример использования:
        builder = PluginKeyboardBuilder(settings, "TEMPLATE")
        keyboard = builder.plugin_menu().build_markup()
    """

    def __init__(self, plugin_conf: PluginSettings, plugin_name: str):
        """
        Инициализация построителя
        Параметры:
            plugin_conf (PluginSettings): настройки плагина
            plugin_name (str): имя плагина в верхнем регистре
        Возвращает: None
        """
        super().__init__()
        self.plugin_conf = plugin_conf
        self.plugin_name = plugin_name

    def integrated_buttons(self) -> "PluginKeyboardBuilder":
        """
        Создает кнопки для интегрированного режима отображения
        Возвращает: PluginKeyboardBuilder - self для цепочки вызовов

        Пример:
            builder.integrated_buttons().build_markup()
        """
        self.keyboard = []
        self.add_button("Записать", f"{self.plugin_name.lower()}:bt1")
        self.add_button("Прочитать", f"{self.plugin_name.lower()}:bt2")
        return self

    def entry_button(self) -> "PluginKeyboardBuilder":
        """
        Создает кнопку входа для entry режима отображения
        Возвращает: PluginKeyboardBuilder - self для цепочки вызовов

        Пример:
            builder.entry_button().build_markup()
        """
        self.keyboard = []
        self.add_button("Перейти в сервис", f"plugin:{self.plugin_name}")
        return self

    def plugin_menu(self) -> "PluginKeyboardBuilder":
        """
        Создает внутреннее меню плагина
        Возвращает: PluginKeyboardBuilder - self для цепочки вызовов

        Пример:
            builder.plugin_menu().build_markup()
        """
        self.keyboard = []
        self.add_button("Записать", f"{self.plugin_name.lower()}:bt1")
        self.add_button("Прочитать", f"{self.plugin_name.lower()}:bt2")
        return self.add_core_buttons()
