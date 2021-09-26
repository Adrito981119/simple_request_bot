from datetime import date
import telegram
import logging

from telegram import chat
import env_vars
import AccessModule
import AdminModule
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.commandhandler import PrefixHandler

bot = telegram.Bot(token = env_vars.get_my_token())
updater = Updater(env_vars.get_my_token(), use_context=True)
despachador = updater.dispatcher
    
#estados
INICIO, PEDIDO, DESEO, VIP, ADMIN = range(5)
#log para errores y demas
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# ejecucion al dar /start
def when_start(update, context):
    if AccessModule.access(update,update.effective_user.id):
        keyboard = [
            [InlineKeyboardButton("Hacer pedido",callback_data="pedido")],
            [InlineKeyboardButton("💎Precios💎",callback_data = "precios"),
            InlineKeyboardButton("📄Informacion📄", callback_data="info")
            ],
            [InlineKeyboardButton("CATALOGO",callback_data = "catalogo")],
            [InlineKeyboardButton("👩‍⚖️Funciones administrativas👨‍⚖️",callback_data= "admin")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(text=f"🌟Bienvenido: "+ str(update.effective_user.first_name) +", soy un bot creado x @Shaddol y @CubanYisus para manejar los pedidos del canal @Anime_y_masS3 \n"
                                    "Puedes usarme directamente desde grupo o x pv si lo deseas", reply_markup = reply_markup)
    else: 
        context.bot.send_message(chat_id=update.effective_chat.id,text = "Debes ser miembro de "+ "@" + str(context.bot.get_chat(env_vars.get_channel()).username) +" para usarme")
    return INICIO



#maneja los pedidos ya sea deseos o vip
def pedir(update : Update, context):
    query =update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Deseo",callback_data="deseo"),
                InlineKeyboardButton("💎VIP💎",callback_data = "VIP")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Que tipo de pedido va a realizar",reply_markup=reply_markup)
    return PEDIDO


#define el estado de la conversacion segun si se seleccion deseo o vip
def pedido(update : Update,context):
    query = update.callback_query
    query.answer("Ha seleccionado " + str(query.data))
    try:
        if str(query.data) == "deseo":
            query.edit_message_text("Ahora escriba el nombre de la serie q desea")
            return DESEO
        else:
            if str(query.data) == "VIP":
                query.edit_message_text("Ahora escriba el nombre de la serie q desea")
                return VIP
    except:
        query.edit_message_text("Error, presione /start para comenzar de nuevo")


            
#envia la lista de los precios, modificar para uso propio
def prices(update: Update, context):
    query = update.callback_query
    query.answer("Consultar Precios. Los mejores precios de S3👌😁")
    query.edit_message_text(text = "🎥 Animes - Películas - OVAS:\n"
                                "🎞 de 12 cap - $10 MN.\n"
                                "🎞 de 24 cap - $25 MN.\n"
                                "🎞 de 25 a 35 cap - $40 MN.\n"
                                "🎞 de 36 a 55 cap - $50 MN.\n"
                                "🎞 de 56 a 65 cap - $60 MN.\n"
                                "🎞 de 66 a 75 cap - $65 MN.\n"
                                "🎞 de 100 cap       $85 MN.\n"
                                "🎞 de 100 cap en adelante es $1 x cada capitulo. Ejemplo: Una serie de 115 cap seria 85 + 15 = 100\n"
                                "🎞 Cap/Sueltos - $2 MN.\n"
                                "🎞 OVAS - $2 MN. ( en dependencia de la duración )\n\n"

                                "🎥 Películas:\n"
                                "🎞 de 1h - $5 MN.\n"
                                "🎞 de 1h 40min en adelante - $10 MN.\n\n"

                                "❗️El Precio se puede ajustar a conveniencia tanto del Admin como del usuario en caso de q la serie no este dentro de esas categorías ó haga un pedido grande variado❗️\n\n"

                                "😁👍 Gracias por elegir a @Anime_y_masS3 como su mejor opción...\n"
                                "🏠 #Quédate_en_Casa y #Échate_par_de_animes.")
    query.message.reply_text("Presione /start para comenzar de nuevo")
    return ConversationHandler.END


#envia una pequeña info sobre el funcionamiento del bot, modificar para uso propio
def info(update: Update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("✅Para pedir una serie usar #deseo seguido del nombre del anime que desea en el chat o con el pv directamente desde el bot\n\n"
                            "✅Para hacer un pedido VIP usar el #VIP seguido del nombre del anime que quiere en el chat o con el pv directamente desde el bot")
    query.message.reply_text("Presione /start para comenzar de nuevo")
    return ConversationHandler.END
    
#envia el catalogo, fichero debe llamarse catalogo.txt
def send_catalog(update: Update, context):
    query = update.callback_query
    query.answer("Aqui tiene nuestro catalogo")
    query.edit_message_text("Recuerde consultar bien el catalogo antes de hacer algun pedido")
    with open("./resources/catalogo.txt",encoding="utf-8") as file:
        context.bot.send_document(chat_id=update.effective_chat.id, document = file, filename = 'Catalogo.txt')
    query.message.reply_text("Presione /start para comenzar de nuevo")
    return ConversationHandler.END



# prepara la respuesta a dar segun si el usuario uso deseo o VIP
def build_answer(update : Update, text):    
    
    try:
        if "deseo" in text:
            resp = "😁DESEO😁 \n" + "🛎: " + update.message.text + "\n" + \
               "👤: " + str(update.effective_user.first_name) + " - " + "@" + str(update.effective_user.username) + "\n" + \
               "🔗:" + str(update.message.link) + "\n" + "ID:" + str(update.effective_user.id)

            update.message.reply_text(
            text='😁 Si contamos con la serie en nuestro stock la subiremos lo antes posible. De otra forma puede '
                 'pedirla VIP😁')
        
        if "VIP" in text:
            resp = "💎PEDIDO VIP💎 \n" + "🛎: " + update.message.text + "\n" + \
            "👤: " + str(update.effective_user.first_name) + " - " + "@" + str(
             update.effective_user.username) + "\n" + \
            "🔗:" + str(update.message.link) + "\n" + "ID:" + str(update.effective_user.id)
            update.message.reply_text(
            text='💎Gracias x usar el servicio VIP💎')         
    finally: 
        return resp 

def format_deseo(update,context):
    formated_message = "deseo " + update.message.text
    resp = build_answer(update, formated_message)
    context.bot.send_message(chat_id= env_vars.get_log_chat(), text=resp)
    update.message.reply_text("Deseo realizado con exito😁 presione /start para comenzar de nuevo")
    return ConversationHandler.END   


def format_VIP(update, context):
    formated_message = "VIP " + update.message.text
    resp = build_answer(update, formated_message)
    context.bot.send_message(chat_id= env_vars.get_log_chat(), text=resp)
    update.message.reply_text("Pedido realizado con exito😁. Le atenderemos lo mas pronto posible presione /start para comenzar de nuevo")
    return ConversationHandler.END

# envia la respuesta a un grupo o canal log creado para este fin
def send_to_log(update, context):
    resp = build_answer(update, update.message.text)
    if resp == None:
        context.bot.send_message(chat_id= update.effective_chat.id, text = "Error de peticion presione /start para empezar de nuevo")
    else:
        context.bot.send_message(chat_id= env_vars.get_log_chat(), text=resp)
        




def main() -> None:
    start_handler = CommandHandler('start', when_start)
    log_handler = PrefixHandler(['#'],['deseo','VIP','vip'],send_to_log)
    conv_handler = ConversationHandler(entry_points= [start_handler],    
    states={
        INICIO:[
            CallbackQueryHandler(pedir,pattern=r'^pedido$'),
            CallbackQueryHandler(info, pattern=r'^info$'),
            CallbackQueryHandler(prices, pattern=r'^precios$'),
            CallbackQueryHandler(send_catalog,pattern=r'^catalogo$'),
            CallbackQueryHandler(AdminModule.admin_mode,pattern=r'^admin$')
        ],
        PEDIDO: [   
            CallbackQueryHandler(pedido,pattern=r'^deseo$'),
            CallbackQueryHandler(pedido,pattern=r'^VIP$')        
        ],
        DESEO: [
            MessageHandler(filters= Filters.text & ~(Filters.command),callback=format_deseo)
        ],
        VIP: [
            MessageHandler(filters= Filters.text & ~(Filters.command),callback=format_VIP)
        ]
    },
    fallbacks=[start_handler], 
    allow_reentry=True , per_chat= True
    )

    despachador.add_handler(conv_handler)
    despachador.add_handler(log_handler)
   
    updater.start_polling()

    print("Bot is ready")
    updater.idle()


if __name__ == '__main__':
    main()
