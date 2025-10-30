from core.plugins.global_registry import plugin_registry
from .plugin import Plugin

# Автоматическая регистрация - имя определяется из директории
plugin_registry.register(lambda config, db: Plugin(config, db))
