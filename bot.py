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
        if len(arguments) == 3:
            add_expense(message, arguments[1], arguments[2])
        else:
            bot.send_message(message.chat.id, "Error inserting entry, please try again.")
    elif keyword == "DELETE":
        if len(arguments) == 2:
            delete_expense(message, arguments[1])
        else:
            bot.send_message(message.chat.id, "Error deleting entry, please try again.")
    elif keyword == "VIEW":
        view_expense(message)
    elif keyword == "UPDATE":
        bot.send_message(message.chat.id, "Update")
    elif keyword == "CLEAR":
        clear_expense(message)
    else:
        bot.send_message(message.chat.id, "Message is not recognised")


def add_expense(message, description, value):
    try:
        float(value)
        conn = sqlite3.connect('expense.db')
        print("Opened database successfully")
        params = (message.from_user.id, description, value)
        conn.execute("INSERT INTO EXPENSE (USER, DESCRIPTION, VALUE) VALUES (?, ?, ?)", params)
        conn.commit()
        print("Data has been added")
        bot.send_message(message.chat.id, "Your entry has been added.")
        conn.close()
    except ValueError as e:
        print(e)
        return False
    return True


def view_expense(message):
    conn = sqlite3.connect('expense.db')
    print("Opened database successfully")
    cursor = conn.execute("SELECT ID, DESCRIPTION, VALUE FROM EXPENSE WHERE USER = " + str(message.from_user.id))
    results = ""
    for row in cursor:
        results += "ID: " + str(row[0]) + " DESCRIPTION: " + row[1] + " VALUE: " + str(row[2]) + "\n"
    if results == "":
        print("No results were found")
        bot.send_message(message.chat.id, "No results were found.")
    else:
        print("Data has been fetched")
        bot.send_message(message.chat.id, results)
    conn.close()
    return True


def delete_expense(message, expense_id):
    try:
        int(expense_id)
        conn = sqlite3.connect('expense.db')
        print("Opened database successfully")
        params = (expense_id, message.from_user.id)
        conn.execute("DELETE FROM EXPENSE WHERE ID = ? AND USER = ?", params)
        conn.commit()
        print("Data has been deleted")
        bot.send_message(message.chat.id, "Data has been deleted.")
        conn.close()
    except ValueError as e:
        print(e)
        bot.send_message(message.chat.id, "Please input a numerical ID.")
        return False


def clear_expense(message):
    conn = sqlite3.connect('expense.db')
    print("Opened database successfully")
    conn.execute("DELETE FROM EXPENSE WHERE USER = " + str(message.from_user.id))
    conn.commit()
    print("Data has been cleared")
    bot.send_message(message.chat.id, "Data has been cleared.")
    conn.close()
    return True


# Bot starts to listen for updates
bot.polling()
