#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Options
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='YOURE TOKEN') # Telegram API Token
dispatcher = updater.dispatcher
# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello, do you want to talk?')
def textMessage(bot, update):
    request = apiai.ApiAI('YOURE DIALOGFLOW TOKEN').text_request() # Dialogflow API Token
    request.lang = 'en' # Request language
    request.session_id = 'YoureBot' # ID dialog session (for bot training)
    request.query = update.message.text # Send request to AI ИИ with the user message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Take JSON answer
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='I dont understand!')
# Handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Add handlers to the dispatcher
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Start update search
updater.start_polling(clean=True)
# Stops the bot
updater.idle()
