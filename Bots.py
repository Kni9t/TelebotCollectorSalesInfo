import telebot
import random
from telebot import types
import pandas as pd
import requests
import json
import os

bot = telebot.TeleBot(open('key').read())
fileName = 'markets.json'
fileForAuthorization = 'AuthorizationBuf.txt'
authList = 'AuthorizationList.json'
idHost = 1209008477
#1209008477

try:
    os.remove(fileForAuthorization)
    os.remove(authList)
except:
    pass

def rewriteToFile(obj, fileName):
    try:
        fileDate = readFromFile(fileName)
        for item in fileDate:
            obj.update(fileDate[item])
        putToFile(obj, fileName)
    except:
        putToFile(obj, fileName)
def putToFile(obj, fileName):
    with open(fileName, 'w', encoding='utf8') as file:
        json.dump(obj, file, ensure_ascii=False)
        file.close()
def readFromFile(fileName):
    with open(fileName, 'r', encoding='utf8') as file:
        date = json.load(file)
        file.close()
    return date

def checkAuthorization():
    result = False
    try:
        file = open(fileForAuthorization, 'r')
        if (file.read() == 'True'):
            result = True
            file.close()
        else:
            result = False
        file.close()
    except:
        return result
    return result
def changeAuthorizationStatus():
    try:
        file = open(fileForAuthorization, 'r')
        if (file.read() == 'True'):
            file.close()
            file = open(fileForAuthorization, 'w')
            file.write('False')
        else:
            file.close()
            file = open(fileForAuthorization, 'w')
            file.write('True')
        file.close()
    except:
        file = open(fileForAuthorization, 'w')
        file.write('True')
        file.close()

marketsDate = readFromFile(fileName)
codeList = [marketCode for marketCode in marketsDate]
authorizationUserList = {}

def Authorization():
    return "msg"

print("Бот запущен!")

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Авторизоваться для учета")
    item2=types.KeyboardButton("Проверить текущую авторизацию")
    markup.add(item1, item2)
    bot.send_message(m.chat.id, 'Приветствую! Я система по учету продаж на маркетах! Я принадлежу [Hlorkens](https://vk.com/hlorkens)', reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == "Авторизоваться для учета" :
        changeAuthorizationStatus()

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)

        bot.send_message(message.chat.id, "Хорошо, сейчас проведем авторизацию.")
        bot.send_message(message.chat.id, "Если необходимо, вы можете перезапустить бота с помощью конопки start.")
        bot.send_message(message.chat.id, "Пожалуйста введите код для авторизации на маркете:", reply_markup=markup)
        #bot.send_message(message.chat.id, Authorization())
    elif ((message.text in codeList) and (checkAuthorization() == True)):
        changeAuthorizationStatus()
        authorizationUserList[int(message.chat.id)] = str(message.text)

        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Начать сбор данных о продажах")
        item2=types.KeyboardButton("/start")

        markup.add(item1, item2)

        rewriteToFile(authorizationUserList, authList)

        bot.send_message(message.chat.id, f"Ключ указан верно, ваш маркет: {marketsDate[message.text]['name']}\nПроводится: {marketsDate[message.text]['date']}")
        bot.send_message(message.chat.id, f"Теперь вы можете запустить сбор информации.", reply_markup=markup)
    elif message.text == "Проверить текущую авторизацию":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)

        if(message.chat.id in authorizationUserList.keys()):
            bot.send_message(message.chat.id, f"Вы авторизованы для следующего маркета:\n{marketsDate[authorizationUserList[message.chat.id]]['name']}\n{marketsDate[authorizationUserList[message.chat.id]]['date']}", reply_markup=markup)
        else:
            item2=types.KeyboardButton("Авторизоваться для учета")
            markup.add(item2)
            bot.send_message(message.chat.id, "Похоже вы не авторизованы. Используйте соответсвующий пункт меню или если что-то пошло не так свяжитесь с владельцами бота.", reply_markup=markup)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("/start")
        markup.add(item1)
        bot.send_message(message.chat.id, "Я не знаю такой команды! Вы можете перезапустить меня, если что-то пошло не так!", reply_markup=markup)

# Запускаем бота
bot.polling(none_stop=True, interval=0)

#https://xakep.ru/2021/11/28/python-telegram-bots/