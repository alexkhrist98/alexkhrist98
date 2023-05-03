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
    print("Get numinc started for " + str(message.from_user.id))
    for i in registry_list:
        if i.get_userid() == message.from_user.id:
            i.set_numinc(int(message.text))
            await mybot.send_message(i.userid, 'Спасибо)')
            await mybot.send_message(i.userid, 'А теперь скажи, пила ли ты сегодня таблетку?')
        else:
            print('Pass')
            pass

#registration step 3
@mybot.message_handler(regexp=r'[данетДАНЕТ]')
async def gettakepill(message):
    print("Gettakepil started forl" + str(message.from_user.id))
    data = getuser(message.from_user.id)
    if data != [] and message.text.lower() == 'да':
        girl = Girlclass.Girl('', False, False, 0).fromtuple(data[0])
        if girl.get_takepill() == True or girl.get_mustpill() == False:
            await mybot.send_message(girl.get_userid(), "Мур-мур, ты уже выпила таблетку)")
        else:
            girl.set_takepill(True)

            await mybot.send_message(girl.get_userid(), 'Хорошо, спасибо, я запомнил')
            updateuser(girl)

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
    /delete - удалить свои данные из бота и отписаться от уведомлений\n
    
    Контакт создателя:\n
    alex-khrist98@mail.ru''')

@mybot.message_handler(commands=['delete'])
async def delete(message):
    print(str(message.from_user.id) + 'requested a removal from database')
    deleteuser(message.from_user.id)
    await mybot.send_message(message.from_user.id, "Мы удалили твои данные и больше не будем присылать уведомления")


#notification logic
async def sender():
    print("Sending messages")
    data = fetchallusers()
    girls = []

    if data != []:
        for i in data:
            girl = Girlclass.Girl().fromtuple(i)
            girls.append(girl)

    if girls != []:
        for i in girls:
                print("Notifications are being sent to" + i.get_userid())
                i.set_takepill(False)
                i.add_numinc(1)
                i.set_mustpill_from_numinc()
                updateuser(i)
                if i.get_mustpill() == True:
                    await mybot.send_message(i.get_userid(), 'Доброе утро) Не забудь Выпить таблетку')
                elif i.get_mustpill() == False:
                    await mybot.send_message(i.get_userid(), "Доброе утро) Сегодня пить ничего не надо, так что просто желаю тебе отличного дня)")



#takepill checker
async def check_takepill():
    print("Checking takepill for users")
    data = fetchallusers()
    girls = []
    for i in data:
        if girls == {}:
            pass
        else:
            girls.append(Girlclass.Girl().fromtuple(i))

        for girl in girls:
            if girls == []:
                pass
            else:
                if girl.get_takepill() == True:
                    pass
                else:
                    await mybot.send_message(girl.get_userid(), 'Мне кажется, ты забыла выпить таблетку. Напиши "да", когда её выпьешь)')

#Scheduler that is responsible for time tracking. RUns in a separate thread.
#adds tasks to event loop in the main thread
def time_logic():
    timer = schedule.Scheduler()
    print("Scheduler started")
    timer.every().day.at("05:30").do(lambda: loop.create_task(sender()))
    timer.every().day.at("07:00").do(lambda: loop.create_task(check_takepill()))
    while True:
        timer.run_pending()


#waits for user input
async def main():
    await mybot.polling()

if __name__ == "__main__":
    time_logic_thread = threading.Thread(target=time_logic)
    time_logic_thread.start()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
