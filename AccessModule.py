
import telegram
from telegram import chat
from telegram.utils.helpers import effective_message_type
import env_vars
from telegram import Update

bot = telegram.Bot(token = env_vars.get_my_token())

#se usa para saber si el usuario pertenece al canal donde esta el bot
def access(update: Update,id):
    person = bot.get_chat_member(env_vars.get_channel(),id).status
    if person == 'member' or person == 'creator' or person == 'administrator' :
        return True
    else:
        return False

def admin_access(update: Update, id):
    admin = bot.get_chat_member(env_vars.get_channel(),id).status
    if admin == 'creator' or admin == 'administrator' : return True
    else: 
        return False