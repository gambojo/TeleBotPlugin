"""
Модуль регистрации плагина
Автоматически регистрирует плагин в системе при импорте
"""

from core.plugins.global_registry import plugin_registry
from .plugin import Plugin

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
plugin_registry.register(lambda config, db: Plugin(config, db))
"""
Регистрация фабрики плагина в глобальном реестре
Параметры: config (ConfigManager), db (DatabaseManager)
Возвращает: зарегистрированную фабрику

Пример сценария:
    При импорте модуля плагин автоматически регистрируется
    PluginManager затем использует фабрику для создания экземпляра
"""
