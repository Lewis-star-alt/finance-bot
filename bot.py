# bot.py

import asyncio
import logging
import traceback  # для вывода полного текста ошибки

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Все импорты проекта — наверху, чтобы при ошибке бот не запустился вообще
# и ты сразу увидел проблему в консоли
from config import TOKEN
from database.database import init_db, async_session  # убедись, что database/__init__.py экспортирует оба
from database.models import Transaction

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ==================== Хендлеры ====================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Проверка, что бот вообще жив.
    Если /start работает — проблема была в хендлере test.
    """
    await message.answer(
        "👋 Бот работает!\n\n"
        "Попробуй: <b>/test</b> — проверка записи в БД"
    )


@dp.message(Command("test"))
async def cmd_test(message: Message):
    """
    Тестовый хендлер с защитой от ошибок.
    Если что-то сломается — отправит тебе текст ошибки в Telegram.
    """
    try:
        # Работаем с БД
        async with async_session() as session:
            trans = Transaction(
                user_id=message.from_user.id,
                amount=-150,
                category="еда",
                description="тестовый кофе",
            )
            session.add(trans)
            await session.commit()
            # refresh нужен, чтобы получить auto-increment id из БД
            await session.refresh(trans)

            await message.answer(
                f"✅ Записано!\n"
                f"ID: <code>{trans.id}</code>\n"
                f"Сумма: {trans.amount} ₽\n"
                f"Категория: {trans.category}"
            )

    except Exception as e:
        # Если упало — отправляем ошибку прямо в чат, чтобы видеть
        error_text = f"❌ Ошибка:\n<code>{type(e).__name__}: {e}</code>\n\n"
        error_text += f"<pre>{traceback.format_exc()}</pre>"
        await message.answer(error_text)
        # И дублируем в консоль
        logging.exception("Ошибка в /test")


# ==================== Запуск ====================

async def main():
    # Создаём таблицы
    await init_db()
    # Запускаем бесконечный цикл
    await dp.start_polling(bot)
    # Закрываем сессию при остановке (Ctrl+C)
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())