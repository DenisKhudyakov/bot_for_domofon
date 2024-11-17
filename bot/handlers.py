from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from bot.config import DEFAULT_COMMANDS
from bot.database.crud import add_user, get_all_telephones, get_telephone, clear_database
from bot.services import open_the_door, get_photo

router = Router()


class UserRegisterState(StatesGroup):
    """
    Класс состояний
    """
    waiting_for_phone = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(UserRegisterState.waiting_for_phone)
    await message.answer(f'Привет {message.from_user.full_name}')
    await message.answer('Введите номер телефона, для регистрации пользователя, в формате: 74563258825')


@router.message(F.text, UserRegisterState.waiting_for_phone)
async def enter_name(message: Message, state: FSMContext):
    phone = message.text
    name = message.from_user.full_name
    try:
        await add_user(username=name, telephone=phone)
        await message.answer('Поздравляем регистрация завершена')
        await message.answer('Справка команда: /help')

    except IntegrityError:
        await message.answer('Данный пользователь уже существует')
        await message.answer('Справка команда: /help')
    finally:
        await state.clear()


@router.message(Command('open_the_door'))
async def handlers_open_door(message: Message):
    telephones = await get_telephone(message.from_user.full_name)
    print(telephones)
    print(type(telephones))
    try:
        await open_the_door(telephones)
        await message.answer('Дверь открыта')
    except ValueError:
        await message.answer('данный пользователь не может открывать дверь, т.к. он не является одобренным')


@router.message(Command('check_photo'))
async def handlers_check_photo(message: Message):
    telephones = await get_telephone(message.from_user.full_name)
    try:
        link = await get_photo(telephones)
        await message.answer(f'Высылаю ссылку на фото:\n{link}')
    except ValueError:
        await message.answer('данный пользователь не может просматривать фото с домофона'
                             ', т.к. он не является одобренным')


@router.message(Command('help'))
async def handlers_help(message: Message):
    text = [f"{commands} - {desk}\n" for commands, desk in DEFAULT_COMMANDS]
    await message.answer("Список команд:" + "\n".join(text))


@router.message(Command('clear'))
async def handlers_clear(message: Message):
    await clear_database()
    await message.answer('База данных очищена')
