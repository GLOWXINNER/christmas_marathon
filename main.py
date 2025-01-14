from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import validators
import re

# Замените TOKEN на токен вашего бота
BOT_TOKEN = "7715066464:AAES118WE5-c6z9gbsBhUpO8bkpUOjXDfkg"
CHANNEL_ID = "@christmas_marathon"  # Укажите ID вашего канала
ADMIN_IDS = [6402145279]  # Укажите ID админов

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class PostCreation(StatesGroup):
    waiting_for_text = State()
    waiting_for_media = State()
    waiting_for_action = State()
    waiting_for_button = State()

def escape_markdown(text: str) -> str:
    """Экранирует специальные символы для Markdown V2, кроме тех, что используются для форматирования."""
    return re.sub(r'([_\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("✉️ Опубликовать пост"))
        keyboard.add(KeyboardButton("🔖 Создать статью", request_contact=False))
        keyboard.add(
            KeyboardButton("🗂 Материалы"),
            KeyboardButton("🔗 Социальные сети"),
            KeyboardButton("❓ Поддержка")
        )
        text = (
            "Вы администратор! ✅\n\n"
            "🌟 Добро пожаловать в \"Рождественский Марафон\", Вашего спутника для изучения православного праздника Рождество!\n\n"
            "Вы можете выбрать один из следующих пунктов:\n\n"
            "🗂 **Материалы** - Погрузитесь в актуальные образовательные материалы.\n\n"
            "🔗 **Социальные сети** - Присоединяйтесь к нам.\n\n"
            "❓ **Поддержка** - Задавайте интересующие Вас вопросы.\n\n"
            "Выберите интересующий Вас пункт, и мы начнем Ваше увлекательное путешествие! ✨"
        )
        await message.answer(
            escape_markdown(text),
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton("🗂 Материалы"),
            KeyboardButton("🔗 Социальные сети"),
            KeyboardButton("❓ Поддержка")
        )
        text = (
            "🌟 Добро пожаловать в \"Рождественский Марафон\", Вашего спутника для изучения православного праздника Рождество!\n\n"
            "Вы можете выбрать один из следующих пунктов:\n\n"
            "🗂 **Материалы** - Погрузитесь в актуальные образовательные материалы.\n\n"
            "🔗 **Социальные сети** - Присоединяйтесь к нам.\n\n"
            "❓ **Поддержка** - Задавайте интересующие Вас вопросы.\n\n"
            "Выберите интересующий Вас пункт, и мы начнем Ваше увлекательное путешествие! ✨"
        )
        await message.answer(
            escape_markdown(text),
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )

@dp.message_handler(lambda message: message.text == "🗂 Материалы", state='*')
async def create_article(message: types.Message):
    article_links = [
        ("Толкование царских часов Сочельника", "https://telegra.ph/Tolkovanie-carskih-chasov-Sochelnika-01-06"),
        ("Десять пророчеств о Рождестве Христовом", "https://telegra.ph/Desyat-prorochestv-o-Rozhdestve-Hristovom-01-06"),
        ("Рождество Христово глазами новомучеников", "https://telegra.ph/Rozhdestvo-Hristovo-glazami-novomuchenikov-01-06"),
        ("Что было бы, если бы не было Рождества Христова", "https://telegra.ph/CHto-bylo-by-esli-by-ne-bylo-Rozhdestva-Hristova-01-06"),
        ("Рождество Христово в живописи", "https://telegra.ph/Rozhdestvo-Hristovo-v-zhivopisi-01-06"),
        ("Толкование главных песнопений службы Рождества", "https://telegra.ph/Tolkovanie-glavnyh-pesnopenij-sluzhby-Rozhdestva-01-06"),
        ("Как разум, сердце и политика готовились к Первому Пришествию Христа", "https://telegra.ph/Kak-razum-serdce-i-politika-gotovilis-k-Pervomu-Prishestviyu-Hrista-01-06"),
        ("Защитник Рождества", "https://telegra.ph/Zashchitnik-Rozhdestva-01-06"),
        ("Приготовление мира к пришествию Христа", "https://telegra.ph/Prigotovlenie-mira-k-prishestviyu-Hrista-01-06"),
        ("Жизнь Иисуса Христа в пророчествах Ветхого Завета", "https://telegra.ph/ZHizn-Iisusa-Hrista-v-prorochestvah-Vethogo-Zaveta-01-06"),
        ("О чем надо думать на святках", "https://telegra.ph/O-chem-nado-dumat-na-svyatkah-01-06"),
        ("Курс лекций о Рождестве Христовом", "https://teletype.in/@glowxinner/nLWAm3kw0KP"),
        ("За несколько минут до креста Христос открыл зачем Он Родился.", "https://telegra.ph/Za-neskolko-minut-do-kresta-Hristos-otkryl-zachem-On-Rodilsya-01-09"),
        ("Рождество и Голгофа", "https://telegra.ph/Rozhdestvo-i-Golgofa-01-09"),
        ("Григорий Богослов. Слово 38 на Рождество Христово", "https://teletype.in/@glowxinner/5UwkloDAHkH"),
        ("Лев Великий. Слова на Рождество Христово", "https://teletype.in/@glowxinner/D2Jw84Xehzf"),
    ]

    markup = InlineKeyboardMarkup()
    for title, link in article_links:
        markup.add(InlineKeyboardButton(title, url=link))
    
    await message.answer("📚 Выберите интересующую Вас тему:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "🔗 Социальные сети", state='*')
async def create_article(message: types.Message):
    article_link = "https://t.me/christmas_marathon"
    article_link2 = "https://www.youtube.com/channel/UCHCU9CbRf859DheRK_o1vNA"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Telegram канал", url=article_link))
    markup.add(InlineKeyboardButton("YouTube", url=article_link2))
    await message.answer("📱 Социальные сети", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "❓ Поддержка", state='*')
async def support_handler(message: types.Message):
    support_link = "https://t.me/glowxinner"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Написать в поддержку", url=support_link))
    await message.answer("Если у вас есть вопросы, напишите нам в поддержку:", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "🔖 Создать статью" and message.from_user.id in ADMIN_IDS, state='*')
async def create_article(message: types.Message):
    article_link = "https://telegra.ph/"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Перейти к созданию статьи", url=article_link))
    await message.answer("Нажмите на кнопку ниже, чтобы создать статью в Telegraph:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "✉️ Опубликовать пост" and message.from_user.id in ADMIN_IDS, state='*')
async def start_post_creation(message: types.Message):
    await message.answer("Введите текст поста:")
    await PostCreation.waiting_for_text.set()

@dp.message_handler(state=PostCreation.waiting_for_text)
async def receive_post_text(message: types.Message, state: FSMContext):
    escaped_text = escape_markdown(message.text)
    await state.update_data(post_text=escaped_text, buttons=[], media=None)
    await message.answer("Теперь отправьте изображение или видео \n (или нажмите /skip, чтобы пропустить):")
    await PostCreation.waiting_for_media.set()

@dp.message_handler(commands=['skip'], state=PostCreation.waiting_for_media)
async def skip_media(message: types.Message, state: FSMContext):
    await send_post_preview(message, state)

@dp.message_handler(content_types=['photo', 'video'], state=PostCreation.waiting_for_media)
async def receive_media(message: types.Message, state: FSMContext):
    if message.photo:
        media = message.photo[-1].file_id
        media_type = 'photo'
    elif message.video:
        media = message.video.file_id
        media_type = 'video'
    else:
        await message.answer("Пожалуйста, отправьте изображение или видео.")
        return

    await state.update_data(media={"type": media_type, "file_id": media})
    await send_post_preview(message, state)

async def send_post_preview(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data['post_text']
    buttons = data['buttons']
    media = data['media']

    if media:
        if media['type'] == 'photo':
            await bot.send_photo(chat_id=message.chat.id, photo=media['file_id'], caption=text, parse_mode=ParseMode.MARKDOWN_V2)
        elif media['type'] == 'video':
            await bot.send_video(chat_id=message.chat.id, video=media['file_id'], caption=text, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Добавить кнопку", callback_data="add_button"),
        InlineKeyboardButton("Отредактировать сообщение", callback_data="edit_message"),
        InlineKeyboardButton("Опубликовать", callback_data="publish")
    )

    await message.answer("Выберите действие:", reply_markup=markup)
    await PostCreation.waiting_for_action.set()

@dp.callback_query_handler(state=PostCreation.waiting_for_action)
async def handle_action(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data
    if action == "add_button":
        await callback_query.message.answer("Введите текст и URL кнопки через запятую \n например: Google, https://google.com")
        await PostCreation.waiting_for_button.set()
    elif action == "edit_message":
        await callback_query.message.answer("Введите новый текст поста:")
        await PostCreation.waiting_for_text.set()
    elif action == "publish":
        await publish_post(callback_query.message, state)

@dp.message_handler(state=PostCreation.waiting_for_button)
async def add_inline_button(message: types.Message, state: FSMContext):
    try:
        text, url = map(str.strip, message.text.split(",", 1))
        if not validators.url(url):
            await message.answer("Некорректный URL. Убедитесь, что он начинается с 'http://' или 'https://'. Попробуйте снова:")
            return
        async with state.proxy() as data:
            data['buttons'].append({"text": text, "url": url})
        await message.answer("Кнопка добавлена!")
        await send_post_preview(message, state)
    except ValueError:
        await message.answer("Некорректный формат. Введите текст и URL через запятую, например: 'Google, https://google.com'")

async def publish_post(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        text = data['post_text']
        buttons = data['buttons']
        media = data['media']

        markup = InlineKeyboardMarkup(row_width=1)
        for button in buttons:
            markup.add(InlineKeyboardButton(button['text'], url=button['url']))

        if media:
            if media['type'] == 'photo':
                await bot.send_photo(chat_id=CHANNEL_ID, photo=media['file_id'], caption=text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN_V2)
            elif media['type'] == 'video':
                await bot.send_video(chat_id=CHANNEL_ID, video=media['file_id'], caption=text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN_V2)

        await message.answer("Пост опубликован!")
        await state.finish()
    except Exception as e:
        await message.answer(f"Ошибка при публикации: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
