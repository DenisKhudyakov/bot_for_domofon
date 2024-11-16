from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import TELEPHONE, DEFAULT_COMMANDS
from bot.database.crud import add_user, get_all_telephones
from bot.services import open_the_door, get_photo

router = Router()


class UserRegisterState(StatesGroup):
    """
    Класс состояний
    """
    waiting_for_name = State()
    waiting_for_phone = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(UserRegisterState.waiting_for_name)
    await message.answer(f'Привет {message.from_user.full_name},\nВведите Ваше имя для регистрации')


@router.message(F.text, UserRegisterState.waiting_for_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserRegisterState.waiting_for_phone)
    await message.answer('Введите номер телефона, для регистрации пользователя, в формате: 74563258825')


@router.message(F.text, UserRegisterState.waiting_for_phone)
async def enter_phone(message: Message, state: FSMContext):
    phone = message.text
    user_data = await state.get_data()
    name = user_data['name']
    await add_user(username=name, telephone=phone)
    await state.clear()
    await message.answer('Поздравляем регистрация завершена')
    await message.answer('Справка команда: /help')


@router.message(Command('open_the_door'))
async def handlers_open_door(message: Message):
    telephones = await get_all_telephones()
    if TELEPHONE not in telephones:
        await message.answer('данный пользователь не может открывать дверь, т.к. он не является одобренным')
    else:
        await open_the_door()
        await message.answer('Дверь открыта')


@router.message(Command('check_photo'))
async def handlers_check_photo(message: Message):
    telephones = await get_all_telephones()
    if TELEPHONE not in telephones:
        await message.answer('данный пользователь не может просматривать фото с домофона'
                             ', т.к. он не является одобренным')
    else:
        link = await get_photo()
        await message.answer(f'Высылаю ссылку на фото:\n{link}')


@router.message(Command('help'))
async def handlers_help(message: Message):
    text = [f"{commands} - {desk}\n" for commands, desk in DEFAULT_COMMANDS]
    await message.answer("Список команд:" + "\n".join(text))


