import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.update import Update
from telegram.ext.filters import Filters

import settings

updater = Updater(token=settings.TELEGRAM_TOKEN)


def start(update: Update, context: CallbackContext):
    update.message \
        .reply_text('Assalomu alaykum! Vikipediadan maʼlumot qidiruvchi '
                    'botga hush kelibsiz! Biron nima izlash uchun /search '
                    'va so‘rovingizni yozing. Misol uchun /search Amir Temur')


def search(update: Update, context: CallbackContext):
    args = context.args

    if len(args) == 0:
        update.message\
            .reply_text('Hech bo‘lmasa, nimadir kiriting. Misol uchun '
                        '/search Amir Temur')
    else:
        search_text = ' '.join(args)
        response = requests.get('https://uz.wikipedia.org/w/api.php', {
            'action': 'opensearch',
            'search': search_text,
            'limit': 1,
            'namespace': 0,
            'format': 'json',
        })

        result = response.json()
        link = result[3]

        if len(link):
            update.message\
                .reply_text('Sizning so‘rovingiz bo‘yicha havola: ' + link[0])
        else:
            update.message\
                .reply_text('Sizning so‘rovingiz bo‘yicha hech nima yo‘q')


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()
