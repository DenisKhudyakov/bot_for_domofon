from dotenv import load_dotenv, find_dotenv
import os

if not find_dotenv():
    exit('File .env not found')
else:
    load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
DATABASE_URL=os.getenv('DATABASE_URL')
SECRET_KEY=os.getenv('SECRET_KEY')

DEFAULT_COMMANDS = (
    ("/start", "Запуск бота + регистрация пользователя"),
    (
        "/check_photo",
        "Просмотр фото с домофона",
    ),
    (
        "/open_the_door",
        "Открыть дверь в домофоне",
    ),
    ("/clear", "Очистить базу данных с пользователями"),
)