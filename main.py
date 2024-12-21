from telegram import (Update,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ReplyKeyboardMarkup,
                      KeyboardButton)
from telegram.ext import (Application,
                          ConversationHandler,
                          MessageHandler,
                          CommandHandler,
                          ContextTypes,
                          InlineQueryHandler,
                          CallbackQueryHandler,
                          filters)

import logging

from tasks_allocation_package.classes_utils import *
from tasks_allocation_package.utils import *

from hid_vars import bot_token

# logging.basicConfig(
#     format="time: %(act_time)s, name: %(name)s, level: %(levelname)s, message: %(message)s",
#     level=logging.INFO
# )
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

LEVELS = zip(("MAIN_MENU", "SCHEDULE", "DAY"), map(chr, range(0, 3)))
# STATES_HIERARCHY = {
#     "MAIN_MENU": {
#         {"SCHEDULE": {
#
#         }},
#         {"SETTINGS": {
#
#         }},
#         {"ABOUT": {
#
#         }}},
# }
# states names
(
    SELECTING_IN_MAIN_MENU,
    TO_SCHEDULE_MENU, SELECTING_IN_SCHEDULE_MENU,
    TO_SCHEDULE,
    TO_TASKS,
    TO_ADD_TASK,
    WRITING_TASK_NAME, WRITING_TASK_DEADLINE, WRITING_TASK_INTEREST, WRITING_TASK_WORK_HOURS, WRITING_TASK_MUST_DO,
    GENERATE_SCHEDULE,
    TO_SETTINGS, SELECTING_IN_SETTINGS,
    TO_ABOUT, SELECTING_IN_ABOUT,
    STOP_ALL
) = map(chr, range(17))
END = ConversationHandler.END


def get_main_menu_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Расписание", callback_data=TO_SCHEDULE_MENU),
            InlineKeyboardButton(text="Настройки", callback_data=TO_SETTINGS)
        ],
        [
            InlineKeyboardButton(text="О проекте", callback_data=TO_ABOUT)
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


def get_back_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Назад", callback_data=END),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    start_text = "Привет, я бот-распределитель задач!"
    await update.message.reply_text(text=start_text)

    text = "Выберите пункт меню:"
    await update.message.reply_text(text=text, reply_markup=get_main_menu_keyboard())

    return SELECTING_IN_MAIN_MENU


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "До встречи!"
    await update.message.reply_text(text=text)

    return STOP_ALL


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Выберите пункт меню:"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=get_main_menu_keyboard())
    return SELECTING_IN_MAIN_MENU


async def show_schedule_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Затычка, расписание ещё не сделано"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=get_back_keyboard())
    return SELECTING_IN_SCHEDULE_MENU


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Затычка, настройки ещё не сделаны"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=get_back_keyboard())
    return SELECTING_IN_SETTINGS


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "chpdd$$$$$$$$$$$$$$$"
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=get_back_keyboard())
    return SELECTING_IN_ABOUT


async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Вот ваше расписание:"
    schedule_keyboard = [
        [InlineKeyboardButton(text="Назад", callback_data=)],
    ]
    schedule_markup = ReplyKeyboardMarkup(keyboard=schedule_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.callback_query.answer()
    await update.message.reply_text(text=text, reply_markup=schedule_markup)
    for work_day in context.user_data["work_days"]:
        await.update.message.reply_text()
    #     TODO: вывод каждого рабочего дня


async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    pass


async def ask_task_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    return WRITING_TASK_NAME


async def ask_task_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    return WRITING_TASK_DEADLINE


async def ask_task_interest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    return WRITING_TASK_INTEREST


async def ask_task_work_hours(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    return WRITING_TASK_WORK_HOURS


async def ask_task_must_do(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    return WRITING_TASK_MUST_DO

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    pass


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)

    return END


def main() -> None:
    application = Application.builder().token(bot_token).build()

    add_task_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern=f"^{TO_ADD_TASK}$", callback=ask_task_name)
        ],
        states={
            WRITING_TASK_NAME: MessageHandler(filters=filters.TEXT, callback=ask_task_deadline),
            WRITING_TASK_DEADLINE: MessageHandler(filters=filters.TEXT, callback=ask_task_interest),
            WRITING_TASK_INTEREST: MessageHandler(filters=filters.TEXT, callback=ask_task_work_hours),
            WRITING_TASK_WORK_HOURS: MessageHandler(filters=filters.TEXT, callback=ask_task_must_do),
            WRITING_TASK_MUST_DO: MessageHandler(filters=filters.TEXT, callback=add_task)
        }
    )

    tasks_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern=f"^{TO_TASKS}$", callback=show_tasks)
        ],
        states={

        }
    )

    schedule_menu_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern=f"^{TO_SCHEDULE_MENU}$", callback=show_schedule_menu),
        ],
        states={
            SELECTING_IN_SCHEDULE_MENU: [
                CallbackQueryHandler(pattern=f"{TO_SCHEDULE}", callback=),
                CallbackQueryHandler(pattern=f"{TO_TASKS}"),
                CallbackQueryHandler()
            ]
        },
        fallbacks=[
            CommandHandler(command="stop", callback=stop),
            CallbackQueryHandler(pattern=f"^{END}$", callback=back_to_main_menu),
        ],
        map_to_parent={
            STOP_ALL: STOP_ALL,
            END: SELECTING_IN_MAIN_MENU
        }
    )

    settings_menu_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern=f"^{TO_SETTINGS}$", callback=show_settings)
        ],
        states={
            SELECTING_IN_SETTINGS: [

            ]
        },
        fallbacks=[
            CommandHandler(command="stop", callback=stop),
            CallbackQueryHandler(pattern=f"^{END}$", callback=back_to_main_menu)
        ],
        map_to_parent={
            STOP_ALL: STOP_ALL,
            END: SELECTING_IN_MAIN_MENU
        }
    )

    about_menu_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern=f"^{TO_ABOUT}$", callback=show_about)
        ],
        states={
            SELECTING_IN_ABOUT: [

            ]
        },
        fallbacks=[
            CommandHandler(command="stop", callback=stop),
            CallbackQueryHandler(pattern=f"^{END}$", callback=back_to_main_menu)
        ],
        map_to_parent={
            STOP_ALL: STOP_ALL,
            END: SELECTING_IN_MAIN_MENU
        }
    )

    main_menu_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
        states={
            SELECTING_IN_MAIN_MENU: [
                schedule_menu_conv_handler,
                settings_menu_conv_handler,
                about_menu_conv_handler
            ],
        },
        fallbacks=[
            CallbackQueryHandler(pattern=f"^{END}$", callback=stop),
            CommandHandler("stop", stop)
        ],
    )

    application.add_handler(main_menu_conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
