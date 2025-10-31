"""
Модуль состояний FSM (Finite State Machine)
Содержит состояния для многошаговых сценариев
"""

from aiogram.fsm.state import State, StatesGroup


class PluginFSM(StatesGroup):
    """
    Группа состояний FSM для плагина
    Наследует: StatesGroup (aiogram)
    Используется для: управления многошаговыми диалогами

    Пример использования:
        await state.set_state(PluginFSM.waiting_input)
        current_state = await state.get_state()
    """

    waiting_input = State()
    """
    Состояние ожидания ввода пользователя
    Назначение: ожидание текстового ввода
    Пример сценария: бот запросил имя → переходит в waiting_input
    """

    choosing_feature = State()
    """
    Состояние выбора функции
    Назначение: ожидание выбора из вариантов
    Пример сценария: показ меню с опциями → ожидание выбора
    """

    confirming_action = State()
    """
    Состояние подтверждения действия
    Назначение: ожидание подтверждения операции
    Пример сценария: показать "Вы уверены?" → ожидать подтверждения
    """
