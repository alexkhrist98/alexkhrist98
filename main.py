#|I have revised the code of this project and found out that it smells very badly. If you're a potential employer, please
#check out my other porojects.

#this file contains main bot logic. The functions are groups in sections

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import os
import dotenv
import Girlclass
from telebot import types
from dblogic import *
import re
import schedule
import threading
import datetime
from telebot.async_telebot import types

dotenv.load()
API_KEY = os.getenv("TOKEN")
mybot = AsyncTeleBot(API_KEY, parse_mode=None)


#registration.
#below is the list that stores objects for each new user trying to register in the bot
registry_list = []

#registration step 1
@mybot.message_handler(commands=['start'])
async def start(message):
    print("Registration started for " + str(message.from_user.id))
    if registry_list == []:
        registry_list.append(Girlclass.Girl())
        registry_list[0].set_userid(message.from_user.id)
        userid = message.from_user.id
        await mybot.send_message(userid, 'Привет, давай познакомимся')
        await mybot.send_message(userid, 'Укажи, какой сегодня день в месячном цикле приёма')
    elif registry_list != []:

        for i in registry_list:
            if i.get_userid == message.from_user.id:
                print('pass')
                pass
            else:
                i.set_userid(message.from_user.id)
                registry_list.append(i)


    else:
        print("Pass")
        pass


#registration step 2
@mybot.message_handler(regexp=r'\d')
async def getnuminc(message: types.Message):
    data = getuser(message.from_user.id)
    keyboard = await create_keyboard()
    if data:
        await set_new_numinc(message)
    else:
        print("Get numinc started for " + str(message.from_user.id))
        for i in registry_list:
            if i.get_userid() == message.from_user.id:
                i.set_numinc(int(message.text))
                await mybot.send_message(i.userid, 'Спасибо)')
                await mybot.send_message(i.userid, 'А теперь скажи, пила ли ты сегодня таблетку?', reply_markup=keyboard)
            else:
                print('Pass')
                pass

#registration step 3
@mybot.message_handler(regexp=r'[данетДАНЕТ]')
async def gettakepill(message):
    print("Gettakepil started forl" + str(message.from_user.id))
    data = getuser(message.from_user.id)
    if data and message.text.lower() == 'да':
        girl = Girlclass.Girl().fromtuple(data[0])
        if girl.get_takepill() == True or girl.get_mustpill() == False:
            try:
                await mybot.send_message(girl.get_userid(), "Мур-мур, ты уже выпила таблетку)")
            except telebot.apihelper.ApiTelegramException:
                deleteuser(girl.userid)
        else:
            girl.set_takepill(True)

            try:
                await mybot.send_message(girl.get_userid(), 'Хорошо, спасибо, я запомнил')
                updateuser(girl)
            except telebot.apihelper.ApiTelegramException:
                deleteuser(girl.userid)

    for i in registry_list:
        if i.get_userid() == message.from_user.id:
            if message.text.lower() == 'да':
                i.set_takepill(True)
                await mybot.send_message(i.get_userid(), "Мур-мур, спасибо)")
                await getmustpill()
            elif message.text.lower() == 'нет':
                i.set_takepill(False)
                await mybot.send_message(i.get_userid(), 'Спасибо)')
                await getmustpill()
            else:
                await mybot.send_message(i.get_userid(), 'Введи да или нет')
        else:
            print('Pass')
            pass

#This handler handles the input from an inline keyborad, created with create_keyborad() coroutine
@mybot.callback_query_handler(func=lambda call: True)
async def set_takepill_from_keyboard(call: types.CallbackQuery):
    data = getuser(call.from_user.id)
    if data:
        girl = Girlclass.Girl().fromtuple(data[0])
        if call.data == "true":
            girl.takepill = True
            await mybot.send_message(girl.userid, "Отлично, спасибо!)")
            updateuser(girl)
        elif call.data == 'false':
            await mybot.send_message(girl.userid, "Хорошо, я напомню о ней через час.")
            await asyncio.sleep(3600)
            await check_takepill()
    else:
        for i in registry_list:
            if i.userid == call.from_user.id:
                if call.data == "true":
                    i.takepill = True
                    await mybot.send_message(i.userid, "Отлично, спасибо!)")
                    await getmustpill()
                elif call.data == 'false':
                    i.takepill = False
                    await mybot.send_message(i.userid, "Хорошо, я наопмню о ней через час, если сегодня её нужно пить")
                    await getmustpill()

async def getmustpill():
    for i in registry_list:
        if i.get_numinc() <= 21:
            i.set_mustpill(True)
        elif i.get_numinc() <= 28:
            i.set_mustpill(False)
    await registrycomplete()

#registration complete
async def registrycomplete():
    for i in registry_list:
        userid = i.get_userid()
        takepill = i.get_takepill()
        mustpill = i.get_mustpill()
        numinc = i.get_numinc()
        makenewgirl(userid, takepill, mustpill, numinc)
        await mybot.send_message(i.userid, 'Мур-мур, теперь ты зарегистрирована')
        registry_list.remove(i)
        print("Registration complete")

#other input handlers
@mybot.message_handler(commands=['help'])
async def help(message: types.Message):
    await mybot.send_message(message.from_user.id, '''Привет!\nЭтот бот поможет тебе отслеживать приём противозачаточных средств)\n
    ВНИМАНИЕ! ВСЯ ИНФОРМАЦИЯ В ЭТОМ БОТЕ НЕ ЯВЛЯЕТСЯ РЕКОМЕНДАЦИЕЙ ВРАЧА! Пожалуйста, относись ответственно к своему здоровь)\n
    Команды:\n
    /start - регистрация в боте
    /cdnuminc - изменить номер дня в цикле
    /me - узнать, что записано в боте о тебе
    /delete - удалить свои данные из бота и отписаться от уведомлений\n
    
    Контакт создателя:\n
    alex-khrist98@mail.ru''')

@mybot.message_handler(commands=['delete'])
async def delete(message):
    print(str(message.from_user.id) + 'requested a removal from database')
    deleteuser(message.from_user.id)
    await mybot.send_message(message.from_user.id, "Мы удалили твои данные и больше не будем присылать уведомления")

@mybot.message_handler(commands=['me'])
async def me(message):
    data = getuser(message.from_user.id)
    if data:
        girl = Girlclass.Girl().fromtuple(data[0])
        if girl.get_takepill() == False and girl.get_mustpill == True:
            await mybot.send_message(girl.get_userid(), f'''Ты зарегистрирована! Твой день в цикле - {girl.get_numinc()}
Сегодня ты должна выпить таблетку, но ещё её не выпила. Отправь да, когда её выпьешь''')
        elif girl.get_takepill == True:
            await mybot.send_message(girl.get_userid, f'Ты зарегистрирована! Твой день в цикле - {girl.get_numinc()} '
                                                      f'и ты уже выпила таблетку')
        elif girl.get_mustpill() == False:
            await mybot.send_message(girl.get_userid(), f'''Ты зарегистрирована! твой день в цикле - {girl.get_numinc()}
и сегодня тебе НЕ НУЖНО пить таблетку''')
        else:
            await mybot.send_message(girl.get_userid(), f'Ты зарегистрирована! Твой номер в цикле - {girl.get_numinc()}')
    else:
        await mybot.send_message(message.from_user.id, 'Ты не зарегистрирована.')

@mybot.message_handler(commands=['cdnuminc'])
async def cdnuminc(message):
    await mybot.send_message(message.from_user.id, 'Отправь новый день в цикле числом (например - 13)')

@mybot.message_handler(regexp="\d")
async def set_new_numinc(message):
    data = getuser(message.from_user.id)
    if data:
        girl = Girlclass.Girl().fromtuple(data[0])
        new_numinc = int(message.text)
        girl.set_numinc(new_numinc)
        girl.set_mustpill_from_numinc()
        updateuser(girl)
        await mybot.send_message(girl.get_userid(), f'Отлично! Теперь твой номер в цикле - {girl.get_numinc()}')

#coroutine that updates parameters for all users
async def updater():
    data = fetchallusers()
    girls = []
    if data == []:
        pass
    else:
        for i in data:
            girls.append(Girlclass.Girl().fromtuple(i))

    if girls != []:
        for i in girls:
            i.set_takepill(False)
            i.add_numinc(1)
            i.set_mustpill_from_numinc()
            updateuser(i)

#this function creates a keyboard with yes and no replies
async def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_true = types.InlineKeyboardButton(text="Да", callback_data="true", color="positive")
    button_false = types.InlineKeyboardButton(text="Нет", callback_data="false", color="negative")
    keyboard.add(button_true, button_false)
    return keyboard


#notification logic
async def sender():
    print("Sending messages")
    data = fetchallusers()
    girls = []
    keyboard = await create_keyboard()
    if data:
        for i in data:
            girl = Girlclass.Girl().fromtuple(i)
            girls.append(girl)

    if girls != []:
        for i in girls:
                print("Notifications are being sent to" + str(i.get_userid()))

                if i.get_mustpill() == True:
                    try:
                        await mybot.send_message(i.get_userid(), 'Доброе утро) Не забудь Выпить таблетку', reply_markup=keyboard)
                    except telebot.apihelper.ApiTelegramException:
                        deleteuser(i.userid)
                elif i.get_mustpill() == False:
                    try:
                        await mybot.send_message(i.get_userid(), "Доброе утро) Сегодня пить ничего не надо, так что просто желаю тебе отличного дня)")
                    except telebot.apihelper.ApiTelegramException:
                        deleteuser(i.userid)


#takepill checker
async def check_takepill():
    print("Checking takepill for users")
    keyboard = await create_keyboard()
    data = fetchallusers()
    girls = []
    for i in data:
        if not data:
            pass
        else:
            girls.append(Girlclass.Girl().fromtuple(i))

        for girl in girls:
            if girls == []:
                pass
            else:
                if girl.get_takepill() == True or girl.get_mustpill() == False:
                    pass
                else:
                    try:
                        await mybot.send_message(girl.get_userid(), 'Мне кажется, ты забыла выпить таблетку. Напиши "да", когда её выпьешь)', \
                                                 reply_markup=keyboard)
                    except telebot.apihelper.ApiTelegramException:
                        deleteuser(girl.userid)


#Scheduler that is responsible for time tracking. RUns in a separate thread.
#adds tasks to event loop in the main thread
def time_logic():
    global timer
    timer = schedule.Scheduler()
    print("Scheduler started")
    timer.every().day.at('00:00').do(lambda: loop.create_task(updater()))
    timer.every().day.at("05:30").do(lambda: loop.create_task(sender()))
    timer.every().day.at("07:00").do(lambda: loop.create_task(check_takepill()))
    while True:
        timer.run_pending()

#this function sends notifications to all users after bot was restarted
async def reboot_alert():
    data = fetchallusers()
    if data:
        for i in data:
            girl = Girlclass.Girl().fromtuple(i)
            try:
                await mybot.send_message(girl.userid, "ВНИМАНИЕ! \n"
                                                      "Бот вернулся в эфир после технического перерыва. Пожалуйста, проверьте свои данные."
                                                      "Используйте /me")
            except telebot.apihelper.ApiTelegramException:
                deleteuser(girl.userid)

#waits for user input
async def main():
    try:
        await mybot.polling(request_timeout=150, non_stop=True)
    except:
        await asyncio.sleep(1)
        loop.create_task(main())




if __name__ == "__main__":
    time_logic_thread = threading.Thread(target=time_logic)
    time_logic_thread.start()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(reboot_alert())
    loop.run_forever()
