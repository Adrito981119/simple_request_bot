import bot
import telegram
import logging
import env_vars
import AccessModule
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.commandhandler import PrefixHandler

ADMIN = range(1)

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
        return ADMIN

    else: 
         query = update.callback_query
         query.answer("🚫Acceso no autorizado🚫")
         context.bot.send_message(chat_id = update.effective_chat.id, text = "Deber ser administrador del canal para acceder a estas funciones.Una advertencia silenciosa a sido enviada a los admins.\n\n A la tercera advertencia usted sera baneado. Muchas gracias☺")
         context.bot.send_message(chat_id=env_vars.get_log_chat(),text= "🚫Acceso no autorizado🚫 \n\n" + 
        "de: " + "@" + str(update.effective_user.username) + "\n\n" + "Nombre: " + str(update.effective_user.full_name))
