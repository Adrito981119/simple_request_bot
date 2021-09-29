import AccessModule
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import PicklePersistence

#teclado de acceso admin, retorna 4 xq es el numero del estado ADMIN en el bot
def admin_mode(update: Update, context):
    if AccessModule.admin_access(update,update.effective_user.id):
        query = update.callback_query
        query.answer("Acceso Autorizado. Bienvenido " + str(update.effective_user.username))
        keyboard = [
            [
                InlineKeyboardButton("Añadir catalogo",callback_data="add_catalog"),
                InlineKeyboardButton("Añadir precios",callback_data= "add_prices")
            ],
            [InlineKeyboardButton("Añadir Informacion",callback_data="add_info")]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text = "Seleccione la funcion", reply_markup=reply_markup)
    
    return 4


def set_catalog(update: Update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text("Catalogo en desarrollo")


def set_info(update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text("Catalogo en desarrollo")


def set_prices(update, context):
    query = update.callback_query
    query.answer()
    query.message.reply_text("Catalogo en desarrollo")