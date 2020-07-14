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
    bot.send_message(message.chat.id, "Welcome User!")
    help_message(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = "Hello, my name is SleepyExpenseBot and I was created to help manage people's expenditure.\n"
    help_text += "The following commands are used to interact with me.\n"
    help_text += "ADD NAME COST (e.g ADD Burger 2.50)\n"
    help_text += "VIEW\n"
    help_text += "UPDATE EXPENSE_ID NEW_NAME NEW_COST (e.g UPDATE 1 BubbleTea 3.00)\n"
    help_text += "DELETE EXPENSE_ID (e.g DELETE 1)\n"
    help_text += "CLEAR"
    bot.send_message(message.chat.id, help_text)


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
        if len(arguments) == 4:
            update_expense(message, arguments[1], arguments[2], arguments[3])
        else:
            bot.send_message(message.chat.id, "Error updating entry, please try again.")
    elif keyword == "CLEAR":
        clear_expense(message)
    else:
        bot.send_message(message.chat.id, "Message is not recognised")


def add_expense(message, description, value):
    try:
        float(value)
        conn = sqlite3.connect('expense.db')
        params = (message.from_user.id, description, value)
        conn.execute("INSERT INTO EXPENSE (USER, DESCRIPTION, VALUE) VALUES (?, ?, ?)", params)
        conn.commit()
        bot.send_message(message.chat.id, "Your entry has been added.")
        conn.close()
    except ValueError as e:
        print(e)
        return False
    return True


def view_expense(message):
    total = 0
    conn = sqlite3.connect('expense.db')
    cursor = conn.execute("SELECT ID, DESCRIPTION, VALUE FROM EXPENSE WHERE USER = " + str(message.from_user.id))
    results = ""
    for row in cursor:
        total += row[2]
        results += "ID: " + str(row[0]) + " DESCRIPTION: " + row[1] + " VALUE: " + str(row[2]) + "\n"
    if results == "":
        bot.send_message(message.chat.id, "No results were found.")
    else:
        results += "Your total expenditure is $" + str(total)
        bot.send_message(message.chat.id, results)
    conn.close()
    return True


def update_expense(message, expense_id, description, value):
    try:
        float(expense_id)
        try:
            float(value)
            conn = sqlite3.connect('expense.db')
            cursor = conn.cursor()
            params = (description, value, expense_id, message.from_user.id)
            cursor.execute("UPDATE EXPENSE SET DESCRIPTION = ?, VALUE = ? WHERE ID = ? AND USER = ?", params)
            if cursor.rowcount != 0:
                conn.commit()
                bot.send_message(message.chat.id, "Your entry has been updated.")
            else:
                bot.send_message(message.chat.id, "Record does not exist.")
            conn.close()
        except ValueError as e:
            print(e)
            bot.send_message(message.chat.id, "Please input a valid cost.")
            return False
    except ValueError as e:
        print(e)
        bot.send_message(message.chat.id, "Please input a numerical ID.")
        return False
    return True


def delete_expense(message, expense_id):
    try:
        int(expense_id)
        conn = sqlite3.connect('expense.db')
        cursor = conn.cursor()
        params = (expense_id, message.from_user.id)
        cursor.execute("DELETE FROM EXPENSE WHERE ID = ? AND USER = ?", params)
        if cursor.rowcount != 0:
            conn.commit()
            bot.send_message(message.chat.id, "Data has been deleted.")
        else:
            bot.send_message(message.chat.id, "Record does not exist.")
        conn.close()
    except ValueError as e:
        print(e)
        bot.send_message(message.chat.id, "Please input a numerical ID.")
        return False


def clear_expense(message):
    conn = sqlite3.connect('expense.db')
    conn.execute("DELETE FROM EXPENSE WHERE USER = " + str(message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, "Data has been cleared.")
    conn.close()
    return True


# Bot starts to listen for updates
bot.polling()
