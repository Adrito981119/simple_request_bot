import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import datetime


#declaraciones y login en telegram
mToken = '1963669907:AAHPjXfT5139wX1ZwzD9w5CQsiRsw-0vD5Q'
target = '-1001541425188'
today = datetime.date.today()
bot = telegram.Bot(mToken)
updater = Updater(mToken, use_context=True)
despachador = updater.dispatcher
#log para errores y demas
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# ejecucion al dar /start, totalmente inutil
def when_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola soy un bot creado x @Shaddol y @CubanYisus para manejar los pedidos del canal @Anime_y_masS3 \n"
                                  "Puedes usarme directamente desde grupo o x pv si lo deseas")


start_handler = CommandHandler('start', when_start)
despachador.add_handler(start_handler)
updater.start_polling()


# prepara la respuesta a dar segun si el usuario uso deseo o VIP
def build_answer(update, text):
    text = update.message.text
    if '#deseo' in text:
        resp = "😁DESEO😁 \n" + "🛎: " + update.message.text + "\n" + \
               "👤: " + str(update.effective_user.first_name) + " - " + "@" + str(update.effective_user.username) + "\n" + \
               "⌚:" + str(today) + "\n" + \
               "🔗:" + str(update.message.link) + "\n" + "ID:" + str(update.effective_user.id)

        update.message.reply_text(
            text='😁 Si contamos con la serie en nuestro stock la subiremos lo antes posible. De otra forma puede '
                 'pedirla VIP😁')
    if '#VIP' in text:
        resp = "💎PEDIDO VIP💎 \n" + "🛎: " + update.message.text + "\n" + \
               "👤: " + str(update.effective_user.first_name) + " - " + "@" + str(
            update.effective_user.username) + "\n" + \
               "⌚:" + str(today) + "\n" + \
               "🔗:" + str(update.message.link) + "\n" + "ID:" + str(update.effective_user.id)
        update.message.reply_text(
            text='💎Gracias x usar el servicio VIP💎')
    return resp


# envia la respuesta a un grupo o canal log creado para este fin
def send_to_log(update, context):
    resp = build_answer(update, update.message.text)
    context.bot.send_message(chat_id=target, text=resp)


log_handler = MessageHandler(Filters.regex('#deseo') ^ Filters.regex('#VIP'), send_to_log)
despachador.add_handler(log_handler)

print("Bot is ready")
