# TeleBotPlugin

## TeleBotPlugin - Шаблон разработки плагинов для TeleBotCore

<div align="center">

**Шаблон разработки плагинов для создания Telegram ботов на базе TeleBotCore**

[Примеры](#Пример-минимального-рабочий-плагин-мз-3-файлов) • 
[Расширения и кастомизация](#Расширения-и-кастомизация) • 
[Соглашения и стандарты](#Соглашения-и-стандарты) • 
[Обязательные компоненты](#Обязательные-компоненты) • 
[Лицензия](#лицензия) • 
[Авторы](#авторы)

</div>


## Пример минимального рабочий плагин мз 3 файлов
### Условные обозначения и система маркировки
- **НЕ ТРОГАТЬ** - Системные блоки
```text
# СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
```
- **НАСТРОИТЬ** - Ваши кастомные настройки
```text
# НАСТРОЙТЕ ЭТО - ваш код здесь
```
- **ОПЦИОНАЛЬНО** - Можно добавить/удалить
```text
# ОПЦИОНАЛЬНО - добавляйте по необходимости
```

- **1. config.py - настройки плагина**
```python
# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
from pydantic_settings import BaseSettings, SettingsConfigDict

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
ENABLED: bool = True

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
class PluginSettings(BaseSettings):
    # 🔧 НАСТРОЙТЕ ЭТО - ваши переменные здесь
    PLUGIN_TITLE: str = "Мой плагин"
    BUTTON_TEXT: str = "Нажми меня"
    
    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
```

- **2. plugin.py - главный класс**
```python
# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
from core.plugins.base import PluginBase
from core.config import ConfigManager
from aiogram import Router
from aiogram.types import InlineKeyboardButton, CallbackQuery
from databases import DatabaseManager
from .config import PluginSettings

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
class Plugin(PluginBase):
    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
        self.plugin_name = self.get_name()
        self.settings: PluginSettings = config.load_plugin_config(self.plugin_name, PluginSettings)

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_router(self) -> Router:
        router = Router(name=self.plugin_name)
        
        # 🔧 НАСТРОЙТЕ ЭТО - добавьте ваши обработчики
        @router.callback_query(lambda c: c.data == f"plugin:{self.plugin_name}")
        async def entry_point(callback: CallbackQuery):
            await callback.message.answer(
                f"Привет! Это {self.settings.PLUGIN_TITLE}",
                reply_markup=self._get_main_keyboard()
            )
        
        return router

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_integrated_buttons(self) -> list[list[InlineKeyboardButton]]:
        # 🔧 НАСТРОЙТЕ ЭТО - ваши кнопки для главного меню
        return [
            [InlineKeyboardButton(
                text=self.settings.BUTTON_TEXT, 
                callback_data=f"plugin:{self.plugin_name}"
            )]
        ]

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_entry_button(self) -> list[list[InlineKeyboardButton]]:
        # 🔧 НАСТРОЙТЕ ЭТО - кнопка входа (если нужен entry режим)
        return self.get_integrated_buttons()

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_config(self) -> type[PluginSettings]:
        return PluginSettings

    # 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
    def get_settings(self) -> PluginSettings:
        return self.settings

    # ⚡ ОПЦИОНАЛЬНО - вспомогательные методы
    def _get_main_keyboard(self):
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="core:main_menu")]
        ])
```

- **3. init.py - регистрация**
```python
# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
from core.plugins.global_registry import plugin_registry
from .plugin import Plugin

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ!
plugin_registry.register(lambda config, db: Plugin(config, db))
```

### Шпаргалка - что именно менять
- В **config.py**:
```
# 🔧 МЕНЯЙТЕ ТОЛЬКО ЭТИ ПЕРЕМЕННЫЕ:
PLUGIN_TITLE: str = "Мой плагин"        # ← Название плагина
BUTTON_TEXT: str = "Нажми меня"         # ← Текст кнопки

# 🚫 ВСЁ ОСТАЛЬНОЕ НЕ ТРОГАТЬ!
```
- В **plugin.py**:
```
# 🔧 МЕНЯЙТЕ ТОЛЬКО ЭТИ БЛОКИ:

# 1. Логика ответа на кнопку:
async def entry_point(callback: CallbackQuery):
    await callback.message.answer(
        f"Привет! Это {self.settings.PLUGIN_TITLE}",  # ← Ваш текст
        reply_markup=self._get_main_keyboard()
    )

# 2. Кнопки в главном меню:
def get_integrated_buttons(self):
    return [
        [InlineKeyboardButton(
            text=self.settings.BUTTON_TEXT,           # ← Ваш текст кнопки
            callback_data=f"plugin:{self.plugin_name}"
        )]
    ]

# 🚫 ВСЁ ОСТАЛЬНОЕ НЕ ТРОГАТЬ!
```
- В **__init__.py**:
```
# 🚫 ВЕСЬ ФАЙЛ - НЕ ТРОГАТЬ ВООБЩЕ!
```

## Расширения и кастомизация
### 1. Дополнительные обработчики - новые кнопки и логику
- **Создайте структуру файлов**
```text
ваш_плагин/
├── config.py          # Обязательно
├── plugin.py          # Обязательно
├── __init__.py        # Обязательно
└── handlers.py        # Дополнительно -> Новый файл опционально обработчики можно вынести сюда - handlers
```
- **Добавьте в plugin.py:**
```python
def get_router(self) -> Router:
    router = Router(name=self.plugin_name)
    
    # Существующий обработчик
    @router.callback_query(lambda c: c.data == f"plugin:{self.plugin_name}")
    async def entry_point(callback: CallbackQuery):
        await callback.message.answer("Главное меню плагина", reply_markup=self._get_main_keyboard())
    
    # 🔧 НОВЫЙ ОБРАБОТЧИК - добавьте это
    @router.callback_query(lambda c: c.data == f"{self.plugin_name.lower()}:action1")
    async def handle_action1(callback: CallbackQuery):
        await callback.message.answer("Вы выполнили действие 1!")
    
    return router

def get_integrated_buttons(self):
    return [
        [InlineKeyboardButton(text="Действие 1", callback_data=f"{self.plugin_name.lower()}:action1")]  # 🔧 Новая кнопка
    ]
```

### 2. Свои клавиатуры - через keyboards.py
- **Создайте структуру файлов**
```text
ваш_плагин/
├── config.py          # Обязательно
├── plugin.py          # Обязательно
├── __init__.py        # Обязательно
└── keyboards.py       # Дополнительно -> Новый файл - клавиатуры
```
- **Создайте файл keyboards.py:**
```python
from core.keyboards import KeyboardBuilderBase
from .config import PluginSettings

class PluginKeyboardBuilder(KeyboardBuilderBase):
    def __init__(self, plugin_conf: PluginSettings, plugin_name: str):
        super().__init__()
        self.plugin_conf = plugin_conf
        self.plugin_name = plugin_name
    
    def main_menu(self):
        self.keyboard = []
        self.add_button("Действие 1", f"{self.plugin_name.lower()}:action1")
        self.add_button("Действие 2", f"{self.plugin_name.lower()}:action2")
        return self.add_core_buttons()  # ⚡ Автоматически добавляет кнопки Ядра
```
- **Обновите plugin.py:**
```python
from .keyboards import PluginKeyboardBuilder  # 🔧 Добавьте импорт

def _get_main_keyboard(self):
    builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
    return builder.main_menu().build_markup()  # 🔧 Используйте ваш построитель
```

### 3. База данных - через models.py
- **Создайте структуру файлов**
```text
ваш_плагин/
├── config.py          # Обязательно
├── plugin.py          # Обязательно
├── __init__.py        # Обязательно
└── models.py          # Дополнительно -> Новый файл - модели данных для БЛ
```
- **Создайте файл models.py:** - таблица еудет создана автоматически при запуске!
```python
from databases.database_manager import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class UserData(Base):
    __tablename__ = "plugin_data"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    data = Column(String)
    created_at = Column(DateTime, default=datetime.now)
```

### 4. Сервисы - бизнес-логику в services/
- **Создайте структуру файлов**
```text
ваш_плагин/
├── config.py          # Обязательно
├── plugin.py          # Обязательно
├── __init__.py        # Обязательно
└── services/
    └── service.py     # Дополнительно -> Новый файл - внутренняя логика или интеграции с внешними сервисами
```
- **Создайте папку services/ и файл services/service.py:**
```python
from sqlalchemy import select
from databases import DatabaseManager
from ..models import UserData

class PluginService:
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    async def save_user_data(self, user_id: int, data: str):
        session = self.db.create_session()
        async with session:
            user_data = UserData(user_id=user_id, data=data)
            session.add(user_data)
            await session.commit()
            return user_data
    
    async def get_user_data(self, user_id: int):
        session = self.db.create_session()
        async with session:
            result = await session.execute(
                select(UserData).where(UserData.user_id == user_id)
            )
            return result.scalars().all()
```
- **Обновите plugin.py:**
```python
from .services.service import PluginService  # 🔧 Добавьте импорт

class Plugin(PluginBase):
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        # ... существующий код ...
        self.service = PluginService(db)  # 🔧 Добавьте сервис
    
    @router.callback_query(lambda c: c.data == f"{self.plugin_name.lower()}:save")
    async def save_data(callback: CallbackQuery):
        # 🔧 Используйте сервис
        await self.service.save_user_data(callback.from_user.id, "пример данных")
        await callback.message.answer("Данные сохранены!")
```

## Пример кастомных FSM и Middleware в плагинах
- **Создайте структуру файлов**
```text
ваш_плагин/
├── config.py        # Обязательно
├── plugin.py        # Обязательно
├── __init__.py      # Обязательно
├── fsm.py           # Дополнительно -> Новый файл - состояния
├── middleware.py    # Дополнительно -> Новый файл - middleware
└── handlers.py      # Дополнительно -> Новый файл или обновим существующий - handlers
```
- **FSM - Машина состояний (fsm.py)**
```python
from aiogram.fsm.state import State, StatesGroup

# 🚫 СИСТЕМНЫЙ КОД - НЕ ИЗМЕНЯТЬ структуру StatesGroup!
class PluginFSM(StatesGroup):
    """🔧 НАСТРОЙТЕ ЭТО - ваши состояния"""
    
    # 🔧 Добавьте свои состояния здесь:
    waiting_name = State()        # ← Ожидаем ввод имени
    waiting_age = State()         # ← Ожидаем ввод возраста  
    confirming_data = State()     # ← Подтверждение данных
    choosing_option = State()     # ← Выбор опции
```
- **Middleware (middleware.py)**
```python
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

class PluginAuthMiddleware(BaseMiddleware):
    """🔧 НАСТРОЙТЕ ЭТО - ваш middleware"""
    
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # 🔧 Ваша логика проверки доступа
        user = data.get("user")
        
        # Пример: проверяем есть ли пользователь в базе
        if not user:
            if isinstance(event, Message):
                await event.answer("❌ Сначала запустите бота командой /start")
            return
        
        # Пример: проверяем права доступа
        if user.role != "admin":
            if isinstance(event, Message):
                await event.answer("❌ У вас нет доступа к этому плагину")
            return
        
        # 🔧 Можете добавить свои проверки:
        # - Проверка подписки на канал
        # - Проверка баланса
        # - Проверка лимитов использования
        
        return await handler(event, data)
```
- **Обновленные обработчики (handlers.py)** - если вынесли их в отдельный файл
```python
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from .keyboards import PluginKeyboardBuilder
from .fsm import PluginFSM  # 🔧 Импортируем FSM
from .middleware import PluginAuthMiddleware  # 🔧 Импортируем middleware

class PluginHandlers:
    def __init__(self, config, plugin_name: str, db):
        self.config = config
        self.plugin_name = plugin_name

    def register(self, router: Router):
        # 🔧 Middleware для всех обработчиков плагина
        router.message.middleware(PluginAuthMiddleware(self.plugin_name))
        router.callback_query.middleware(PluginAuthMiddleware(self.plugin_name))
        
        # 🚪 Точка входа в плагин
        router.callback_query.register(
            self.entry_callback,
            F.data == f"plugin:{self.plugin_name}"
        )
        
        # 🔧 FSM обработчики - регистрируем ВСЕ состояния
        
        # Начало FSM сценария
        router.callback_query.register(
            self.start_fsm_flow,
            F.data == f"{self.plugin_name.lower()}:start_fsm"
        )
        
        # Обработка ввода имени
        router.message.register(
            self.process_name_input,
            StateFilter(PluginFSM.waiting_name)
        )
        
        # Обработка ввода возраста
        router.message.register(
            self.process_age_input, 
            StateFilter(PluginFSM.waiting_age)
        )
        
        # Подтверждение данных
        router.callback_query.register(
            self.confirm_data,
            F.data == f"{self.plugin_name.lower()}:confirm",
            StateFilter(PluginFSM.confirming_data)
        )
        
        # Отмена FSM
        router.callback_query.register(
            self.cancel_fsm,
            F.data == f"{self.plugin_name.lower()}:cancel"
        )

    async def entry_callback(self, callback: CallbackQuery):
        """🚪 Главное меню плагина"""
        keyboard = PluginKeyboardBuilder(self.config, self.plugin_name).main_menu().build_markup()
        await callback.message.edit_text(
            "Добро пожаловать! Выберите действие:",
            reply_markup=keyboard
        )

    async def start_fsm_flow(self, callback: CallbackQuery, state: FSMContext):
        """🔧 Начало FSM сценария"""
        await callback.message.answer(
            "📝 Введите ваше имя:",
            reply_markup=self._get_cancel_keyboard()
        )
        await state.set_state(PluginFSM.waiting_name)
        await callback.answer()

    async def process_name_input(self, message: Message, state: FSMContext):
        """🔧 Обработка ввода имени"""
        name = message.text
        
        # Сохраняем имя в состоянии
        await state.update_data(user_name=name)
        
        await message.answer(
            f"👤 Имя сохранено: {name}\n"
            f"📊 Теперь введите ваш возраст:",
            reply_markup=self._get_cancel_keyboard()
        )
        await state.set_state(PluginFSM.waiting_age)

    async def process_age_input(self, message: Message, state: FSMContext):
        """🔧 Обработка ввода возраста"""
        try:
            age = int(message.text)
            
            # Сохраняем возраст в состоянии
            await state.update_data(user_age=age)
            
            # Получаем все сохраненные данные
            data = await state.get_data()
            
            await message.answer(
                f"✅ Данные получены:\n"
                f"👤 Имя: {data['user_name']}\n"
                f"📊 Возраст: {data['user_age']}\n\n"
                f"Подтверждаете сохранение?",
                reply_markup=self._get_confirm_keyboard()
            )
            await state.set_state(PluginFSM.confirming_data)
            
        except ValueError:
            await message.answer("❌ Пожалуйста, введите число для возраста:")

    async def confirm_data(self, callback: CallbackQuery, state: FSMContext):
        """🔧 Подтверждение и сохранение данных"""
        data = await state.get_data()
        
        # 🔧 Здесь ваша логика сохранения в БД
        # await self.service.save_user_data(callback.from_user.id, data)
        
        await callback.message.answer(
            f"✅ Данные сохранены!\n"
            f"👤 Имя: {data['user_name']}\n"
            f"📊 Возраст: {data['user_age']}"
        )
        
        await state.clear()
        await callback.answer()

    async def cancel_fsm(self, callback: CallbackQuery, state: FSMContext):
        """🔧 Отмена FSM сценария"""
        await state.clear()
        await callback.message.answer("❌ Операция отменена")
        await callback.answer()

    def _get_cancel_keyboard(self):
        """🔧 Клавиатура для отмены FSM"""
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="❌ Отмена", 
                callback_data=f"{self.plugin_name.lower()}:cancel"
            )
        ]])

    def _get_confirm_keyboard(self):
        """🔧 Клавиатура для подтверждения"""
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="✅ Подтвердить", 
                callback_data=f"{self.plugin_name.lower()}:confirm"
            ),
            InlineKeyboardButton(
                text="❌ Отмена", 
                callback_data=f"{self.plugin_name.lower()}:cancel"
            )
        ]])
```
- **Обновленные клавиатуры (keyboards.py)**
```python
from core.keyboards import KeyboardBuilderBase
from .config import PluginSettings

class PluginKeyboardBuilder(KeyboardBuilderBase):
    def __init__(self, plugin_conf: PluginSettings, plugin_name: str):
        super().__init__()
        self.plugin_conf = plugin_conf
        self.plugin_name = plugin_name
    
    def main_menu(self):
        """🔧 Главное меню с FSM кнопкой"""
        self.keyboard = []
        self.add_button("🚀 Начать FSM сценарий", f"{self.plugin_name.lower()}:start_fsm")
        self.add_button("ℹ️ Информация", f"{self.plugin_name.lower()}:info")
        return self.add_core_buttons()
    
    def integrated_buttons(self):
        """🔧 Кнопки для главного меню бота"""
        self.keyboard = []
        self.add_button("📝 FSM Пример", f"plugin:{self.plugin_name}")
        return self
```
- **Обновленный plugin.py**
```python
from core.plugins.base import PluginBase
from core.config import ConfigManager
from aiogram import Router
from aiogram.types import InlineKeyboardButton
from databases import DatabaseManager
from .config import PluginSettings
from .handlers import PluginHandlers  # 🔧 Теперь используем отдельные handlers
from .keyboards import PluginKeyboardBuilder

class Plugin(PluginBase):
    def __init__(self, config: ConfigManager, db: DatabaseManager):
        self.config = config
        self.db = db
        self.plugin_name = self.get_name()
        self.settings: PluginSettings = config.load_plugin_config(self.plugin_name, PluginSettings)

    def get_router(self) -> Router:
        router = Router(name=self.plugin_name)
        PluginHandlers(self.settings, self.plugin_name, self.db).register(router)
        return router  # 🔧 Middleware теперь в handlers

    # ... остальные методы без изменений ...
    def get_integrated_buttons(self):
        builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
        return builder.integrated_buttons().keyboard

    def get_entry_button(self):
        builder = PluginKeyboardBuilder(self.settings, self.plugin_name)
        return builder.entry_button().keyboard

    def get_config(self):
        return PluginSettings

    def get_settings(self):
        return self.settings
```

### Итог - полноценный плагин с многошаговыми сценариями и системой контроля доступа!
#### FSM сценарий:
- **Пользователь нажимает** "Начать FSM сценарий"
- **Бот запрашивает имя** → сохраняет в состоянии
- **Бот запрашивает возраст** → сохраняет в состоянии
- **Бот показывает сводку** → ждет подтверждения
- **Данные сохраняются** → состояние очищается

#### Middleware:
- **Проверяет** авторизацию пользователя
- **Проверяет** права доступа к плагину
- **Работает** для всех сообщений и callback'ов плагина

#### Гибкая архитектура:
- **Каждый** компонент в отдельном файле
- **Легко** расширять и модифицировать
- **Четкое** разделение ответственности

## Обязательные компоненты
- **1. Конфигурация (config.py)**
```python
ENABLED: bool = True  # ⚠️ ОБЯЗАТЕЛЬНО

class PluginSettings(BaseSettings):  # ⚠️ ОБЯЗАТЕЛЬНО
    # Кастомные настройки плагина
    model_config = SettingsConfigDict(...)  # ⚠️ ОБЯЗАТЕЛЬНО
```
- **2. Главный класс (plugin.py)**
```python
class Plugin(PluginBase):  # ⚠️ ОБЯЗАТЕЛЬНО
    def __init__(self, config: ConfigManager, db: DatabaseManager):  # ⚠️ ОБЯЗАТЕЛЬНО
    def get_router(self) -> Router:  # ⚠️ ОБЯЗАТЕЛЬНО (абстрактный)
    def get_integrated_buttons(self) -> list[list[InlineKeyboardButton]]:  # ⚠️ ОБЯЗАТЕЛЬНО (абстрактный)
    def get_entry_button(self) -> list[list[InlineKeyboardButton]]:  # ⚠️ ОБЯЗАТЕЛЬНО (абстрактный)
    def get_config(self) -> type[BaseSettings]:  # ⚠️ ОБЯЗАТЕЛЬНО (абстрактный)
    def get_settings(self) -> BaseSettings:  # ⚠️ ОБЯЗАТЕЛЬНО (абстрактный)
```
- **3. Регистрация (__init__.py)**
```python
# ⚠️ ОБЯЗАТЕЛЬНО для авторегистрации
plugin_registry.register(lambda config, db: Plugin(config, db))
```

## Соглашения и стандарты
- **Именование callback данных:**
```python
# Вход в плагин
f"plugin:{plugin_name}"  # → "plugin:TEMPLATE"

# Действия внутри плагина  
f"{plugin_name.lower()}:action"  # → "template:bt1"
```

- **Доступ к ядру:**
```python
# Конфигурация
self.settings = config.load_plugin_config(self.plugin_name, PluginSettings)

# База данных
session = self.db.create_session()

# Логирование
router.message.middleware(PluginLoggerMiddleware(self.plugin_name))
```

### Шаблон разработки плагина:
- **Наследовать** от PluginBase
- **Реализовать** 5 абстрактных методов
- **Определить** PluginSettings с настройками
- **Создать** роутер с обработчиками
- **Построить** клавиатуры через PluginKeyboardBuilder
- **Зарегистрировать** фабрику в __init__.py
- **Следовать** соглашениям именования

### Структура клавиатур:
- **integrated_buttons()** - кнопки для интегрированного режима
- **entry_button()** - одна кнопка входа для entry режима
- **plugin_menu()** - внутреннее меню плагина

## Лицензия
Этот проект распространяется под лицензией MIT.

## Авторы
* Агамов Гамид • [GitHub](https://github.com/gambojo) • [Telegram](https://t.me/gambo_jo)
