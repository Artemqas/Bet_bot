import telebot
import config

from telebot import types

from payment import create_comment, generate_link_for_get_payment, get_operations, checking_is_payment_done, get_comment
from const import *
from bets import *

bot = telebot.TeleBot(config.TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton("Выбрать спорт и получить прогноз")
item2 = types.KeyboardButton("Обратная связь")
markup.add(item1, item2)

markup_choice_sport = types.ReplyKeyboardMarkup(resize_keyboard = True)
item_s1 = types.KeyboardButton("Футбол")
item_s2 = types.KeyboardButton("Баскетбол")
item_s3 = types.KeyboardButton("Теннис")
item_s4 = types.KeyboardButton("Киберспорт")
item_s5 = types.KeyboardButton("В начало")

markup_choice_sport.add(item_s1, item_s2, item_s3, item_s4, item_s5)

markup_payment = types.ReplyKeyboardMarkup(resize_keyboard = True)
item_pay1 = types.KeyboardButton("Оплатить прогноз")
item_pay2 = types.KeyboardButton("Другой спорт")
item_pay3 = types.KeyboardButton("В начало")

markup_payment.add(item_pay1, item_pay2, item_pay3)

markup_paid = types.ReplyKeyboardMarkup(resize_keyboard = True)
it_ok1 = types.KeyboardButton("Оплачено")
it_ok2 = types.KeyboardButton("В начало")

markup_paid.add(it_ok1, it_ok2)

admin_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
admin_item1 = types.KeyboardButton('Продолжить как User')
admin_item2 = types.KeyboardButton('Изменить ставку')

admin_markup.add(admin_item1, admin_item2)

@bot.message_handler(commands=['start'])
def FirstMessage(message):
    if message.chat.id == 1878499259:
        msg = bot.send_message(1878499259, 'Админ.', parse_mode = 'html', reply_markup = admin_markup)
        bot.register_next_step_handler(msg, what_bets)
    else:
        welcome_sti = open('static/sticker_welcome.webp', 'rb')
        oferta = open('static/Oferta.pdf', 'rb')
        bot.send_sticker(message.chat.id, welcome_sti)
        bot.send_message(message.chat.id,
        "🤖Привет, {0.first_name} Я бот Neurobet - твой персональный помощник по ставкам.\nЯ искуственный интеллект, созданный группой аналитиков, и работаю на нейросети.\n\nХочешь получить прогноз на события с коэффициентом выше 1.7?👇\n\nЧтобы получить прогноз, тебе нужно пройти всего 3 шага:\nШаг 1⃣ Выбери вид спорта\nШаг 2⃣ Я сообщу, есть ли надежные прогнозы на сегодня\nШаг 3⃣ Оплати и получи прогноз с коэффициентом выше 1.7\n\nИ вуа-ля, всё готово!\nЖми на кнопку ниже✨".format(message.from_user),
        parse_mode='html', reply_markup = markup)
        bot.send_document(message.chat.id, oferta)


@bot.message_handler(content_types = ['text'])
def choice_sport(message):
    if message.text == 'Выбрать спорт и получить прогноз':
            msg = bot.send_message(message.chat.id, "Выбери вид спорта, на который хочешь сделать ставку", parse_mode = 'html', reply_markup = markup_choice_sport)
            txt = message.text
            bot.register_next_step_handler(msg, choosing_sport)
    elif message.text == 'Обратная связь':
            bot.send_message(message.chat.id, "Напишите @neurobet_administrator для решения проблем", parse_mode = 'html', reply_markup = markup)

@bot.message_handler(content_types = ['text'])
def choosing_sport(message):
    if message.text not in ('Футбол', 'Баскетбол', 'Теннис', 'Киберспорт', 'В начало'):
        bot.send_message(message.chat.id, 'Я вас не понимаю :(\n\nИспользуйте встроенную телеграм-клавиатуру для общения!', parse_mode = 'html', reply_markup = markup)
        choice_sport(message)
    if message.text == 'Футбол':
        msg = bot.send_message(message.chat.id, "{0}".format(FOOTBAL_BET), parse_mode = 'html', reply_markup = markup_payment)
        txt = message.text
        bot.register_next_step_handler(msg, lambda c: paying_for_bet(c, txt))
    elif message.text == 'Баскетбол':
        msg = bot.send_message(message.chat.id, "{0}".format(BASKETBALL_BET), parse_mode = 'html', reply_markup = markup_payment)
        txt = message.text
        bot.register_next_step_handler(msg, lambda c: paying_for_bet(c, txt))
    elif message.text == 'Теннис':
        msg = bot.send_message(message.chat.id, "{0}".format(TENNIS_BET), parse_mode = 'html', reply_markup = markup_payment)
        txt = message.text
        bot.register_next_step_handler(msg, lambda c: paying_for_bet(c, txt))
    elif message.text == 'Киберспорт':
        msg = bot.send_message(message.chat.id, "{0}".format(CYBER_BET), parse_mode = 'html', reply_markup = markup_payment)
        txt = message.text
        bot.register_next_step_handler(msg, lambda c: paying_for_bet(c, txt))
    elif message.text == 'В начало':
        bot.send_message(message.chat.id,'Жми "Выбрать спорт и получить прогноз"!', reply_markup = markup)
        choice_sport(message)

@bot.message_handler(content_types = ['text'])
def paying_for_bet(message, text):
    #bot.send_message(message.chat.id, '')
    if message.text not in ('В начало', 'Другой спорт', 'Оплатить прогноз'):
        bot.send_message(message.chat.id, 'Я вас не понимаю :(\n\nИспользуйте встроенную телеграм-клавиатуру для общения!', parse_mode = 'html', reply_markup = markup)
        choice_sport(message)
    if message.text == 'В начало':
        bot.send_message(message.chat.id, 'Жми "Выбрать спорт и получить прогноз"!\nТебя ждут хорошие деньги, друг!', reply_markup = markup)
        choice_sport(message)
    if message.text == 'Другой спорт':
        msg = bot.send_message(message.chat.id, 'Выбирай по интересам :-)', reply_markup = markup_choice_sport)
        bot.register_next_step_handler(msg, choosing_sport)
    if message.text == 'Оплатить прогноз':
        txt = text
        comment_index = create_comment()
        link_for_payment = generate_link_for_get_payment(comment_index, CONST_AMOUNT)
        bot.send_message(message.chat.id, "Перейдите по ссылке и после оплаты нажми «Оплачено» в чате.\nПроверь, чтобы в окне был указан комментарий к платежу: " + str(comment_index), parse_mode = 'html', reply_markup = None)
        msg = bot.send_message(message.chat.id, link_for_payment, parse_mode = 'html', reply_markup = markup_paid)
        bot.register_next_step_handler(msg, lambda m: process_payment(m, txt))

def process_payment(message, text):
    if message.text not in ('В начало', 'Оплачено'):
        bot.send_message(message.chat.id, 'Я вас не понимаю :(\n\nИспользуйте встроенную телеграм-клавиатуру для общения!', parse_mode = 'html', reply_markup = markup)
        choice_sport(message)
    if message.text == 'В начало':
        bot.send_message(message.chat.id, 'Жми "Выбрать спорт и получить прогноз"!\nТебя ждут хорошие деньги, друг!', reply_markup = markup)
        choice_sport(message)
    elif message.text == 'Оплачено':
        msg = bot.send_message(message.chat.id, "Подождите, проверяю информацию о платеже", parse_mode = 'html', reply_markup = markup)
        get_operations()
        well_sti = open('static/sticker_well.webp', 'rb')
        if checking_is_payment_done(get_comment(), CONST_AMOUNT):
            if text == 'Киберспорт':
                bot.send_message(message.chat.id, "{0}\n\nУдачи!".format(get_last_bet(text)), parse_mode = 'html', reply_markup = markup)
                bot.send_sticker(message.chat.id, well_sti)
                choice_sport(message)
            if text == 'Баскетбол':
                bot.send_message(message.chat.id,  "{0}\n\nУдачи!".format(get_last_bet(text)), parse_mode = 'html', reply_markup = markup)
                bot.send_sticker(message.chat.id, well_sti)
                choice_sport(message)
            if text == 'Теннис':
                bot.send_message(message.chat.id,  "{0}\n\nУдачи!".format(get_last_bet(text)), parse_mode = 'html', reply_markup = markup)
                bot.send_sticker(message.chat.id, well_sti)
                choice_sport(message)
            if text == 'Футбол':
                bot.send_message(message.chat.id,  "{0}\n\nУдачи!".format(get_last_bet(text)), parse_mode = 'html', reply_markup = markup)
                bot.send_sticker(message.chat.id, well_sti)
                choice_sport(message)
        elif not checking_is_payment_done(get_comment(), CONST_AMOUNT):
                bot.send_message(message.chat.id, "Оплата не прошла, если вы считаете, что произошла ошибка, то свяжитесь с администратором @neurobet_administrator", parse_mode = 'html', reply_markup = markup)
                choice_sport(message)
        else:
            bot.send_message(message.chat.id, "Произошла ошибка, если Вы считаете, что оплата прошла, то напишите администратору, иначе повторите попытку.", parse_mode = 'html', reply_markup = markup)
            choice_sport(message)

bot.polling(none_stop=True)
