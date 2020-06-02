import logging
import requests
import COVID19Py
import matplotlib.pyplot as plt
import re
import json
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, InlineQueryHandler)

__author__ = 'Desai'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def KAR_Dist(bot, update):
    
    chat_id= update.message.chat_id
    data = requests.get('https://api.covidindiatracker.com/state_data.json').json()
    for each in data[11]['districtData']:
        bot.send_message(chat_id=chat_id, text=each['name']+'\n '+"confirmed : "+str(each['confirmed'])+'\n '+ "Recovered : " +str(each['recovered'])+'\n '+"Deaths : "+str(each['deaths'])+'\n\n'+"Zone :" +each['zone'])


covid19=COVID19Py.COVID19()
data = covid19.getAll(timelines=True)
virusdata=dict(data["latest"])
names=list(virusdata.keys())
values=list(virusdata.values())

def start(bot, update):
    update.message.reply_text('Hey! Welcome to The_COVID19BOT.\n\nThis Bot is to keep people updated about count of people affected by Corona.\nPlease click on /All to get World covid19 affected Data , /IN to get INDIA covid19 affected Data and /KAR_Dist gives all district affected data from KARNATAKA'
                              )

def world_plot():
    plt.bar(range(len(virusdata)), values,tick_label=names)
    plt.savefig('All.png')
    return plt


def All(bot, update):
    world_plot()
    chat_id= update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('All.png', 'rb'))
    bot.send_message(chat_id=chat_id, text=virusdata)

def IN(bot, update):
    chat_id= update.message.chat_id
    location=covid19.getLocationByCountryCode("IN")
    loc_data=location[0]
    virusdata=dict(loc_data['latest'])
    names=list(virusdata.keys())
    values=list(virusdata.values())
    plt.bar(range(len(virusdata)), values,tick_label=names)
    plt.savefig('IN.png')
    bot.send_photo(chat_id=chat_id, photo=open('IN.png', 'rb'))
    bot.send_message(chat_id=chat_id, text=virusdata)

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, bot.error)

def main():
    updater = Updater('844537889:AAHyfuJiV9vz556SS4ZjC-GBpRKHnYi8W0Q')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('All',All))
    dp.add_handler(CommandHandler('IN',IN))
    dp.add_handler(CommandHandler('KAR_Dist',KAR_Dist))
    
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('error',error))
    logger.info('Stay Home ! Stay Safe ! %s..' % updater.bot.username)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    