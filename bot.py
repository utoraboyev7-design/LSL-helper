import asyncio
import json
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from languages.ru.texts import TEXTS as RU_TEXTS
from languages.ru.subjects import SUBJECTS as RU_SUBJECTS

from languages.uz.texts import TEXTS as UZ_TEXTS
from languages.uz.subjects import SUBJECTS as UZ_SUBJECTS

from languages.en.texts import TEXTS as EN_TEXTS
from languages.en.subjects import SUBJECTS as EN_SUBJECTS


# ============================================================
# НАСТРОЙКИ
# ============================================================



BOT_TOKEN = os.getenv("BOT_TOKEN")
DEVELOPER_PIN = os.getenv("DEVELOPER_PIN")

DATA_FILE = "users.json"

dp = Dispatcher()

# ============================================================
# ЯЗЫКИ
# ============================================================

LANGUAGES = {
    "🇷🇺 Русский": "ru",
    "🇺🇿 O‘zbekcha": "uz",
    "🇬🇧 English": "en",
}

TEXTS = {
    "ru": RU_TEXTS,
    "uz": UZ_TEXTS,
    "en": EN_TEXTS,
}

SUBJECTS = {
    "ru": RU_SUBJECTS,
    "uz": UZ_SUBJECTS,
    "en": EN_SUBJECTS,
}


# ============================================================
# КЛАССЫ
# ============================================================

CLASSES = {
    "1А", "1Б",
    "2А", "2Б",
    "3А", "3Б",
    "4А", "4Б",
    "5А", "5Б",
    "6А", "6Б",
    "7А", "7Б",
    "8А",
    "9А", "9Б",
    "10А", "10Б",
    "11А"
}


# ============================================================
# РАСПИСАНИЕ
# ============================================================

SCHEDULES = {

    "6Б": {
        "Понедельник": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Tasviriy san'at"),
            ("11:15–12:00", "Nutq madaniyati"),
            ("13:00–13:45", "Adabiyot"),
            ("13:55–14:40", "Tarix"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Matematika"),
        ],
        "Вторник": [
            ("8:30–9:15", "Ona tili"),
            ("9:25–10:10", "Nutq madaniyati"),
            ("10:20–11:05", "Science"),
            ("11:15–12:00", "Adabiyot"),
            ("13:00–13:45", "Texnologiya"),
            ("13:55–14:40", "Texnologiya"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Среда": [
            ("8:30–9:15", "Mat. kurs"),
            ("9:25–10:10", "Mat. kurs"),
            ("10:20–11:05", "Ona tili"),
            ("11:15–12:00", "Tarbiya"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Rus tili"),
            ("15:45–16:30", "Tarix"),
        ],
        "Четверг": [
            ("8:30–9:15", "Matematika"),
            ("9:25–10:10", "Matematika"),
            ("10:20–11:05", "Ona tili"),
            ("11:15–12:00", "Science"),
            ("13:00–13:45", "Nutq madaniyati"),
            ("13:55–14:40", "Rus tili"),
            ("14:50–15:35", "Informatika"),
            ("15:45–16:30", "Informatika"),
        ],
        "Пятница": [
            ("8:30–9:15", "Ona tili"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Chet tili"),
            ("11:15–12:00", "Science"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Musiqa"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Суббота": [
            ("8:30–9:15", "Jis/tar"),
            ("9:25–10:10", "Jis/tar"),
            ("10:20–11:05", "Informatika"),
            ("11:15–12:00", "Informatika"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Matematika"),
        ],
    },

    "7А": {
        "Понедельник": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Ona tili"),
            ("11:15–12:00", "Tarbiya"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Geografiya"),
            ("15:45–16:30", "Rus tili"),
        ],
        "Вторник": [
            ("8:30–9:15", "Kimyo"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Chet tili"),
            ("11:15–12:00", "Mat. kurs"),
            ("13:00–13:45", "Mat. kurs"),
            ("13:55–14:40", "Tarix"),
            ("14:50–15:35", "Geografiya"),
            ("15:45–16:30", "Matematika"),
        ],
        "Среда": [
            ("8:30–9:15", "Chet tili"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Adabiyot"),
            ("11:15–12:00", "Biologiya"),
            ("13:00–13:45", "Informatika"),
            ("13:55–14:40", "Informatika"),
            ("14:50–15:35", "Matematika"),
            ("15:45–16:30", "Matematika"),
        ],
        "Четверг": [
            ("8:30–9:15", "Biologiya"),
            ("9:25–10:10", "Ona tili"),
            ("10:20–11:05", "Fizika"),
            ("11:15–12:00", "Adabiyot"),
            ("13:00–13:45", "Jis/tar"),
            ("13:55–14:40", "Jis/tar"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Пятница": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Fizika"),
            ("11:15–12:00", "Rus tili"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Tarix"),
            ("14:50–15:35", "Texnologiya"),
            ("15:45–16:30", "Texnologiya"),
        ],
        "Суббота": [
            ("8:30–9:15", "Tarix"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Chet tili"),
            ("11:15–12:00", "Kimyo"),
            ("13:00–13:45", "Matematika"),
            ("13:55–14:40", "Matematika"),
            ("14:50–15:35", "Ona tili"),
            ("15:45–16:30", "Chizmachilik / Musiqa"),
        ],
    },

    "8А": {
        "Понедельник": [
            ("8:30–9:15", "Adabiyot"),
            ("9:25–10:10", "Geografiya"),
            ("10:20–11:05", "Algebra"),
            ("11:15–12:00", "Geometriya"),
            ("13:00–13:45", "Informatika"),
            ("13:55–14:40", "Informatika"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Вторник": [
            ("8:30–9:15", "Adabiyot"),
            ("9:25–10:10", "Algebra"),
            ("10:20–11:05", "Geometriya"),
            ("11:15–12:00", "Kimyo"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Chet tili"),
            ("14:50–15:35", "Ona tili"),
            ("15:45–16:30", "Iqtisod / Geografiya"),
        ],
        "Среда": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Tarbiya"),
            ("11:15–12:00", "Mat. kurs"),
            ("13:00–13:45", "Mat. kurs"),
            ("13:55–14:40", "Huquq"),
            ("14:50–15:35", "Chet tili"),
            ("15:45–16:30", "Chet tili"),
        ],
        "Четверг": [
            ("8:30–9:15", "Chet tili"),
            ("9:25–10:10", "Chet tili"),
            ("10:20–11:05", "Kimyo"),
            ("11:15–12:00", "Chet tili"),
            ("13:00–13:45", "Chet tili"),
            ("13:55–14:40", "Ona tili"),
            ("14:50–15:35", "Chizmachilik / Tarix"),
            ("15:45–16:30", "Texnologiya"),
        ],
        "Пятница": [
            ("8:30–9:15", "Rus tili"),
            ("9:25–10:10", "Fizika"),
            ("10:20–11:05", "Algebra"),
            ("11:15–12:00", "Tarix"),
            ("13:00–13:45", "Sinf soati"),
            ("13:55–14:40", "Fizika"),
            ("14:50–15:35", "Biologiya"),
            ("15:45–16:30", "Algebra"),
        ],
        "Суббота": [
            ("8:30–9:15", "Informatika"),
            ("9:25–10:10", "Informatika"),
            ("10:20–11:05", "Rus tili"),
            ("11:15–12:00", "Tarix"),
            ("13:00–13:45", "Ona tili"),
            ("13:55–14:40", "Biologiya"),
            ("14:50–15:35", "Jis/tar"),
            ("15:45–16:30", "Jis/tar"),
        ],
    },
}


# ============================================================
# ДНИ НЕДЕЛИ
# ============================================================

DAY_NAMES = {
    "ru": {
        "Понедельник": "Понедельник",
        "Вторник": "Вторник",
        "Среда": "Среда",
        "Четверг": "Четверг",
        "Пятница": "Пятница",
        "Суббота": "Суббота",
    },

    "uz": {
        "Понедельник": "Dushanba",
        "Вторник": "Seshanba",
        "Среда": "Chorshanba",
        "Четверг": "Payshanba",
        "Пятница": "Juma",
        "Суббота": "Shanba",
    },

    "en": {
        "Понедельник": "Monday",
        "Вторник": "Tuesday",
        "Среда": "Wednesday",
        "Четверг": "Thursday",
        "Пятница": "Friday",
        "Суббота": "Saturday",
    },
}


# ============================================================
# РАБОТА С ПОЛЬЗОВАТЕЛЯМИ
# ============================================================

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


users = load_users()


def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


def create_user(user_id, tg_user=None):
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "language": None,
            "class": None,
            "role": "student",
            "banned": False,
            "username": None,
            "first_name": None,
            "last_name": None
        }

    user = users[user_id]
    user.setdefault("language", None)
    user.setdefault("class", None)
    user.setdefault("role", "student")
    user.setdefault("banned", False)
    user.setdefault("username", None)
    user.setdefault("first_name", None)
    user.setdefault("last_name", None)

    if tg_user is not None:
        user["username"] = tg_user.username
        user["first_name"] = tg_user.first_name
        user["last_name"] = tg_user.last_name

    save_users()


def get_language(user_id):
    user = users.get(str(user_id), {})
    language = user.get("language")
    if language in TEXTS:
        return language
    return None


def get_class(user_id):
    return users.get(str(user_id), {}).get("class")


def get_role(user_id):
    return users.get(str(user_id), {}).get("role", "student")


def is_banned(user_id):
    return users.get(str(user_id), {}).get("banned", False)


def is_developer(user_id):
    return get_role(user_id) == "developer"


# ============================================================
# МЕНЮ ЯЗЫКА
# ============================================================

language_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇺🇿 O‘zbekcha")],
        [KeyboardButton(text="🇬🇧 English")],
    ],
    resize_keyboard=True
)


# ============================================================
# МЕНЮ КЛАССОВ
# ============================================================

class_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1А"), KeyboardButton(text="1Б")],
        [KeyboardButton(text="2А"), KeyboardButton(text="2Б")],
        [KeyboardButton(text="3А"), KeyboardButton(text="3Б")],
        [KeyboardButton(text="4А"), KeyboardButton(text="4Б")],
        [KeyboardButton(text="5А"), KeyboardButton(text="5Б")],
        [KeyboardButton(text="6А"), KeyboardButton(text="6Б")],
        [KeyboardButton(text="7А"), KeyboardButton(text="7Б")],
        [KeyboardButton(text="8А")],
        [KeyboardButton(text="9А"), KeyboardButton(text="9Б")],
        [KeyboardButton(text="10А"), KeyboardButton(text="10Б")],
        [KeyboardButton(text="11А")],
    ],
    resize_keyboard=True
)


# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

def main_menu(user_id):

    language = get_language(user_id)
    class_name = get_class(user_id)

    t = TEXTS[language]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t["schedule"]),
                KeyboardButton(text=t["books"]),
            ],
            [
                KeyboardButton(text=t["homework"]),
                KeyboardButton(text=t["news"]),
            ],
            [
                KeyboardButton(text=t["contacts"]),
                KeyboardButton(text=t["help"]),
            ],
            [
                KeyboardButton(
                    text=t["change_class"].format(
                        class_name=class_name
                    )
                )
            ],
            [
                KeyboardButton(text=t["language"])
            ],
        ],
        resize_keyboard=True
    )


# ============================================================
# РЕЖИМ РАЗРАБОТЧИКА
# ============================================================

class DeveloperLogin(StatesGroup):
    waiting_for_pin = State()


developer_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👥 Пользователи"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="🔎 Найти пользователя")],
        [KeyboardButton(text="🚪 Выйти из панели")]
    ],
    resize_keyboard=True
)


def developer_user_card(user_id, user):
    username = f"@{user.get('username')}" if user.get("username") else "—"
    full_name = " ".join(
        part for part in [user.get("first_name"), user.get("last_name")] if part
    ) or "—"
    return (
        f"👤 {full_name}\n"
        f"🆔 {user_id}\n"
        f"🔗 {username}\n"
        f"🎓 Класс: {user.get('class') or '—'}\n"
        f"🌐 Язык: {user.get('language') or '—'}\n"
        f"🔑 Роль: {user.get('role', 'student')}\n"
        f"🚫 Бан: {'да' if user.get('banned', False) else 'нет'}"
    )


@dp.message(Command("panel"))
async def open_panel(message: Message, state: FSMContext):
    user_id = message.from_user.id
    create_user(user_id, message.from_user)

    if is_banned(user_id):
        await message.answer("🚫 Доступ к боту для вашего аккаунта заблокирован.")
        return

    if is_developer(user_id):
        await message.answer("👑 Режим разработчика", reply_markup=developer_menu)
        return

    if not DEVELOPER_PIN:
        await message.answer("⚠️ DEVELOPER_PIN не настроен на сервере.")
        return

    await state.set_state(DeveloperLogin.waiting_for_pin)
    await message.answer(
        "🔐 Введите PIN разработчика:",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(DeveloperLogin.waiting_for_pin)
async def developer_pin_login(message: Message, state: FSMContext):
    if message.text == DEVELOPER_PIN:
        user_id = str(message.from_user.id)
        create_user(user_id, message.from_user)
        users[user_id]["role"] = "developer"
        save_users()
        await state.clear()
        await message.answer(
            "✅ Доступ подтверждён.\n\n👑 Режим разработчика",
            reply_markup=developer_menu
        )
        return

    await message.answer("❌ Неверный PIN. Попробуйте ещё раз или отправьте /start для выхода.")


@dp.message(F.text == "📊 Статистика")
async def developer_stats(message: Message):
    if not is_developer(message.from_user.id):
        return

    total = len(users)
    banned = sum(1 for user in users.values() if user.get("banned", False))
    teachers = sum(1 for user in users.values() if user.get("role") == "teacher")
    admins = sum(1 for user in users.values() if user.get("role") == "admin")

    await message.answer(
        "📊 Статистика бота\n\n"
        f"👥 Пользователей: {total}\n"
        f"👨‍🏫 Учителей: {teachers}\n"
        f"🛡 Администраторов: {admins}\n"
        f"🚫 Заблокировано: {banned}"
    )


@dp.message(F.text == "👥 Пользователи")
async def developer_users(message: Message):
    if not is_developer(message.from_user.id):
        return

    if not users:
        await message.answer("Пользователей пока нет.")
        return

    items = list(users.items())
    await message.answer(f"👥 Всего пользователей: {len(items)}")

    # Первая версия: показываем до 20 пользователей за один запрос.
    for user_id, user in items[:20]:
        await message.answer(developer_user_card(user_id, user))

    if len(items) > 20:
        await message.answer(
            "ℹ️ Показаны первые 20. Позже добавим страницы и кнопки управления."
        )


@dp.message(F.text == "🚪 Выйти из панели")
async def developer_logout(message: Message):
    if not is_developer(message.from_user.id):
        return

    language = get_language(message.from_user.id)
    class_name = get_class(message.from_user.id)

    if language and class_name:
        await message.answer(
            "🚪 Панель закрыта.",
            reply_markup=main_menu(message.from_user.id)
        )
    elif language:
        await message.answer("🚪 Панель закрыта.", reply_markup=class_menu)
    else:
        await message.answer("🚪 Панель закрыта.", reply_markup=language_menu)


# ============================================================
# START
# ============================================================

@dp.message(CommandStart())
async def start(message: Message):

    user_id = message.from_user.id

    create_user(user_id, message.from_user)

    if is_banned(user_id):
        await message.answer("🚫 Доступ к боту для вашего аккаунта заблокирован.")
        return

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:

        await message.answer(
            "🏫 Welcome / Добро пожаловать / Xush kelibsiz!\n\n"
            "🌐 Выбери язык / Choose your language / Tilni tanlang:",
            reply_markup=language_menu
        )
        return

    if not class_name:

        await message.answer(
            TEXTS[language]["choose_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        f"🏫 {class_name}\n\n"
        f"{TEXTS[language]['choose_class']}",
        reply_markup=main_menu(user_id)
    )


# ============================================================
# ВЫБОР ЯЗЫКА
# ============================================================

@dp.message(F.text.in_(LANGUAGES.keys()))
async def select_language(message: Message):

    user_id = message.from_user.id

    create_user(user_id)

    language = LANGUAGES[message.text]

    users[str(user_id)]["language"] = language

    save_users()

    class_name = get_class(user_id)

    if not class_name:

        await message.answer(
            TEXTS[language]["choose_class"],
            reply_markup=class_menu
        )

    else:

        await message.answer(
            TEXTS[language]["welcome"].split("\n\n")[0],
            reply_markup=main_menu(user_id)
        )


# ============================================================
# ВЫБОР КЛАССА
# ============================================================

@dp.message(F.text.in_(CLASSES))
async def select_class(message: Message):

    user_id = message.from_user.id

    create_user(user_id)

    language = get_language(user_id)

    if not language:

        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    users[str(user_id)]["class"] = message.text

    save_users()

    await message.answer(
        TEXTS[language]["class_selected"].format(
            class_name=message.text
        ),
        reply_markup=main_menu(user_id)
    )


# ============================================================
# СМЕНА КЛАССА
# ============================================================

@dp.message(F.text.startswith("🎓"))
async def change_class(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    await message.answer(
        TEXTS[language]["change_class_text"].format(
            class_name=class_name
        ),
        reply_markup=class_menu
    )


# ============================================================
# СМЕНА ЯЗЫКА
# ============================================================

@dp.message(
    F.text.in_({
        "🌐 Язык: Русский",
        "🌐 Til: O‘zbekcha",
        "🌐 Language: English"
    })
)
async def change_language(message: Message):

    await message.answer(
        "🌐 Выбери язык / Choose language / Tilni tanlang:",
        reply_markup=language_menu
    )


# ============================================================
# РАСПИСАНИЕ
# ============================================================

async def send_schedule(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    if class_name not in SCHEDULES:

        await message.answer(
            TEXTS[language]["no_schedule"].format(
                class_name=class_name
            )
        )
        return

    schedule = SCHEDULES[class_name]

    text = TEXTS[language]["schedule_title"].format(
        class_name=class_name
    )

    for day, lessons in schedule.items():

        text += "\n\n━━━━━━━━━━━━━━\n"

        text += f"📌 {DAY_NAMES[language][day]}\n\n"

        for number, (time, subject) in enumerate(
            lessons,
            start=1
        ):

            translated_subject = SUBJECTS[language].get(
                subject,
                subject
            )

            text += (
                f"{number}. "
                f"{time} — "
                f"{translated_subject}\n"
            )

    await message.answer(text)


# ============================================================
# КНОПКА РАСПИСАНИЯ
# ============================================================

@dp.message(
    F.text.in_({
        "📅 Расписание",
        "📅 Dars jadvali",
        "📅 Schedule"
    })
)
async def schedule(message: Message):

    await send_schedule(message)


# ============================================================
# УЧЕБНИКИ
# ============================================================

@dp.message(
    F.text.in_({
        "📚 Учебники",
        "📚 Darsliklar",
        "📚 Textbooks"
    })
)
async def books(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["books_text"].format(
            class_name=class_name
        )
    )


# ============================================================
# ДОМАШНИЕ ЗАДАНИЯ
# ============================================================

@dp.message(
    F.text.in_({
        "📝 Домашние задания",
        "📝 Uy vazifalari",
        "📝 Homework"
    })
)
async def homework(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["homework_text"].format(
            class_name=class_name
        )
    )


# ============================================================
# НОВОСТИ
# ============================================================

@dp.message(
    F.text.in_({
        "📢 Новости",
        "📢 Yangiliklar",
        "📢 News"
    })
)
async def news(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["news_text"]
    )


# ============================================================
# КОНТАКТЫ
# ============================================================

@dp.message(
    F.text.in_({
        "☎️ Контакты",
        "☎️ Aloqa",
        "☎️ Contacts"
    })
)
async def contacts(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["contacts_text"]
    )


# ============================================================
# ПОМОЩЬ
# ============================================================

@dp.message(
    F.text.in_({
        "ℹ️ Помощь",
        "ℹ️ Yordam",
        "ℹ️ Help"
    })
)
async def help_command(message: Message):

    user_id = message.from_user.id

    language = get_language(user_id)
    class_name = get_class(user_id)

    if not language:
        await message.answer(
            "🌐 Сначала выбери язык.",
            reply_markup=language_menu
        )
        return

    if not class_name:
        await message.answer(
            TEXTS[language]["no_class"],
            reply_markup=class_menu
        )
        return

    await message.answer(
        TEXTS[language]["help_text"].format(
            class_name=class_name
        )
    )


# ============================================================
# ЗАПУСК
# ============================================================

async def main():

    bot = Bot(token=BOT_TOKEN)

    print("🤖 Бот запущен!")
    print("🌐 Языки: RU / UZ / EN")
    print("🎓 Классы: 1А–11А/Б")
    print("📅 Расписание: 6Б / 7А / 8А")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
