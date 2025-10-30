from aiogram.fsm.state import State, StatesGroup

class PluginFSM(StatesGroup):
    """Состояния FSM для плагина-шаблона"""
    waiting_input = State()
    choosing_feature = State()
    confirming_action = State()
