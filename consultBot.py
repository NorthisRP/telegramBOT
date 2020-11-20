import config
import json
import telebot
import re

bot = telebot.TeleBot(config.token)
path = 'consults.json'


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Список доступных команд: \n /consults - вывести список свободных консультаций \n /addme [ФИО] [Группа] [Предмет] [Дата] - записаться на консультацию')

@bot.message_handler(commands=['consults'])
def list_of_consults(message):   
    with open(path, 'r', encoding="utf-8") as target:
        data = json.load(target)  
        consults = ""
        for consult in data:
            if (consult["status"] == 'Свободно'):
                consults += "Предмет - %s \n Дата - %s \n Аудитория - %s\n\n" % (consult['subject'], consult['date'], consult['room']) 
        
        bot.send_message(message.chat.id, 'Вот список доступных консультаций: \n \n {}'.format(consults))

@bot.message_handler(commands=['addme'])
def add(message): 
    text = message.text
    try:
        name = re.search(r'([А-Я]{1}[а-яё]{1,23})\s([А-Я]{1}[а-яё]{1,23})\s([А-Я]{1}[а-яё]{1,23})', text).group(0)
        group = re.search(r'[А-Я]{3}-[0-9]{3}', text).group(0)
        subject = re.search(r'(([А-Яа-я]{1,40})\.?\s+)(([а-я]{1,40})\.?)', text).group(0)
        date = re.search(r'\d{2}.\d{2}.\d{4}\s\d{2}:\d{2}', text).group(0)   
    except:
        bot.send_message(message.chat.id,'Введите данные корректно!')
    with open(path, 'r', encoding="utf-8") as target:  
        data = json.load(target)
        success = 0
        for consult in data:
            if consult['subject'] == subject and consult['date'] == date and consult['status'] == "Свободно":
                consult['status'] = 'Занят'
                with open(path, "w", encoding="utf-8") as write_file:
                    json.dump(data, write_file, ensure_ascii=False, indent=4)
                bot.send_message(message.chat.id,'Запись на консультацию прошла успешно')
                success = 1
        if success == 0:
            bot.send_message(message.chat.id,'Запрошенная консультация занята либо не существует')

       
#gh

if __name__ == '__main__':
     bot.polling(none_stop=True)