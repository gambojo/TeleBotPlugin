from core.plugins.global_registry import plugin_registry
from .plugin import Plugin

# Регистрируем плагин в глобальном реестре
plugin_registry.register("template", lambda config, db: Plugin(config, db))
