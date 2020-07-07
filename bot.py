import telebot
import sqlite3

from secret import *

print("-" * 15)
print("Initialising SleepyExpenseBot")

bot = telebot.TeleBot(API_TOKEN)

print("SleepyExpenseBot is ready")
print("-" * 15)
print("Waiting to receive Telegram messages...")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello User!")
    bot.send_message(message.chat.id, "Instructions")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "Bot functions")


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    arguments = message.text.split()
    keyword = arguments[0]
    if keyword == "ADD":
        if len(arguments) == 3 and add_expense(message.from_user.id, arguments[1], arguments[2]):
            bot.send_message(message.chat.id, "Your entry has been added.")
        else:
            bot.send_message(message.chat.id, "Error inserting entry, please try again.")
    elif keyword == "DELETE":
        bot.send_message(message.chat.id, "Delete")
    elif keyword == "VIEW":
        view_expense(message)
    elif keyword == "UPDATE":
        bot.send_message(message.chat.id, "Update")
    else:
        bot.send_message(message.chat.id, "Message is not recognised")


def add_expense(user_id, description, value):
    try:
        float(value)
        conn = sqlite3.connect('expense.db')
        print("Opened database successfully")
        params = (user_id, description, value)
        conn.execute("INSERT INTO EXPENSE (USER, DESCRIPTION, VALUE) VALUES (?, ?, ?)", params)
        conn.commit()
        print("Data added")
        conn.close()
    except ValueError as e:
        print(e)
        return False
    return True


def view_expense(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('expense.db')
    print("Opened database successfully")
    cursor = conn.execute("SELECT ID, DESCRIPTION, VALUE FROM EXPENSE WHERE USER = " + str(user_id))
    results = ""
    for row in cursor:
        results += "ID: " + str(row[0]) + " DESCRIPTION: " + row[1] + " VALUE: " + str(row[2]) + "\n"
    if results == "":
        print("No results were found")
        bot.send_message(message.chat.id, "No results were found")
    else:
        print("Data has been fetched")
        bot.send_message(message.chat.id, results)
    return True


# Bot starts to listen for updates
bot.polling()
