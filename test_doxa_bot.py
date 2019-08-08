import math
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
import time
import requests
import re
from random import randint
from functools import reduce
import random
import telebot
from telebot import types, logger


TOKEN = '937987436:AAGHrcIRswlBzW0LyJJ6Jh_zqNzKkkn0oXQ'

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)

bot = telebot.TeleBot(TOKEN);


@bot.message_handler(commands=['start'])
def first_start(message):
    bot.send_message(message.chat.id, "Привет! Это бот от @doxajournal для помощи задержанным студентам и сотрудникам университетов. Вы также можете обращаться от лица задержанных, если у них самих нет возможности сделать это. Мы поможем оплатить административный штраф или передачи в спецприемник, придать огласке конкретно вашу ситуацию (рассказать о давлении, например), а также дать необходимую информацию. \n\
ВНИМАНИЕ: Этот бот — не замена бота ОВД-ИНФО или любой другой правозащитной организации. Мы не предоставляем адвокатов. Если вас задержали, первым делом обязательно обратитесь в @OvdInfoBot и лишь после этого — к нам. \n\
Для начала работы с ботом используйте команду /help");

@bot.message_handler(commands=['help'])
def lets_get_started(message, chat_id=None):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_1 = types.InlineKeyboardButton(text='Меня задержали, сижу в автозаке/ОВД', callback_data='1'); #кнопка «Да»
    keyboard.add(key_1); #добавляем кнопку в клавиатуру
    key_2= types.InlineKeyboardButton(text='Уже отпустили, но суда еще не было', callback_data='2');
    keyboard.add(key_2);
    key_3 = types.InlineKeyboardButton(text='Суд был, назначили арест/штраф', callback_data='3'); #кнопка «Да»
    keyboard.add(key_3); #добавляем кнопку в клавиатуру
    key_4 = types.InlineKeyboardButton(text='Оплата передач', callback_data='4');
    keyboard.add(key_4);
    key_5 = types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
    keyboard.add(key_5);
    
    question = 'Чем мы можем помочь? \n \
Если повязали/пришли с обыском/везут на допрос/грозятся отчислить и т.п., мы незамедлительно напишем об этом во все доступные нам информационные каналы, чтобы придать этот случай максимальной огласке: ведь сейчас она — ваша главная защита. \n\
Также мы помогаем всем, кому нужно оплатить штраф. \n\
Ещё к нам можно (и нужно!) обращаться за помощью в оплате передачек в спецприёмники для задержанных. \n\
Внизу есть несколько кнопок — выбери ту, что по душе :) \n\
Если нужного варианта нет, или ситуация не терпит отлагательств, пиши нам прямо здесь. Кстати, сделать это можно будет на любом этапе общения с ботом.'
    if not chat_id:
        chat_id = message.chat.id
    bot.send_message(chat_id, text=question, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.chat.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

def send_message_to_nasvobode(message):
    text = message.text + '\n' + 'username @{}'.format(str(message.from_user.username))
    # str(message.from_user.username)
    print(message.chat.id)
    bot.send_message(-382306040, text);
    bot.send_message(message.chat.id, "Спасибо! Мы получили информацию и скоро тебе ответим. \
        Если еще не написал/а боту ОВД-инфо (@OvdInfoBot), пожалуйста, сделай это. Держись, мы с тобой!")

def send_message_to_nenasvobode(message):
    text = message.text + '\n' + 'username @{}'.format(str(message.from_user.username))
    # str(message.from_user.username)
    print(message.chat.id)
    bot.send_message(-337074015, text);
    bot.send_message(message.chat.id, "Спасибо! Мы получили информацию и скоро тебе ответим. \
        Если еще не написал/а боту ОВД-инфо (@OvdInfoBot), пожалуйста, сделай это. Держись, мы с тобой!")

def send_message_to_shtrafi(message):
    text = message.text + '\n' + 'username @{}'.format(str(message.from_user.username))
    # str(message.from_user.username)
    print(message.chat.id)
    bot.send_message(-252458159, text);
    bot.send_message(message.chat.id, "Спасибо! Мы получили информацию и скоро тебе напишем.")

def send_message_to_everything(message):
    text = message.text + '\n' + 'username @{}'.format(str(message.from_user.username))
    # str(message.from_user.username)
    print(message.chat.id)
    bot.send_message(-330837612, text);
    bot.send_message(message.chat.id, "Спасибо! Мы получили информацию и скоро тебе ответим. \
        Если еще не написал/а боту ОВД-инфо (@OvdInfoBot), пожалуйста, сделай это. Держись, мы с тобой!")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    text1 = 'Если еще не написал_а в @OvdInfoBot - пиши сейчас. \n\
Если уже написал/а -- опиши максимально подробно и в ОДНОМ сообщении, что произошло с тобой/твоим знакомым: \n\
1) ФИО, возраст и контактный телефон. \n\
2) ВУЗ, статус в нем. \n\
3) Что с тобой происходит: применялось ли насилие. Есть фото/видео задержания? Пришли и их. \n\
4) Если есть еще что-то, что мы должны знать, — рассказывай! \n\
Также у нас есть чат для задержанных студентов/сотрудников ВУЗов. В нем своя — довольно уютная — атмосфера. Присоединяйся: @DOXA_OVD'
    text2 = 'Напиши нам (в ОДНОМ сообщении): \n\
1) Свои ФИО, возраст и контактный телефон. \n\
2) Свой университет и твой статус в нем. \n\
3) Опиши все детали. \n\
4) Если есть еще что-то, что мы должны знать, — рассказывай! \n\
Также у нас есть чат для задержанных студентов. В нем своя — довольно уютная — атмосфера. Присоединяйся: @DOXA_OVD \n\
Сообщай нам обо всех подробностях твоего дела и обязательно напиши, когда изберут меру пресечения — неважно, арест это (будем надеяться, что нет) или штраф.'
    text3 = "К сожалению, финансово мы помогаем только студентам и сотрудникам университетов. \n\
Но если тебя задержали, в первую очередь обратись в ОВД-ИНФО (@OvdInfoBot / 88007070528) или Правозащиту Открытки (@ORpravobot), или же напиши лично главе юрслужбы «Апология протеста» Алексею Глухову (@GlukhovLawyer), если никто не отвечает. \n\
Также ты можешь прочитать наш FAQ (http://doxajournal.ru/uni/detentions_faq?fbclid=IwAR25rdl_LA0k- Cl8tgujFtdpk6GEZsNkzvAg_SaG7E88RwJRvJ3bSn4qrCE), где собрана вся необходимая информация. \n\
Если же нужно оплатить штраф, не переживай — оплатой штрафов всех задержанных по политическим делам давно и успешно занимается ФБК (https://fbk.info/blog/post/513/)"
    text4 = "В этом случае лучшим вариантом будет обратиться к ребятам из ФБК. Они предоставляют подробную инструкцию по суду, апелляциям, ходатайствам и т.д., а также помогают дойти до ЕСПЧ, компенсирующего все твои штрафы и моральный ущерб. Но главное — Фонд Борьбы с Коррупцией тоже оплачивает штрафы. Здесь можно найти всю необходимую информацию: https://fbk.info/blog/post/513/ В случае, если передумаешь подавать апелляцию, возиться с судами и идти до ЕСПЧ – не стесняйся снова обращаться к нам, мы оплатим штраф!"
    text5 = "В этом случае ты не сможешь подать жалобу в ЕСПЧ. Штраф оплатим мы. Тебе нужно будет отправить нам: \n\
    1) фото студенческого \n\
    2) фото постановления об оплате штрафа \n\
    3) номер карты \n\
    Для этого напиши сюда 'Хочу возместить штраф' и мы с тобой свяжемся"
    text6 = "Если ты подаешь апелляцию, то вся необходимая помощь (адвокат, помощь в суде, помощь с подачей ходатайств и проч.) будет предоставлена правозащитными организациями — например, ОВД- ИНФО, Апологией Протеста или ФБК. Помимо этого, тебе помогут подать жалобу в ЕСПЧ, который компенсирует все твои затраты и моральный ущерб. И ещё: в случае подачи апелляции твой штраф оплачивает ФБК. Можешь вернуться назад и выбрать нужный вариант ответа."
    if call.data == "0":
        lets_get_started(call.message, call.message.chat.id)
    elif call.data == "1":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0'); 
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='?');
        keyboard.add(key_2);
        key_3= types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
        keyboard.add(key_3);
        bot.send_message(call.message.chat.id, text=text1, reply_markup=keyboard);
        bot.register_next_step_handler(call.message, send_message_to_nenasvobode);
    elif call.data == "2":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0'); 
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='?');
        keyboard.add(key_2);
        key_3= types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
        keyboard.add(key_3);
        bot.send_message(call.message.chat.id, text2, reply_markup=keyboard);
        bot.register_next_step_handler(call.message, send_message_to_nasvobode);
    elif call.data == "3":
        keyboard = types.InlineKeyboardMarkup();
        key_3 = types.InlineKeyboardButton(text='Да', callback_data='31'); 
        keyboard.add(key_3);
        key_4 = types.InlineKeyboardButton(text='Нет', callback_data='32'); 
        keyboard.add(key_4);
        key_5 = types.InlineKeyboardButton(text='Зачем мне это?', callback_data='33'); 
        keyboard.add(key_5);
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0'); 
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='?');
        keyboard.add(key_2);
        key_6= types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
        keyboard.add(key_6);
        bot.send_message(call.message.chat.id, 'Планируешь подавать апелляцию?', reply_markup=keyboard);
        # bot.register_next_step_handler(call.message, send_message);
    elif call.data == "4":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0'); 
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='?');
        keyboard.add(key_2);
        key_3= types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
        keyboard.add(key_3);
        bot.send_message(call.message.chat.id, 'Купите все необходимое человеку, которого отправили в спецприемник, а затем отправьте нам фотографию чека и номер вашей банковской карты. Мы возместим сумму целиком. Также мы попросим приложить подтверждение того, что человек имеет отношение к академической среде: фото студенческого, ссылку на личную страницу на сайте ВУЗа, (если задержанный — преподаватель) или любой другой документ подобного типа. Всю информацию по арестам, необходимым в спецприемнике вещам, правилам передач и т.д. можно найти здесь — @Peredachi. Для этого напишите сообщение с текстом "Хочу возместить по чеку" и с вами свяжутся', reply_markup=keyboard);
        bot.register_next_step_handler(call.message, send_message_to_shtrafi);  
    elif call.data == "-":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0'); 
        keyboard.add(key_1);
        # key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='?');
        # keyboard.add(key_2);
        # key_3 = types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
        # keyboard.add(key_3);
        bot.send_message(call.message.chat.id, text3, reply_markup=keyboard);
        # bot.register_next_step_handler(call.message, send_message_to_adm);
    elif call.data == "31":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0');
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='3');
        keyboard.add(key_2);
        key_3= types.InlineKeyboardButton(text='Я не имею отношения к вузу', callback_data='-');
        keyboard.add(key_3);
        bot.send_message(call.message.chat.id, text4, reply_markup=keyboard);
        # bot.register_next_step_handler(call.message, send_message);
    elif call.data == "32":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0');
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='3');
        keyboard.add(key_2);
        bot.send_message(call.message.chat.id, text5, reply_markup=keyboard);
        bot.register_next_step_handler(call.message, send_message_to_shtrafi);
    elif call.data == "33":
        keyboard = types.InlineKeyboardMarkup(); 
        key_1 = types.InlineKeyboardButton(text='В начало', callback_data='0'); 
        keyboard.add(key_1);
        key_2= types.InlineKeyboardButton(text='На шаг назад', callback_data='3');
        keyboard.add(key_2);
        bot.send_message(call.message.chat.id, text6, reply_markup=keyboard);
        # bot.register_next_step_handler(call.message, send_message);
    elif call.data == "?":
        lets_get_started(call.message, call.message.chat.id)



if __name__ == '__main__':
    # bot.polling(none_stop=True, interval=0.1)
    while True:
        try:
            bot.polling(none_stop=True, interval=1)

        # ConnectionError and ReadTimeout because of possible timout of the requests library

        # TypeError for moviepy errors

        # maybe there are others, therefore Exception

        except Exception as e:

            # logger.error(e)

            time.sleep(10)












