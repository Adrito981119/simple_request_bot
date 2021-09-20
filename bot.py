import telegram
import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler

#env vars y login en telegram
mToken = os.environ['TOKEN']
target = os.environ['ID_CHAT']
bot = telegram.Bot(mToken)


#log para errores y demas
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




# ejecucion al dar /start
def when_start(update, context):
    keyboard = [
   
        [InlineKeyboardButton("💎Precios💎",callback_data = "precios"),
        InlineKeyboardButton("📄Informacion📄", callback_data="info")
        ],
        [InlineKeyboardButton("CATALOGO",callback_data = "catalogo")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text=f"🌟Bienvenido: "+ str(update.effective_user.first_name) +", soy un bot creado x @Shaddol y @CubanYisus para manejar los pedidos del canal @Anime_y_masS3 \n"
                                    "Puedes usarme directamente desde grupo o x pv si lo deseas", reply_markup = reply_markup)

#envia la lista de los precios, modificar para uso propio
def prices(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("🎥 Animes - Películas - OVAS:\n"
                                "🎞 de 12 cap - $10 MN.\n"
                                "🎞 de 24 cap - $25 MN.\n"
                                "🎞 de 25 a 35 cap - $35 MN.\n"
                                "🎞 de 36 a 50 cap - $40 MN.\n"
                                "🎞  de 51 a 75 cap - $55 MN.\n"
                                "🎞 de 100 cap  o mas - $75 MN.\n"
                                "🎞 Cap/Sueltos - $2 MN.\n"
                                "🎞 OVAS - $2 MN. ( en dependencia de la duración )\n\n"

                                "🎥 Películas:\n"
                                "🎞 de 1h - $5 MN.\n"
                                "🎞 de 1h 40min en adelante - $10 MN.\n\n"

                                "❗️El Precio se puede ajustar a conveniencia tanto del Admin como del usuario en caso de q la serie no este dentro de esas categorías ó haga un pedido grande variado❗️\n\n"

                                "😁👍 Gracias por elegir a @Anime_y_masS3 como su mejor opción...\n"
                                "🏠 #Quédate_en_Casa y #Échate par de animes.")

#envia una pequeña info sobre el funcionamiento del bot, modificar para uso propio
def info(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("✅Para pedir una serie usar #deseo seguido del nombre del anime que desea en el chat o con el pv directamente desde el bot\n\n"
                            "✅Para hacer un pedido VIP usar el #VIP seguido del nombre del anime que quiere en el chat o con el pv directamente desde el bot")
    

def send_catalog(update: Update, context):
    query = update.callback_query
    query.answer()
    with open("./resources/catalogo.txt", encoding = "utf-8") as file:
        context.bot.send_document(chat_id=update.effective_chat.id,document = file, filename = 'Catalogo.txt')




# prepara la respuesta a dar segun si el usuario uso deseo o VIP
def build_answer(update, text):
    text = update.message.text
    if '#deseo' in text:
        resp = "😁DESEO😁 \n" + "🛎: " + update.message.text + "\n" + \
               "👤: " + str(update.effective_user.first_name) + " - " + "@" + str(update.effective_user.username) + "\n" + \
               "🔗:" + str(update.message.link) + "\n" + "ID:" + str(update.effective_user.id)

        update.message.reply_text(
            text='😁 Si contamos con la serie en nuestro stock la subiremos lo antes posible. De otra forma puede '
                 'pedirla VIP😁')
    if '#VIP' in text:
        resp = "💎PEDIDO VIP💎 \n" + "🛎: " + update.message.text + "\n" + \
               "👤: " + str(update.effective_user.first_name) + " - " + "@" + str(
                update.effective_user.username) + "\n" + \
               "🔗:" + str(update.message.link) + "\n" + "ID:" + str(update.effective_user.id)
        update.message.reply_text(
            text='💎Gracias x usar el servicio VIP💎')
    return resp



# envia la respuesta a un grupo o canal log creado para este fin
def send_to_log(update, context):
    resp = build_answer(update, update.message.text)
    context.bot.send_message(chat_id=target, text=resp)




def main() -> None:

    updater = Updater(mToken, use_context=True)
    despachador = updater.dispatcher
    


    start_handler = CommandHandler('start', when_start)
    log_handler = MessageHandler(Filters.regex('#deseo') ^ Filters.regex('#VIP'), send_to_log)
    info_handler = CallbackQueryHandler(info, pattern=r'^info$')
    price_handler = CallbackQueryHandler(prices, pattern=r'^precios$')
    catalog_handler = CallbackQueryHandler(send_catalog,pattern=r'^catalogo$')


    despachador.add_handler(start_handler)
    despachador.add_handler(info_handler)
    despachador.add_handler(price_handler)
    despachador.add_handler(catalog_handler)
    despachador.add_handler(log_handler)

    updater.start_polling()

    print("Bot is ready")
    updater.idle()


if __name__ == '__main__':
    main()
