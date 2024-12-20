import telebot
import random
from telebot import types
import pandas as pd
import requests
import time
import json
import os
from datetime import datetime

import stateController
import salesController

bot = telebot.TeleBot(open('key').read())
fileMarketList = 'MarketList.json'
fileForStatus = 'BufferFiles/statusList.json'
fileForSales = 'SalesList/salesList.json'

idHost = 1209008477
#1209008477

stateController = stateController.stateController(fileForStatus)
sales = salesController.salesController(fileForSales)

with open(fileMarketList, 'r', encoding='utf8') as file:
    marketsDate = json.load(file)
    file.close()

print("Бот запущен!")

@bot.message_handler(commands=["start"])
def start(message, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Авторизоваться для учета")
    item2=types.KeyboardButton("Проверить текущую авторизацию")
    markup.add(item1, item2)

    if (stateController.getSalesCollectState(str(message.chat.id))):
        bot.send_message(message.chat.id, 'Сбор данных о продажах остановлен!')

    stateController.setUserStats(str(message.chat.id), 'salesCollectState', False)
    stateController.setUserStats(str(message.chat.id), 'authorizationState', False)

    if (str(message.chat.id) in stateController.getDate().keys()):
        if(stateController.getDate()[str(message.chat.id)]['selectedMarket'] != None):
            item3=types.KeyboardButton("Начать сбор данных о продажах")
            markup.add(item3)
    
    if(message.chat.id == idHost):
        item4=types.KeyboardButton("Данные о текущих продажах")
        markup.add(item4)

    bot.send_message(message.chat.id, 'Приветствую! Я система по учету продаж на маркетах! Я принадлежу [Hlorkens](https://vk.com/hlorkens)', reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=["text"])
def func(message):
    if ((message.text != '') and (stateController.getSalesCollectState(str(message.chat.id)) == True) and (message.text != '/start')):
        try:
            bufNum = int(message.text.split()[0])
            authorizationUserMarket = str(stateController.getDate()[str(message.chat.id)]['selectedMarket'])
            if (bufNum >= 0):
                bufID = sales.getActualID(authorizationUserMarket)
                date = {
                    'ID': int(bufID + 1),
                    'Date': datetime.now().strftime('%d.%m.%Y'),
                    'Time': datetime.now().strftime('%H:%M:%S'),
                    'Value': bufNum,
                    'Cash': False,
                    'SenderID': str(message.chat.id),
                    'SenderName': str(message.from_user.username)
                }
                if (len(message.text.split()) > 1):
                    date['Cash'] = True
                sales.addSales(authorizationUserMarket, date)

                if (date['Cash']):
                    msgTypeSales = 'Оплата: Наличные'
                else:
                    msgTypeSales = 'Оплата: Онлайн перевод'

                bot.send_message(message.chat.id, f"Продажа зарегистрирована!\nID: {date['ID']}\nСумма: {date['Value']}\n{msgTypeSales}")
                
                totalSales = sales.getDetailsSales(authorizationUserMarket)
                cash = totalSales['Cash']
                online = totalSales['Online']
                total = totalSales['Total']

                bot.send_message(message.chat.id, f"Текущие продажи для маркета: {marketsDate[authorizationUserMarket]['name']}\nНаличные: {cash}\nПереводы: {online}\nОбщая сумма: {total}")
            else:
                bufNum *= -1
                if (sales.getSalesOwner(authorizationUserMarket, int(bufNum)) == str(message.chat.id)):
                    removedSales = sales.removeSalesByID(authorizationUserMarket, int(bufNum))
                    if (removedSales != None):
                        bot.send_message(message.chat.id, f"Продажа, зарегистрированная в {removedSales['Date']} {removedSales['Time']}\nc ID: {removedSales['ID']}, на сумму {removedSales['Value']} успешно удалена!")
                    else:
                        bot.send_message(message.chat.id, f"Продажи с таким ID нету для данного маркета!")
                else:
                    bot.send_message(message.chat.id, f"У вас нету доступа для удаления данной продажи, так как не вы добавили ее!")
        except Exception as e:
            print(f'Error: {e}')
            bot.send_message(message.chat.id, "Значение перед пробелом должно быть числом!")
    elif message.text == "Авторизоваться для учета" :
        stateController.setUserStats(str(message.chat.id), 'salesCollectState', False)
        stateController.setUserStats(str(message.chat.id), 'authorizationState', True)

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)

        bot.send_message(message.chat.id, "Хорошо, сейчас проведем авторизацию.")
        bot.send_message(message.chat.id, "Если необходимо, вы можете перезапустить бота с помощью кнопки start.")
        bot.send_message(message.chat.id, "Пожалуйста введите код для авторизации на маркете:", reply_markup=markup)
        #bot.send_message(message.chat.id, Authorization())
    elif ((message.text in marketsDate.keys()) and (stateController.getAuthorizationUserState(str(message.chat.id)) == True)):
        
        stateController.setUserStats(str(message.chat.id), 'authorizationState', False)
        stateController.setUserStats(str(message.chat.id), 'selectedMarket', str(message.text))

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Начать сбор данных о продажах")
        item2=types.KeyboardButton("/start")

        markup.add(item1, item2)

        bot.send_message(message.chat.id, f"Ключ указан верно, ваш маркет: {marketsDate[message.text]['name']}\nПроводится: {marketsDate[message.text]['date']}")
        bot.send_message(message.chat.id, f"Теперь вы можете запустить сбор информации. Для этого нажмите соответствующую кнопку ниже, либо же напишите боту сообщение: 'Начать сбор данных о продажах'", reply_markup=markup)
    elif message.text == "Проверить текущую авторизацию":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)

        if(stateController.getAuthorizatMarket(str(message.chat.id)) != None):
            bot.send_message(message.chat.id, f"Вы авторизованы для следующего маркета:\n{marketsDate[stateController.getDate()[str(message.chat.id)]['selectedMarket']]['name']}\n{marketsDate[stateController.getDate()[str(message.chat.id)]['selectedMarket']]['date']}", reply_markup=markup)
        else:
            item2=types.KeyboardButton("Авторизоваться для учета")
            markup.add(item2)
            bot.send_message(message.chat.id, "Похоже вы не авторизованы. Используйте соответствующий пункт меню или если что-то пошло не так свяжитесь с владельцами бота.", reply_markup=markup)
    elif message.text == "Начать сбор данных о продажах":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)

        if(stateController.getDate()[str(message.chat.id)]['selectedMarket'] != None):
            stateController.setUserStats(str(message.chat.id), 'salesCollectState', True)
            bot.send_message(message.chat.id, f"Вы успешно запустили сбор данных о продажах на: {marketsDate[stateController.getDate()[str(message.chat.id)]['selectedMarket']]['name']}\nТеперь вы можете писать сумму в чат и она будет автоматически добавятся к списку продаж на маркете!\nЕсли вам нужно прекратить сбор данных, просто напишите команду: /start, или нажмите на кнопку ниже.")
            bot.send_message(message.chat.id, 'Все зарегистрированные платежи считаются полученными по переводу. Если необходимо указать, что оплата была произведена наличными добавьте после суммы пробел и любую текстовую строчку.\nНапример так: "600 нал"\nИли так: "500 н"')
            bot.send_message(message.chat.id, f"Каждой продаже присваивается уникальный ID. Если вы хотите удалить какую-либо продажу, напишите боту ID продажи добавив знак - в начале.", reply_markup=markup)
        else:
            item2=types.KeyboardButton("Авторизоваться для учета")
            markup.add(item2)
            bot.send_message(message.chat.id, "Похоже вы не авторизованы. Используйте соответствующий пункт меню или если что-то пошло не так свяжитесь с владельцами бота.", reply_markup=markup)
    elif ((message.text == 'Данные о текущих продажах') and (message.chat.id == idHost)):
        for market in marketsDate.keys():
            bufSum = sales.getSumSales(market)
            if (bufSum != 0):
                bot.send_message(message.chat.id, f"Для маркета {marketsDate[str(market)]["name"]} на текущий момент сумма продаж составляет: {bufSum} руб.")
            else:
                bot.send_message(message.chat.id, f"Для маркета {marketsDate[str(market)]["name"]} продаж пока отсутствуют!")
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)
        bot.send_message(message.chat.id, "Я не знаю такой команды! Вы можете перезапустить меня, если что-то пошло не так!", reply_markup=markup)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        file = open('Error_log.txt', 'a')
        file.write(f'{datetime.now()} - {e}\n')
        time.sleep(5)
        continue
